from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.all_models import Profile, Job, CandidateProfile
from app.schemas.all_schemas import SkillGapResponse
from app.api.deps import get_current_user
from app.agents.skill_gap_agent import skill_gap_agent

router = APIRouter(prefix="/skill-gaps", tags=["Skill Gap Intelligence"])


@router.get("", response_model=SkillGapResponse)
async def get_skill_gaps(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    cand_res = await db.execute(cand_stmt)
    cand = cand_res.scalar_one_or_none()

    candidate_skills = cand.skills or [] if cand else []
    user_domains = cand.domains or [] if cand else []

    # Retrieve relevant active jobs
    job_stmt = select(Job).where(Job.status == "ACTIVE")
    if user_domains:
        job_stmt = job_stmt.where(Job.domain.in_(user_domains))

    job_res = await db.execute(job_stmt)
    jobs = job_res.scalars().all()

    # If domain filter resulted in too few jobs, look at all active jobs
    if len(jobs) < 3:
        all_jobs_stmt = select(Job).where(Job.status == "ACTIVE")
        all_res = await db.execute(all_jobs_stmt)
        jobs = all_res.scalars().all()

    jobs_data = []
    for j in jobs:
        jobs_data.append({
            "required_skills": j.required_skills or [],
            "preferred_skills": j.preferred_skills or [],
            "domain": j.domain,
            "title": j.title,
        })

    result = skill_gap_agent.analyze_skill_gaps(
        candidate_skills=candidate_skills,
        relevant_jobs=jobs_data,
        top_n=8
    )

    return SkillGapResponse(
        target_jobs_analyzed=result["target_jobs_analyzed"],
        top_missing_skills=result["top_missing_skills"],
        insights_summary=result["insights_summary"]
    )
