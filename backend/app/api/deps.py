from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.all_models import Profile
from app.core.security import get_current_user_token, get_optional_user_token


async def get_current_user(
    token_payload: dict = Depends(get_current_user_token),
    db: AsyncSession = Depends(get_db)
) -> Profile:
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token."
        )

    stmt = select(Profile).where(Profile.id == user_id)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found."
        )

    return user


async def get_optional_current_user(
    token_payload: Optional[dict] = Depends(get_optional_user_token),
    db: AsyncSession = Depends(get_db)
) -> Optional[Profile]:
    if not token_payload:
        return None
    user_id = token_payload.get("sub")
    if not user_id:
        return None
    stmt = select(Profile).where(Profile.id == user_id)
    res = await db.execute(stmt)
    return res.scalar_one_or_none()

