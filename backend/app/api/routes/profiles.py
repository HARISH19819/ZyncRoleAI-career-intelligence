import os
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.all_models import Profile, CareerPreference, CandidateProfile, UserActivity, Resume
from app.schemas.all_schemas import (
    ProfileResponse, ProfileUpdate, CareerPreferencesSchema,
    OnboardingFullRequest, CandidateProfileSchema
)
from app.api.deps import get_current_user
from app.agents.profile_agent import profile_agent
from app.agents.job_normalization_agent import normalization_agent
from app.services.embeddings.embedding_service import embedding_service

router = APIRouter(prefix="/users", tags=["User Profiles"])


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Retrieve career preferences
    pref_stmt = select(CareerPreference).where(CareerPreference.user_id == current_user.id)
    pref_res = await db.execute(pref_stmt)
    prefs = pref_res.scalar_one_or_none()

    # Retrieve candidate profile
    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    cand_res = await db.execute(cand_stmt)
    cand = cand_res.scalar_one_or_none()

    completeness = cand.completeness_score if cand else 20

    prefs_data = None
    if prefs:
        prefs_data = CareerPreferencesSchema(
            preferred_roles=prefs.preferred_roles or [],
            preferred_domains=prefs.preferred_domains or [],
            preferred_locations=prefs.preferred_locations or [],
            work_modes=prefs.work_modes or [],
            employment_types=prefs.employment_types or [],
            salary_min=prefs.salary_min or 0.0,
            salary_currency=prefs.salary_currency or "USD",
            preferred_company_types=prefs.preferred_company_types or []
        )

    cand_data = None
    if cand:
        cand_data = CandidateProfileSchema(
            career_level=cand.career_level or "fresher",
            domains=cand.domains or [],
            skills=cand.skills or [],
            education=cand.education or [],
            projects=cand.projects or [],
            experience=cand.experience or [],
            certifications=cand.certifications or [],
            preferred_roles=cand.preferred_roles or [],
            preferred_locations=cand.preferred_locations or [],
            work_mode=cand.work_mode or [],
            completeness_score=cand.completeness_score or 0
        )

    return ProfileResponse(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        headline=current_user.headline,
        phone=current_user.phone,
        current_location=current_user.current_location,
        avatar_url=current_user.avatar_url,
        career_preferences=prefs_data,
        candidate_profile=cand_data,
        completeness_percentage=completeness,
        created_at=current_user.created_at
    )


