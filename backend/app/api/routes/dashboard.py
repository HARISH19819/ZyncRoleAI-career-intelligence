from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.session import get_db
from app.models.all_models import Profile, Job, Resume, ResumeAnalysis, CandidateProfile, SavedJob, Application, Notification
from app.schemas.all_schemas import DashboardResponse, JobSummary, ApplicationItem, SkillGapItem
from app.api.deps import get_current_user
from app.agents.career_feed_agent import career_feed_agent
from app.agents.skill_gap_agent import skill_gap_agent
from app.core.config import settings

router = APIRouter(prefix="/dashboard", tags=["Career Dashboard"])


@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Greeting based on time of day
    now = datetime.now(timezone.utc)
    hour = now.hour
    if 5 <= hour < 12:
        greeting_text = "Good morning"
    elif 12 <= hour < 17:
        greeting_text = "Good afternoon"
    else:
        greeting_text = "Good evening"

    # Fetch candidate profile
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
    completeness = cand.completeness_score if cand else 20

    # Resume status
    r_stmt = select(Resume).where(Resume.user_id == current_user.id, Resume.is_current == True)
    r_res = await db.execute(r_stmt)
    current_resume = r_res.scalar_one_or_none()
    resume_status = None

    if current_resume:
        a_stmt = select(ResumeAnalysis).where(ResumeAnalysis.resume_id == current_resume.id)
        a_res = await db.execute(a_stmt)
        analysis = a_res.scalar_one_or_none()
        resume_status = {
            "has_resume": True,
            "file_name": current_resume.file_name,
            "uploaded_at": current_resume.uploaded_at,
            "ats_score": analysis.ats_score if analysis else None,
            "detected_skills_count": len(analysis.detected_skills) if analysis else 0,
            "builder_url": settings.ATS_RESUME_BUILDER_URL
        }
    else:
        resume_status = {
            "has_resume": False,
            "builder_url": settings.ATS_RESUME_BUILDER_URL
        }

    # Fetch saved & applied jobs
    saved_stmt = select(SavedJob.job_id).where(SavedJob.user_id == current_user.id)
    saved_res = await db.execute(saved_stmt)
    saved_set = set(saved_res.scalars().all())

    app_stmt = select(Application.job_id, Application.status).where(Application.user_id == current_user.id)
    app_res = await db.execute(app_stmt)
    app_map = {row[0]: row[1] for row in app_res.all()}

    # Fetch active jobs
    jobs_stmt = select(Job).where(Job.status == "ACTIVE")
    jobs_res = await db.execute(jobs_stmt)
    active_jobs = jobs_res.scalars().all()

    job_dicts = []
    for j in active_jobs:
        job_dicts.append({
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "country": j.country,
            "work_mode": j.work_mode,
            "employment_type": j.employment_type,
            "domain": j.domain,
            "salary_min": j.salary_min,
            "salary_max": j.salary_max,
            "salary_currency": j.salary_currency,
            "source_id": j.source_id,
            "apply_url": j.apply_url,
            "source_url": j.source_url,
            "published_at": j.published_at,
            "updated_at": j.updated_at,
            "required_skills": j.required_skills or [],
            "preferred_skills": j.preferred_skills or [],
            "all_skills": j.all_skills or [],
            "eligible_for_fresher": j.eligible_for_fresher,
            "experience_min": j.experience_min,
            "experience_max": j.experience_max,
            "education_text": j.education_text,
            "description": j.description,
            "embedding": j.embedding,
        })

    # Rank recommended jobs
    ranked_jobs = career_feed_agent.rank_feed(
        candidate_profile=cand_dict,
        jobs=job_dicts,
        candidate_embedding=cand.embedding if cand else None,
        saved_job_ids=saved_set,
        application_map=app_map,
        sort_by="match_score",
        limit=5
    )

    strong_matches_count = len([j for j in ranked_jobs if j["match_score"] >= 75.0])
    headline_status = (
        f"{strong_matches_count} strong matches are waiting for your profile today."
        if strong_matches_count > 0
        else "Discover fresh opportunities aligned with your career goals."
    )

    # Skill gap snapshot
    gap_res = skill_gap_agent.analyze_skill_gaps(
        candidate_skills=cand_dict["skills"],
        relevant_jobs=job_dicts,
        top_n=3
    )

    # Recent applications
    rec_app_stmt = (
        select(Application, Job)
        .join(Job, Job.id == Application.job_id)
        .where(Application.user_id == current_user.id)
        .order_by(Application.applied_at.desc())
        .limit(3)
    )
    rec_app_res = await db.execute(rec_app_stmt)
    rec_apps = [
        ApplicationItem(
            id=app.id,
            job_id=job.id,
            job_title=job.title,
            company=job.company,
            location=job.location,
            work_mode=job.work_mode,
            source_name=job.source_id.replace("_", " ").title(),
            apply_url=job.apply_url,
            match_score=None,
            status=app.status,
            applied_at=app.applied_at,
            notes=app.notes,
            follow_up_date=app.follow_up_date
        )
        for app, job in rec_app_res.all()
    ]

    # Unread notifications
    n_stmt = select(func.count(Notification.id)).where(Notification.user_id == current_user.id, Notification.is_read == False)
    n_res = await db.execute(n_stmt)
    unread_count = n_res.scalar_one()

    return DashboardResponse(
        greeting=greeting_text,
        first_name=current_user.first_name,
        headline_status=headline_status,
        profile_readiness_score=completeness,
        resume_status=resume_status,
        recommended_jobs=ranked_jobs,
        skill_gap_snapshot=gap_res["top_missing_skills"],
        recent_applications=rec_apps,
        unread_notifications_count=unread_count
    )
