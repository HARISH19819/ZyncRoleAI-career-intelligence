from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.all_models import Profile, Job, CandidateProfile
from app.schemas.all_schemas import CareerInsightsResponse
from app.api.deps import get_current_user
from app.agents.career_intelligence_agent import career_intelligence_agent

router = APIRouter(prefix="/career", tags=["Career Intelligence"])


@router.get("/insights", response_model=CareerInsightsResponse)
async def get_career_insights(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    cand_res = await db.execute(cand_stmt)
    cand = cand_res.scalar_one_or_none()

    candidate_skills = cand.skills or [] if cand else []
    user_domains = cand.domains or [] if cand else []

    job_stmt = select(Job).where(Job.status == "ACTIVE")
    job_res = await db.execute(job_stmt)
    jobs = job_res.scalars().all()

    jobs_data = []
    for j in jobs:
        jobs_data.append({
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "work_mode": j.work_mode,
            "domain": j.domain,
            "required_skills": j.required_skills or [],
            "preferred_skills": j.preferred_skills or [],
            "all_skills": j.all_skills or [],
            "eligible_for_fresher": j.eligible_for_fresher,
            "experience_min": j.experience_min,
        })

    insights = career_intelligence_agent.compute_market_insights(
        jobs=jobs_data,
        candidate_skills=candidate_skills,
        user_domains=user_domains
    )

    return CareerInsightsResponse(**insights)


@router.get("/roles/{role_name}")
async def inspect_role_intelligence(
    role_name: str,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    cand_res = await db.execute(cand_stmt)
    cand = cand_res.scalar_one_or_none()
    candidate_skills = cand.skills or [] if cand else []

    job_stmt = select(Job).where(Job.status == "ACTIVE")
    job_res = await db.execute(job_stmt)
    jobs = job_res.scalars().all()

    jobs_data = []
    for j in jobs:
        jobs_data.append({
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "work_mode": j.work_mode,
            "domain": j.domain,
            "required_skills": j.required_skills or [],
            "all_skills": j.all_skills or [],
            "eligible_for_fresher": j.eligible_for_fresher,
            "experience_min": j.experience_min,
        })

    return career_intelligence_agent.inspect_role(role_name, jobs_data, candidate_skills)
