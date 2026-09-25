from fastapi import APIRouter, Header, HTTPException, status, BackgroundTasks
from app.core.config import settings
from app.core.logging import logger
from app.services.jobs.ingestion_service import run_ingestion

router = APIRouter(prefix="/internal", tags=["Internal Tasks"])


@router.post("/ingestion/run")
async def trigger_ingestion(
    background_tasks: BackgroundTasks,
    x_internal_secret: str = Header(..., alias="X-Internal-Secret")
):
    """Protected endpoint for automated cron/GitHub Actions ingestion runs."""
    if x_internal_secret != settings.INTERNAL_INGESTION_SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Invalid internal ingestion secret."
        )

    background_tasks.add_task(run_ingestion)
    return {"message": "Job ingestion triggered in background."}
