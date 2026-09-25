import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.services.jobs.ingestion_service import run_ingestion

if __name__ == "__main__":
    asyncio.run(run_ingestion())
