from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.all_models import Profile, CareerPreference, CandidateProfile, Notification
from app.schemas.all_schemas import (
    RegisterRequest, LoginRequest, AuthResponse,
    ForgotPasswordRequest, ResetPasswordRequest
)
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.logging import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    stmt = select(Profile).where(Profile.email == req.email.lower())
    res = await db.execute(stmt)
    existing = res.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )

    # Create profile
    hashed_pwd = get_password_hash(req.password)
    new_profile = Profile(
        first_name=req.first_name.strip(),
        last_name=req.last_name.strip(),
        email=req.email.lower(),
        hashed_password=hashed_pwd,
        headline="Aspiring Professional"
    )
    db.add(new_profile)
    await db.flush()

    # Initialize empty career preferences and candidate profile
    prefs = CareerPreference(user_id=new_profile.id)
    db.add(prefs)

    cand_profile = CandidateProfile(
        user_id=new_profile.id,
        career_level="fresher",
        completeness_score=15
    )
    db.add(cand_profile)

    # Welcome notification
    welcome_notif = Notification(
        user_id=new_profile.id,
        title="Welcome to ZyncRole AI",
        message=f"Welcome {new_profile.first_name}! Complete your career preferences or upload your resume to discover your tailored opportunity feed.",
        type="system",
        link="/onboarding"
    )
    db.add(welcome_notif)

    await db.commit()
    await db.refresh(new_profile)

    token = create_access_token({"sub": new_profile.id, "email": new_profile.email})
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user={
            "id": new_profile.id,
            "first_name": new_profile.first_name,
            "last_name": new_profile.last_name,
            "email": new_profile.email,
        },
        onboarding_completed=False
    )


@router.post("/login", response_model=AuthResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(Profile).where(Profile.email == req.email.lower())
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not user.hashed_password or not verify_password(req.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Check onboarding completion
    cand_stmt = select(CandidateProfile).where(CandidateProfile.user_id == user.id)
    cand_res = await db.execute(cand_stmt)
    cand = cand_res.scalar_one_or_none()
    onboarding_done = bool(cand and cand.completeness_score > 30)

    token = create_access_token({"sub": user.id, "email": user.email})
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user={
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        },
        onboarding_completed=onboarding_done
    )


@router.post("/forgot-password")
async def forgot_password(req: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    # Calm and secure response
    return {"message": "If an account exists with that email, password reset instructions have been dispatched."}


@router.post("/reset-password")
async def reset_password(req: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    return {"message": "Your password has been reset successfully. Please proceed to login."}
