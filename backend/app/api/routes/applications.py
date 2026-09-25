from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.all_models import Profile, Application, Job, CandidateProfile, UserActivity
from app.schemas.all_schemas import ApplicationCreate, ApplicationUpdate, ApplicationItem
from app.api.deps import get_current_user
from app.services.matching.matching_engine import matching_engine

router = APIRouter(prefix="/applications", tags=["Application Tracker"])


@router.post("", response_model=ApplicationItem)
async def track_application(
    app_in: ApplicationCreate,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify job exists
    j_stmt = select(Job).where(Job.id == app_in.job_id)
    j_res = await db.execute(j_stmt)
    job = j_res.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")

    # Check existing application
    stmt = select(Application).where(Application.user_id == current_user.id, Application.job_id == app_in.job_id)
    res = await db.execute(stmt)
    app = res.scalar_one_or_none()

    if app:
        app.status = app_in.status or "Applied"
        if app_in.notes:
            app.notes = app_in.notes
        if app_in.follow_up_date:
            app.follow_up_date = app_in.follow_up_date
    else:
        app = Application(
            user_id=current_user.id,
            job_id=app_in.job_id,
            status=app_in.status or "Applied",
            notes=app_in.notes,
            follow_up_date=app_in.follow_up_date,
            applied_at=datetime.now(timezone.utc)
        )
        db.add(app)

    db.add(UserActivity(user_id=current_user.id, event_type="application_created", event_data={"job_id": job.id, "status": app.status}))
    await db.commit()
    await db.refresh(app)

    return ApplicationItem(
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


@router.get("", response_model=List[ApplicationItem])
async def list_applications(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application, Job).join(Job, Job.id == Application.job_id).where(Application.user_id == current_user.id).order_by(Application.applied_at.desc())
    res = await db.execute(stmt)
    rows = res.all()

    # Get candidate profile for match score
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

    items = []
    for app, job in rows:
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
        m = matching_engine.calculate_match(cand_dict, job_dict, cand.embedding if cand else None, job.embedding)
        items.append(ApplicationItem(
            id=app.id,
            job_id=job.id,
            job_title=job.title,
            company=job.company,
            location=job.location,
            work_mode=job.work_mode,
            source_name=job.source_id.replace("_", " ").title(),
            apply_url=job.apply_url,
            match_score=m["match_score"],
            status=app.status,
            applied_at=app.applied_at,
            notes=app.notes,
            follow_up_date=app.follow_up_date
        ))

    return items


@router.patch("/{app_id}", response_model=ApplicationItem)
async def update_application(
    app_id: str,
    update_data: ApplicationUpdate,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application, Job).join(Job, Job.id == Application.job_id).where(Application.id == app_id, Application.user_id == current_user.id)
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application record not found.")

    app, job = row
    if update_data.status:
        app.status = update_data.status
    if update_data.notes is not None:
        app.notes = update_data.notes
    if update_data.follow_up_date is not None:
        app.follow_up_date = update_data.follow_up_date

    await db.commit()
    await db.refresh(app)

    return ApplicationItem(
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


@router.delete("/{app_id}")
async def delete_application(
    app_id: str,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application).where(Application.id == app_id, Application.user_id == current_user.id)
    res = await db.execute(stmt)
    app = res.scalar_one_or_none()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")

    await db.delete(app)
    await db.commit()
    return {"message": "Application removed successfully."}
