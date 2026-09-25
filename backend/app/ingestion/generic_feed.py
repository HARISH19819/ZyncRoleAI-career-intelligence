from typing import Dict, Any, List
from datetime import datetime, timezone
from app.ingestion.base import JobSourceAdapter
from app.agents.job_normalization_agent import normalization_agent
from app.agents.job_classification_agent import classification_agent
from app.agents.skill_extraction_agent import skill_extraction_agent


class DemoSeedSourceAdapter(JobSourceAdapter):
    """Source Adapter: Demo seed data for development, testing, and offline hackathon demonstration."""

    name = "Demo Dataset"
    source_id = "demo_seed"
    source_type = "DEMO"
    requires_api_key = False
    supports_live_fetch = True
    supports_search = True
    supports_pagination = True
    attribution_required = False
    terms_url = None
    region = "GLOBAL"
    enabled = True

    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 50) -> List[Dict[str, Any]]:
        # This adapter returns structured demo jobs
        return []

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        title = raw_job.get("title", "")
        company = raw_job.get("company", "")
        location = raw_job.get("location", "Remote")
        description = raw_job.get("description", "")
        req_skills = normalization_agent.normalize_skills(raw_job.get("required_skills", []))
        pref_skills = normalization_agent.normalize_skills(raw_job.get("preferred_skills", []))
        all_skills = list(dict.fromkeys(req_skills + pref_skills))
        domain = raw_job.get("domain") or classification_agent.classify(title, description, all_skills)

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("id") or raw_job.get("source_job_id", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company,
            "location": location,
            "country": raw_job.get("country", "US"),
            "work_mode": raw_job.get("work_mode", "Remote"),
            "employment_type": raw_job.get("employment_type", "Full-time"),
            "description": description,
            "requirements": raw_job.get("requirements", ""),
            "responsibilities": raw_job.get("responsibilities", ""),
            "required_skills": req_skills,
            "preferred_skills": pref_skills,
            "all_skills": all_skills,
            "experience_text": raw_job.get("experience_text", "0-1 years"),
            "experience_min": float(raw_job.get("experience_min", 0.0)),
            "experience_max": float(raw_job.get("experience_max", 1.0)),
            "eligible_for_fresher": bool(raw_job.get("eligible_for_fresher", True)),
            "education_text": raw_job.get("education_text", "Bachelor's degree in CS, AI, or related field"),
            "domain": domain,
            "salary_min": raw_job.get("salary_min"),
            "salary_max": raw_job.get("salary_max"),
            "salary_currency": raw_job.get("salary_currency", "USD"),
            "source_url": raw_job.get("source_url", "https://example.com/jobs"),
            "apply_url": raw_job.get("apply_url", "https://example.com/apply"),
            "published_at": raw_job.get("published_at") or datetime.now(timezone.utc),
            "status": "ACTIVE",
            "content_hash": self.compute_content_hash(title, company, location)
        }


demo_source_adapter = DemoSeedSourceAdapter()
