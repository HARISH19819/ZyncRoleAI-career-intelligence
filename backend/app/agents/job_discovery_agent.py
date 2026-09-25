from typing import List, Dict, Any
from app.ingestion.source_registry import source_registry
from app.agents.job_deduplication_agent import deduplication_agent
from app.services.embeddings.embedding_service import embedding_service
from app.core.logging import logger


class JobDiscoveryAgent:
    """Agent 1: Discovers and collects available jobs across enabled source adapters."""

    async def discover_jobs(self, query: str = "engineer", location: str = "", limit_per_source: int = 15) -> List[Dict[str, Any]]:
        enabled_sources = source_registry.get_enabled_sources()
        all_discovered = []

        for source in enabled_sources:
            try:
                logger.info(f"Discovering jobs from source: {source.name}")
                jobs = await source.fetch_jobs(query=query, location=location, limit=limit_per_source)
                all_discovered.extend(jobs)
            except Exception as e:
                logger.error(f"Error fetching from source {source.name}: {e}")
                continue  # Never let one failed source stop others

        return all_discovered


job_discovery_agent = JobDiscoveryAgent()
