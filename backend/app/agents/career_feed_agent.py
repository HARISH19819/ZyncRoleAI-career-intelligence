from typing import List, Dict, Any, Optional
from app.services.matching.matching_engine import matching_engine
from app.services.jobs.freshness import calculate_freshness_label


class CareerFeedAgent:
    """Agent 12: Personalizes and ranks available opportunities for the candidate's intelligent feed."""

    def rank_feed(
        self,
        candidate_profile: Dict[str, Any],
        jobs: List[Dict[str, Any]],
        candidate_embedding: Optional[List[float]] = None,
        saved_job_ids: Optional[set] = None,
        application_map: Optional[Dict[str, str]] = None,
        sort_by: str = "match_score",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Ranks jobs according to compatibility and user criteria without hallucinating any jobs."""
        saved_set = saved_job_ids or set()
        apps_map = application_map or {}
        scored_jobs = []

        for job in jobs:
            match_res = matching_engine.calculate_match(
                candidate=candidate_profile,
                job=job,
                candidate_embedding=candidate_embedding,
                job_embedding=job.get("embedding")
            )

            job_id = job.get("id")
            freshness = calculate_freshness_label(job.get("published_at"), job.get("updated_at"))

            card_data = {
                "id": job_id,
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "country": job.get("country", "US"),
                "work_mode": job.get("work_mode", "On-site"),
                "employment_type": job.get("employment_type", "Full-time"),
                "domain": job.get("domain", "Other"),
                "salary_min": job.get("salary_min"),
                "salary_max": job.get("salary_max"),
                "salary_currency": job.get("salary_currency", "USD"),
                "source_id": job.get("source_id"),
                "source_name": job.get("source_name") or job.get("source_id", "").replace("_", " ").title(),
                "apply_url": job.get("apply_url"),
                "source_url": job.get("source_url"),
                "published_at": job.get("published_at"),
                "freshness_label": freshness,
                "top_skills": (job.get("required_skills") or job.get("all_skills") or [])[:4],
                "match_score": match_res["match_score"],
                "compatibility_level": match_res["compatibility_level"],
                "matched_skills": match_res["matched_skills"],
                "missing_required_skills": match_res["missing_required_skills"],
                "missing_preferred_skills": match_res["missing_preferred_skills"],
                "explanation": match_res["explanation"],
                "is_saved": job_id in saved_set,
                "application_status": apps_map.get(job_id)
            }
            scored_jobs.append(card_data)

        # Sorting logic
        if sort_by == "newest":
            scored_jobs.sort(key=lambda x: str(x.get("published_at") or ""), reverse=True)
        elif sort_by == "salary":
            scored_jobs.sort(key=lambda x: (x.get("salary_max") or x.get("salary_min") or 0.0), reverse=True)
        else:  # default: highest match_score
            scored_jobs.sort(key=lambda x: x["match_score"], reverse=True)

        return scored_jobs[:limit]


career_feed_agent = CareerFeedAgent()
