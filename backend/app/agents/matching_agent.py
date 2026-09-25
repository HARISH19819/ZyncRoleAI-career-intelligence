from typing import Dict, Any, List, Optional
from app.services.matching.matching_engine import matching_engine


class MatchingAgent:
    """Agent 8: Orchestrates candidate profile to job matching."""

    async def run(
        self,
        candidate_profile: Dict[str, Any],
        job: Dict[str, Any],
        candidate_embedding: Optional[List[float]] = None,
        job_embedding: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        return matching_engine.calculate_match(
            candidate=candidate_profile,
            job=job,
            candidate_embedding=candidate_embedding,
            job_embedding=job_embedding
        )


matching_agent = MatchingAgent()
