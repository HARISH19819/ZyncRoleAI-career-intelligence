import httpx
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.ingestion.base import JobSourceAdapter
from app.core.config import settings
from app.core.logging import logger
from app.agents.job_normalization_agent import normalization_agent
from app.agents.job_classification_agent import classification_agent
from app.agents.skill_extraction_agent import skill_extraction_agent


class AdzunaSourceAdapter(JobSourceAdapter):
    """Source Adapter: Adzuna Job Search REST API."""

    name = "Adzuna"
    source_id = "adzuna"
    source_type = "AGGREGATED_API"
    requires_api_key = True
    supports_live_fetch = True
    supports_search = True
    supports_pagination = True
    attribution_required = True
    terms_url = "https://developer.adzuna.com/"
    region = "GLOBAL"

    def __init__(self):
        self.app_id = settings.ADZUNA_APP_ID
        self.app_key = settings.ADZUNA_APP_KEY
        self.country = settings.ADZUNA_COUNTRY or "us"
        self.enabled = bool(self.app_id and self.app_key)

    async def fetch_jobs(self, query: str = "software engineer", location: str = "", limit: int = 15) -> List[Dict[str, Any]]:
        if not self.enabled:
            logger.info("Adzuna adapter disabled: credentials not provided.")
            return []

        url = f"https://api.adzuna.com/v1/api/jobs/{self.country}/search/1"
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "results_per_page": min(limit, 50),
            "what": query,
            "where": location,
            "content-type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    return [self.normalize_job(j) for j in results if self.validate_job(self.normalize_job(j))]
                else:
                    logger.warning(f"Adzuna API returned {resp.status_code}: {resp.text[:200]}")
                    return []
        except Exception as e:
            logger.error(f"Adzuna fetch error: {e}")
            return []

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        title = raw_job.get("title", "")
        company = raw_job.get("company", {}).get("display_name", "Unknown Company")
        location = raw_job.get("location", {}).get("display_name", "Remote")
        description = raw_job.get("description", "")
        source_url = raw_job.get("redirect_url", "")

        req_skills, pref_skills, all_skills = skill_extraction_agent.extract_required_and_preferred(description)
        exp_info = skill_extraction_agent.extract_experience(description)
        domain = classification_agent.classify(title, description, all_skills)

        work_mode = normalization_agent.normalize_work_mode(f"{title} {description} {location}")
        emp_type = normalization_agent.normalize_employment_type(raw_job.get("contract_time", ""))

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("id", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company,
            "location": location,
            "country": self.country.upper(),
            "work_mode": work_mode,
            "employment_type": emp_type,
            "description": description,
            "requirements": description[:500],
            "responsibilities": "",
            "required_skills": req_skills,
            "preferred_skills": pref_skills,
            "all_skills": all_skills,
            "experience_text": exp_info["experience_text"],
            "experience_min": exp_info["experience_min"],
            "experience_max": exp_info["experience_max"],
            "eligible_for_fresher": exp_info["eligible_for_fresher"],
            "education_text": skill_extraction_agent.extract_education(description),
            "domain": domain,
            "salary_min": raw_job.get("salary_min"),
            "salary_max": raw_job.get("salary_max"),
            "salary_currency": "USD",
            "source_url": source_url,
            "apply_url": source_url,
            "published_at": datetime.now(timezone.utc),
            "status": "ACTIVE",
            "content_hash": self.compute_content_hash(title, company, location)
        }