@router.put("/profile", response_model=ProfileResponse)
async def update_profile(
    update_data: ProfileUpdate,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if update_data.first_name is not None:
        current_user.first_name = update_data.first_name
    if update_data.last_name is not None:
        current_user.last_name = update_data.last_name
    if update_data.headline is not None:
        current_user.headline = update_data.headline
    if update_data.phone is not None:
        current_user.phone = update_data.phone
    if update_data.current_location is not None:
        current_user.current_location = update_data.current_location
    if update_data.avatar_url is not None:
        current_user.avatar_url = update_data.avatar_url

    await db.commit()
    await db.refresh(current_user)
    return await get_profile(current_user=current_user, db=db)


@router.put("/preferences")
async def update_career_preferences(
    prefs_in: CareerPreferencesSchema,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    pref_stmt = select(CareerPreference).where(CareerPreference.user_id == current_user.id)
    pref_res = await db.execute(pref_stmt)
    prefs = pref_res.scalar_one_or_none()
    if not prefs:
        prefs = CareerPreference(user_id=current_user.id)
        db.add(prefs)

    prefs.preferred_roles = prefs_in.preferred_roles
    prefs.preferred_domains = prefs_in.preferred_domains
    prefs.preferred_locations = prefs_in.preferred_locations
    prefs.work_modes = prefs_in.work_modes
    prefs.employment_types = prefs_in.employment_types
    prefs.salary_min = prefs_in.salary_min
    prefs.salary_currency = prefs_in.salary_currency
    prefs.preferred_company_types = prefs_in.preferred_company_types

    # Also update candidate profile fields
    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    cand_res = await db.execute(cand_stmt)
    cand = cand_res.scalar_one_or_none()
    if cand:
        cand.preferred_roles = prefs_in.preferred_roles
        cand.domains = prefs_in.preferred_domains
        cand.preferred_locations = prefs_in.preferred_locations
        cand.work_mode = prefs_in.work_modes

    await db.commit()
    return {"message": "Preferences updated successfully."}


@router.post("/onboarding")
async def complete_onboarding(
    data: OnboardingFullRequest,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Processes 4-step onboarding data and synthesizes candidate intelligence."""
    pref_stmt = select(CareerPreference).where(CareerPreference.user_id == current_user.id)
    pref_res = await db.execute(pref_stmt)
    prefs = pref_res.scalar_one_or_none()
    if not prefs:
        prefs = CareerPreference(user_id=current_user.id)
        db.add(prefs)

    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == current_user.id)
    cand_res = await db.execute(cand_stmt)
    cand = cand_res.scalar_one_or_none()
    if not cand:
        cand = CandidateProfile(user_id=current_user.id)
        db.add(cand)

    # Step 1: Education
    if data.education and data.education.degree:
        edu_item = {
            "degree": data.education.degree,
            "specialization": data.education.specialization or "",
            "college": data.education.college or "",
            "graduation_year": data.education.graduation_year or "",
            "status": data.education.current_status or "Fresher"
        }
        cand.education = [edu_item]

    # Step 2: Interests
    if data.interests:
        prefs.preferred_roles = data.interests.desired_roles or []
        prefs.preferred_domains = data.interests.domains or []
        cand.preferred_roles = data.interests.desired_roles or []
        cand.domains = data.interests.domains or []
        cand.career_level = data.interests.experience_level or "fresher"

    # Step 3: Preferences
    if data.preferences:
        prefs.preferred_locations = data.preferences.preferred_cities or ([data.preferences.location] if data.preferences.location else [])
        prefs.work_modes = data.preferences.work_mode or ["Remote", "Hybrid"]
        prefs.salary_min = data.preferences.salary_preference or 0.0
        prefs.employment_types = [data.preferences.employment_preference] if data.preferences.employment_preference else ["Full-time"]

        cand.preferred_locations = prefs.preferred_locations
        cand.work_mode = prefs.work_modes

    # Step 4: Skills
    if data.skills:
        all_raw_skills = (
            data.skills.technical_skills +
            data.skills.tools +
            data.skills.frameworks +
            data.skills.soft_skills
        )
        norm_skills = normalization_agent.normalize_skills(all_raw_skills)
        cand.skills = norm_skills

    # Calculate updated completeness
    cand.completeness_score = profile_agent.calculate_completeness(
        skills=cand.skills or [],
        roles=cand.preferred_roles or [],
        domains=cand.domains or [],
        education=cand.education or [],
        projects=cand.projects or [],
        experience=cand.experience or [],
        has_resume=False
    )

    # Generate candidate embedding
    cand_text = f"{' '.join(cand.preferred_roles or [])} {' '.join(cand.domains or [])} {' '.join(cand.skills or [])}"
    embedding = await embedding_service.get_embedding(cand_text)
    cand.embedding = embedding

    # Record event
    event = UserActivity(
        user_id=current_user.id,
        event_type="onboarding_completed",
        event_data={"completeness": cand.completeness_score}
    )
    db.add(event)

    await db.commit()
    return {"message": "Onboarding completed successfully!", "completeness": cand.completeness_score}


@router.delete("/account")
async def delete_account(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Permanently deletes the user profile and all associated data."""
    # Delete resume files on disk if any
    resumes_stmt = select(Resume).where(Resume.user_id == current_user.id)
    res = await db.execute(resumes_stmt)
    resumes = res.scalars().all()
    for r in resumes:
        if r.storage_path and os.path.exists(r.storage_path):
            try:
                os.remove(r.storage_path)
            except Exception:
                pass

    await db.delete(current_user)
    await db.commit()
    return {"message": "Your account and all associated career data have been permanently erased."}


@router.get("/export-data")
async def export_user_data(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Exports full candidate portfolio and career activity in JSON format."""
    profile_data = await get_profile(current_user=current_user, db=db)
    return {
        "user": profile_data.model_dump() if hasattr(profile_data, "model_dump") else profile_data,
        "exported_at": datetime.now(timezone.utc).isoformat()
    }

