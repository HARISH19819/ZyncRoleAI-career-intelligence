from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.session import get_db
from app.models.all_models import Profile, Notification
from app.schemas.all_schemas import NotificationItem
from app.api.deps import get_current_user

router = APIRouter(prefix="/notifications", tags=["In-App Notifications"])


@router.get("", response_model=List[NotificationItem])
async def list_notifications(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Notification).where(Notification.user_id == current_user.id).order_by(Notification.created_at.desc())
    res = await db.execute(stmt)
    notifs = res.scalars().all()
    return [
        NotificationItem(
            id=n.id,
            title=n.title,
            message=n.message,
            type=n.type,
            link=n.link,
            is_read=n.is_read,
            created_at=n.created_at
        )
        for n in notifs
    ]


@router.patch("/{notif_id}/read")
async def mark_read(
    notif_id: str,
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Notification).where(Notification.id == notif_id, Notification.user_id == current_user.id)
    res = await db.execute(stmt)
    notif = res.scalar_one_or_none()
    if notif:
        notif.is_read = True
        await db.commit()
    return {"message": "Notification marked as read."}


@router.post("/read-all")
async def mark_all_read(
    current_user: Profile = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = update(Notification).where(Notification.user_id == current_user.id).values(is_read=True)
    await db.execute(stmt)
    await db.commit()
    return {"message": "All notifications marked as read."}
