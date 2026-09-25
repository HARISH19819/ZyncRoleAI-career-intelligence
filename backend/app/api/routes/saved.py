from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.all_models import Profile, SavedJob, Job, CandidateProfile, Application, UserActivity
from app.schemas.all_schemas import JobSummary
from app.api.deps import get_current_user
from app.services.matching.matching_engine import matching_engine
from app.services.jobs.freshness import calculate_freshness_label

router = APIRouter(prefix="/saved", tags=["Saved Jobs"])


@router.post("/{job_id}")
async def save_job(
    job_id: str,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(SavedJob).where(SavedJob.user_id == current_user.id, SavedJob.job_id == job_id)
    res = await db.execute(stmt)
    existing = res.scalar_one_or_none()
    if existing:
        return {"message": "Job is already saved.", "is_saved": True}

    saved = SavedJob(user_id=current_user.id, job_id=job_id)
    db.add(saved)
    db.add(UserActivity(user_id=current_user.id, event_type="job_saved", event_data={"job_id": job_id}))
    await db.commit()
    return {"message": "Job saved successfully.", "is_saved": True}


@router.delete("/{job_id}")
async def unsave_job(
    job_id: str,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(SavedJob).where(SavedJob.user_id == current_user.id, SavedJob.job_id == job_id)
    res = await db.execute(stmt)
    existing = res.scalar_one_or_none()
    if existing:
        await db.delete(existing)
        db.add(UserActivity(user_id=current_user.id, event_type="job_unsaved", event_data={"job_id": job_id}))
        await db.commit()
    return {"message": "Job removed from saved list.", "is_saved": False}


@router.get("", response_model=List[JobSummary])
async def list_saved_jobs(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Job).join(SavedJob, SavedJob.job_id == Job.id).where(SavedJob.user_id == current_user.id)
    res = await db.execute(stmt)
    jobs = res.scalars().all()

    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    cand_res = await db.execute(cand_stmt)
    cand = cand_res.scalar_one_or_none()
    cand_dict = {
        "skills": cand.skills or [] if cand else [],
        "preferred_roles": cand.preferred_roles or [] if cand else [],
        "domains": cand.domains or [] if cand else [],
        "career_level": cand.career_level or "fresher" if cand else "fresher",
        "education": cand.education or [] if cand else [],
        "preferred_locations": cand.preferred_locations or [] if cand else [],
        "work_mode": cand.work_mode or [] if cand else [],
    }

    app_stmt = select(Application.job_id, Application.status).where(Application.user_id == current_user.id)
    app_res = await db.execute(app_stmt)
    app_map = {row[0]: row[1] for row in app_res.all()}

    results = []
    for j in jobs:
        job_dict = {
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "work_mode": j.work_mode,
            "employment_type": j.employment_type,
            "domain": j.domain,
            "required_skills": j.required_skills or [],
            "preferred_skills": j.preferred_skills or [],
            "all_skills": j.all_skills or [],
            "eligible_for_fresher": j.eligible_for_fresher,
            "experience_min": j.experience_min,
            "experience_max": j.experience_max,
            "education_text": j.education_text,
            "description": j.description,
            "embedding": j.embedding
        }
        match_res = matching_engine.calculate_match(cand_dict, job_dict, cand.embedding if cand else None, j.embedding)
        results.append(JobSummary(
            id=j.id,
            title=j.title,
            company=j.company,
            location=j.location,
            country=j.country,
            work_mode=j.work_mode,
            employment_type=j.employment_type,
            domain=j.domain,
            salary_min=j.salary_min,
            salary_max=j.salary_max,
            salary_currency=j.salary_currency,
            source_id=j.source_id,
            source_name=j.source_id.replace("_", " ").title(),
            apply_url=j.apply_url,
            source_url=j.source_url,
            published_at=j.published_at,
            freshness_label=calculate_freshness_label(j.published_at, j.updated_at),
            top_skills=(j.required_skills or j.all_skills or [])[:4],
            match_score=match_res["match_score"],
            is_saved=True,
            application_status=app_map.get(j.id)
        ))

    return results
