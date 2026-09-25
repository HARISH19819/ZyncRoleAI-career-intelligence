import sys
import os
import asyncio

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.seed_demo import seed_database

if __name__ == "__main__":
    asyncio.run(seed_database())
