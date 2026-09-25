from datetime import datetime, timezone
from sqlalchemy import select
from app.db.session import AsyncSessionLocal, init_db
from app.models.all_models import Job, JobIngestionRun
from app.agents.job_discovery_agent import job_discovery_agent
from app.core.logging import logger


async def run_ingestion():
    """Runs automated ingestion across all enabled sources, deduplicates, and marks active."""
    logger.info("Starting automated job ingestion run...")
    await init_db()

    async with AsyncSessionLocal() as session:
        run_record = JobIngestionRun(
            source_id="discovery_all",
            status="RUNNING",
            started_at=datetime.now(timezone.utc)
        )
        session.add(run_record)
        await session.commit()

        try:
            discovered_jobs = await job_discovery_agent.discover_jobs(query="developer", limit_per_source=15)
            added = 0
            updated = 0
            duplicates = 0

            for job_data in discovered_jobs:
                content_hash = job_data.get("content_hash")
                stmt = select(Job).where(Job.content_hash == content_hash)
                res = await session.execute(stmt)
                existing = res.scalar_one_or_none()

                if existing:
                    existing.verified_at = datetime.now(timezone.utc)
                    updated += 1
                else:
                    new_job = Job(**job_data)
                    session.add(new_job)
                    added += 1

            run_record.status = "COMPLETED"
            run_record.jobs_fetched = len(discovered_jobs)
            run_record.jobs_added = added
            run_record.jobs_updated = updated
            run_record.jobs_duplicates = duplicates
            run_record.completed_at = datetime.now(timezone.utc)
            await session.commit()
            logger.info(f"Ingestion completed: {added} added, {updated} updated.")
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            run_record.status = "FAILED"
            run_record.error_message = str(e)
            run_record.completed_at = datetime.now(timezone.utc)
            await session.commit()
