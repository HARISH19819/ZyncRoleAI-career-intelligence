import os
import shutil
import hashlib
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.all_models import Profile, Resume, ResumeAnalysis, CandidateProfile, Notification, UserActivity
from app.schemas.all_schemas import ResumeResponse, ResumeAnalysisResponse, ATSScoreBreakdown
from app.api.deps import get_current_user
from app.services.resume.parser import resume_parser
from app.services.ats.ats_engine import ats_engine
from app.services.embeddings.embedding_service import embedding_service
from app.agents.profile_agent import profile_agent
from app.core.config import settings
from app.core.logging import logger

router = APIRouter(prefix="/resume", tags=["Resume Center & ATS"])

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Securely uploads, parses, and evaluates resume ATS score."""
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported format. Only PDF, DOCX, and TXT files are accepted."
        )

    # Save to safe local storage
    user_file_hash = hashlib.sha256(f"{current_user.id}:{file.filename}".encode("utf-8")).hexdigest()[:16]
    safe_name = f"{current_user.id}_{user_file_hash}{ext}"
    file_path = os.path.join(UPLOAD_DIR, safe_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)
    if file_size > 5 * 1024 * 1024:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum limit of 5 MB."
        )

    try:
        # Parse resume
        parsed_data = resume_parser.parse(file_path, file.filename)
    except Exception as e:
        logger.error(f"Resume parsing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unable to read resume structure: {str(e)}"
        )

    # Retrieve candidate target roles for role-relevance scoring
    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    cand_res = await db.execute(cand_stmt)
    cand_profile = cand_res.scalar_one_or_none()
    target_roles = cand_profile.preferred_roles if cand_profile else []

    # Run ATS Compatibility Engine
    ats_result = ats_engine.evaluate(
        raw_text=parsed_data["raw_text"],
        sections=parsed_data["sections"],
        detected_skills=parsed_data["detected_skills"],
        detected_projects=parsed_data["detected_projects"],
        detected_experience=parsed_data["detected_experience"],
        contact_info=parsed_data["contact_info"],
        achievements=parsed_data["achievements"],
        target_roles=target_roles
    )

    # Mark previous resumes as not current
    old_stmt = select(Resume).where(Resume.user_id == current_user.id)
    old_res = await db.execute(old_stmt)
    for old_r in old_res.scalars():
        old_r.is_current = False

    # Store new resume
    new_resume = Resume(
        user_id=current_user.id,
        file_name=file.filename or f"resume{ext}",
        file_type=ext.lstrip("."),
        storage_path=file_path,
        file_size=file_size,
        raw_text=parsed_data["raw_text"],
        is_current=True,
        processing_status="COMPLETED",
        content_hash=hashlib.sha256(parsed_data["raw_text"].encode("utf-8")).hexdigest()
    )
    db.add(new_resume)
    await db.flush()

    # Store analysis
    analysis = ResumeAnalysis(
        resume_id=new_resume.id,
        ats_score=ats_result["ats_score"],
        keyword_score=ats_result["keyword_score"],
        role_relevance_score=ats_result["role_relevance_score"],
        section_score=ats_result["section_score"],
        project_score=ats_result["project_score"],
        formatting_score=ats_result["formatting_score"],
        achievement_score=ats_result["achievement_score"],
        contact_score=ats_result["contact_score"],
        strengths=ats_result["strengths"],
        weaknesses=ats_result["weaknesses"],
        detected_skills=parsed_data["detected_skills"],
        detected_projects=parsed_data["detected_projects"],
        detected_experience=parsed_data["detected_experience"],
        detected_education=parsed_data["detected_education"],
        raw_structured_profile=parsed_data
    )
    db.add(analysis)

    # Update candidate profile with detected data
    if not cand_profile:
        cand_profile = CandidateProfile(user_id=current_user.id)
        db.add(cand_profile)

    combined_skills = list(dict.fromkeys((cand_profile.skills or []) + parsed_data["detected_skills"]))
    cand_profile.skills = combined_skills
    if parsed_data["detected_education"]:
        cand_profile.education = parsed_data["detected_education"]
    if parsed_data["detected_projects"]:
        cand_profile.projects = parsed_data["detected_projects"]
    if parsed_data["detected_experience"]:
        cand_profile.experience = parsed_data["detected_experience"]

    cand_profile.completeness_score = profile_agent.calculate_completeness(
        skills=cand_profile.skills,
        roles=cand_profile.preferred_roles or [],
        domains=cand_profile.domains or [],
        education=cand_profile.education or [],
        projects=cand_profile.projects or [],
        experience=cand_profile.experience or [],
        has_resume=True
    )

    # Refresh candidate embedding
    cand_text = f"{' '.join(cand_profile.preferred_roles or [])} {' '.join(cand_profile.domains or [])} {' '.join(cand_profile.skills or [])}"
    cand_profile.embedding = await embedding_service.get_embedding(cand_text)

    # In-app Notification
    notif = Notification(
        user_id=current_user.id,
        title="Resume Analysis Complete",
        message=f"Your ZyncRole ATS Compatibility Score is {ats_result['ats_score']}/100 with {len(parsed_data['detected_skills'])} detected skills.",
        type="resume",
        link="/resume/analysis"
    )
    db.add(notif)

    # Log user activity
    db.add(UserActivity(user_id=current_user.id, event_type="resume_uploaded", event_data={"ats_score": ats_result["ats_score"]}))

    await db.commit()

    return {
        "message": "Resume processed successfully.",
        "resume_id": new_resume.id,
        "ats_score": ats_result["ats_score"],
        "detected_skills_count": len(parsed_data["detected_skills"])
    }


@router.get("/current")
async def get_current_resume(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Resume).where(Resume.user_id == current_user.id, Resume.is_current == True)
    res = await db.execute(stmt)
    resume = res.scalar_one_or_none()
    if not resume:
        return {"current_resume": None}

    # Fetch analysis
    a_stmt = select(ResumeAnalysis).where(ResumeAnalysis.resume_id == resume.id)
    a_res = await db.execute(a_stmt)
    analysis = a_res.scalar_one_or_none()

    return {
        "current_resume": {
            "id": resume.id,
            "file_name": resume.file_name,
            "file_type": resume.file_type,
            "file_size": resume.file_size,
            "uploaded_at": resume.uploaded_at,
            "ats_score": analysis.ats_score if analysis else None,
            "detected_skills": analysis.detected_skills if analysis else [],
            "builder_url": settings.ATS_RESUME_BUILDER_URL
        }
    }


@router.get("/analysis", response_model=ResumeAnalysisResponse)
async def get_resume_analysis(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Resume).where(Resume.user_id == current_user.id, Resume.is_current == True)
    res = await db.execute(stmt)
    resume = res.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active resume found. Please upload a resume first."
        )

    a_stmt = select(ResumeAnalysis).where(ResumeAnalysis.resume_id == resume.id)
    a_res = await db.execute(a_stmt)
    analysis = a_res.scalar_one_or_none()
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume analysis not found."
        )

    return ResumeAnalysisResponse(
        resume_id=resume.id,
        ats_score=analysis.ats_score,
        breakdown=ATSScoreBreakdown(
            keyword_score=analysis.keyword_score,
            role_relevance_score=analysis.role_relevance_score,
            section_score=analysis.section_score,
            project_score=analysis.project_score,
            formatting_score=analysis.formatting_score,
            achievement_score=analysis.achievement_score,
            contact_score=analysis.contact_score,
        ),
        strengths=analysis.strengths or [],
        weaknesses=analysis.weaknesses or [],
        detected_skills=analysis.detected_skills or [],
        detected_projects=analysis.detected_projects or [],
        detected_experience=analysis.detected_experience or [],
        detected_education=analysis.detected_education or [],
        builder_url=settings.ATS_RESUME_BUILDER_URL,
        created_at=analysis.created_at
    )


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: str,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    res = await db.execute(stmt)
    resume = res.scalar_one_or_none()
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    if os.path.exists(resume.storage_path):
        try:
            os.remove(resume.storage_path)
        except Exception:
            pass

    await db.delete(resume)
    await db.commit()
    return {"message": "Resume and analysis deleted successfully."}
