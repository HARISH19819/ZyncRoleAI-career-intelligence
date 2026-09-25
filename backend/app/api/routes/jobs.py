from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, func
from app.db.session import get_db
from app.models.all_models import Profile, Job, JobSource, CandidateProfile, SavedJob, Application, UserActivity
from app.schemas.all_schemas import JobSummary, JobDetail, JobMatchExplanation
from app.api.deps import get_current_user, get_optional_current_user
from app.agents.career_feed_agent import career_feed_agent
from app.services.matching.matching_engine import matching_engine
from app.services.jobs.freshness import calculate_freshness_label

router = APIRouter(prefix="/jobs", tags=["Jobs & Opportunities"])


@router.get("", response_model=List[JobSummary])
async def list_jobs(
    q: Optional[str] = Query(None, description="Search keyword in title, company, skills, or description"),
    domain: Optional[str] = Query(None, description="Filter by career domain"),
    location: Optional[str] = Query(None, description="Filter by city/location"),
    work_mode: Optional[str] = Query(None, description="Remote, Hybrid, or On-site"),
    employment_type: Optional[str] = Query(None, description="Full-time, Internship, Contract"),
    fresher_only: Optional[bool] = Query(False, description="Filter fresher-eligible positions"),
    sort: Optional[str] = Query("match_score", description="match_score, newest, salary"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: Optional[Profile] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    cand_profile = None
    saved_set = set()
    app_map = {}

    if current_user:
        cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
        cand_res = await db.execute(cand_stmt)
        cand_profile = cand_res.scalar_one_or_none()

        saved_stmt = select(SavedJob.job_id).where(SavedJob.user_id == current_user.id)
        saved_res = await db.execute(saved_stmt)
        saved_set = set(saved_res.scalars().all())

        app_stmt = select(Application.job_id, Application.status).where(Application.user_id == current_user.id)
        app_res = await db.execute(app_stmt)
        app_map = {row[0]: row[1] for row in app_res.all()}

    candidate_dict = {
        "skills": cand_profile.skills or [] if cand_profile else [],
        "preferred_roles": cand_profile.preferred_roles or [] if cand_profile else [],
        "domains": cand_profile.domains or [] if cand_profile else [],
        "career_level": cand_profile.career_level or "fresher" if cand_profile else "fresher",
        "education": cand_profile.education or [] if cand_profile else [],
        "preferred_locations": cand_profile.preferred_locations or [] if cand_profile else [],
        "work_mode": cand_profile.work_mode or [] if cand_profile else [],
    }

    # Base query for active jobs
    stmt = select(Job).where(Job.status == "ACTIVE")

    if domain and domain.lower() != "all":
        stmt = stmt.where(Job.domain == domain)

    if work_mode and work_mode.lower() != "all":
        stmt = stmt.where(Job.work_mode == work_mode)

    if employment_type and employment_type.lower() != "all":
        stmt = stmt.where(Job.employment_type == employment_type)

    if fresher_only:
        stmt = stmt.where(or_(Job.eligible_for_fresher == True, Job.experience_min <= 1.0))

    if location:
        stmt = stmt.where(Job.location.ilike(f"%{location}%"))

    if q:
        query_pattern = f"%{q}%"
        stmt = stmt.where(
            or_(
                Job.title.ilike(query_pattern),
                Job.company.ilike(query_pattern),
                Job.description.ilike(query_pattern),
                Job.domain.ilike(query_pattern)
            )
        )

    res = await db.execute(stmt)
    db_jobs = res.scalars().all()

    # Convert to dict for ranking
    job_dicts = []
    for j in db_jobs:
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

    ranked = career_feed_agent.rank_feed(
        candidate_profile=candidate_dict,
        jobs=job_dicts,
        candidate_embedding=cand_profile.embedding if cand_profile else None,
        saved_job_ids=saved_set,
        application_map=app_map,
        sort_by=sort or "match_score",
        limit=offset + limit
    )

    return ranked[offset:offset + limit]


@router.get("/domains")
async def get_domains(db: AsyncSession = Depends(get_db)):
    """Returns domain counts calculated from real active jobs."""
    stmt = select(Job.domain, func.count(Job.id)).where(Job.status == "ACTIVE").group_by(Job.domain)
    res = await db.execute(stmt)
    counts = [{"domain": row[0], "count": row[1]} for row in res.all()]
    return counts


@router.get("/sources")
async def get_sources(db: AsyncSession = Depends(get_db)):
    """Returns configured job sources."""
    stmt = select(JobSource)
    res = await db.execute(stmt)
    sources = res.scalars().all()
    return sources


@router.get("/{job_id}", response_model=JobDetail)
async def get_job_detail(
    job_id: str,
    current_user: Optional[Profile] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Job).where(Job.id == job_id)
    res = await db.execute(stmt)
    job = res.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job opportunity not found.")

    is_saved = False
    app_status = None
    cand = None

    if current_user:
        # Check saved & applied status
        saved_stmt = select(SavedJob).where(SavedJob.user_id == current_user.id, SavedJob.job_id == job.id)
        s_res = await db.execute(saved_stmt)
        is_saved = s_res.scalar_one_or_none() is not None

        app_stmt = select(Application).where(Application.user_id == current_user.id, Application.job_id == job.id)
        a_res = await db.execute(app_stmt)
        app = a_res.scalar_one_or_none()
        app_status = app.status if app else None

        # Calculate match score
        cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
        cand_res = await db.execute(cand_stmt)
        cand = cand_res.scalar_one_or_none()

    match_score = None
    if cand:
        cand_dict = {
            "skills": cand.skills or [],
            "preferred_roles": cand.preferred_roles or [],
            "domains": cand.domains or [],
            "career_level": cand.career_level or "fresher",
            "education": cand.education or [],
            "preferred_locations": cand.preferred_locations or [],
            "work_mode": cand.work_mode or [],
        }
        job_dict = {
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "work_mode": job.work_mode,
            "employment_type": job.employment_type,
            "domain": job.domain,
            "required_skills": job.required_skills or [],
            "preferred_skills": job.preferred_skills or [],
            "all_skills": job.all_skills or [],
            "eligible_for_fresher": job.eligible_for_fresher,
            "experience_min": job.experience_min,
            "experience_max": job.experience_max,
            "education_text": job.education_text,
            "description": job.description,
            "embedding": job.embedding
        }
        res_m = matching_engine.calculate_match(cand_dict, job_dict, cand.embedding, job.embedding)
        match_score = res_m["match_score"]

    if current_user:
        # Record job view activity
        db.add(UserActivity(user_id=current_user.id, event_type="job_viewed", event_data={"job_id": job.id, "title": job.title}))
        await db.commit()

    return JobDetail(
        id=job.id,
        title=job.title,
        company=job.company,
        location=job.location,
        country=job.country,
        work_mode=job.work_mode,
        employment_type=job.employment_type,
        domain=job.domain,
        salary_min=job.salary_min,
        salary_max=job.salary_max,
        salary_currency=job.salary_currency,
        source_id=job.source_id,
        source_name=job.source_id.replace("_", " ").title(),
        apply_url=job.apply_url,
        source_url=job.source_url,
        published_at=job.published_at,
        freshness_label=calculate_freshness_label(job.published_at, job.updated_at),
        top_skills=(job.required_skills or job.all_skills or [])[:4],
        match_score=match_score,
        is_saved=is_saved,
        application_status=app_status,
        description=job.description,
        requirements=job.requirements or "",
        responsibilities=job.responsibilities or "",
        required_skills=job.required_skills or [],
        preferred_skills=job.preferred_skills or [],
        experience_text=job.experience_text or "",
        experience_min=job.experience_min,
        experience_max=job.experience_max,
        eligible_for_fresher=job.eligible_for_fresher,
        education_text=job.education_text or "",
        verified_at=job.verified_at,
        duplicate_sources=[]
    )


@router.get("/{job_id}/match", response_model=JobMatchExplanation)
async def get_job_match_explanation(
    job_id: str,
    current_user: Optional[Profile] = Depends(get_optional_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Job).where(Job.id == job_id)
    res = await db.execute(stmt)
    job = res.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

    cand = None
    if current_user:
        cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
        cand_res = await db.execute(cand_stmt)
        cand = cand_res.scalar_one_or_none()

    cand_dict = {
        "skills": cand.skills or [] if cand else ["Python", "JavaScript", "Problem Solving"],
        "preferred_roles": cand.preferred_roles or [] if cand else [job.title],
        "domains": cand.domains or [] if cand else [job.domain],
        "career_level": cand.career_level or "fresher" if cand else "fresher",
        "education": cand.education or [] if cand else [],
        "preferred_locations": cand.preferred_locations or [] if cand else [job.location],
        "work_mode": cand.work_mode or [] if cand else [job.work_mode],
    }
    job_dict = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "work_mode": job.work_mode,
        "employment_type": job.employment_type,
        "domain": job.domain,
        "required_skills": job.required_skills or [],
        "preferred_skills": job.preferred_skills or [],
        "all_skills": job.all_skills or [],
        "eligible_for_fresher": job.eligible_for_fresher,
        "experience_min": job.experience_min,
        "experience_max": job.experience_max,
        "education_text": job.education_text,
        "description": job.description,
        "embedding": job.embedding
    }

    match_res = matching_engine.calculate_match(cand_dict, job_dict, cand.embedding, job.embedding)

    return JobMatchExplanation(
        job_id=job.id,
        match_score=match_res["match_score"],
        compatibility_level=match_res["compatibility_level"],
        breakdown=match_res["breakdown"],
        matched_skills=match_res["matched_skills"],
        missing_required_skills=match_res["missing_required_skills"],
        missing_preferred_skills=match_res["missing_preferred_skills"],
        strengths=match_res["strengths"],
        concerns=match_res["concerns"],
        explanation=match_res["explanation"],
        how_to_improve=match_res["how_to_improve"]
    )
