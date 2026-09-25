import httpx
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.ingestion.base import JobSourceAdapter
from app.core.config import settings
from app.core.logging import logger
from app.agents.job_normalization_agent import normalization_agent
from app.agents.job_classification_agent import classification_agent
from app.agents.skill_extraction_agent import skill_extraction_agent


class JoobleSourceAdapter(JobSourceAdapter):
    """Source Adapter: Jooble REST API with request budgeting."""

    name = "Jooble"
    source_id = "jooble"
    source_type = "AGGREGATED_API"
    requires_api_key = True
    supports_live_fetch = True
    supports_search = True
    attribution_required = True
    terms_url = "https://jooble.org/api/about"
    region = "GLOBAL"

    def __init__(self):
        self.api_key = settings.JOOBLE_API_KEY
        self.enabled = bool(self.api_key)

    async def fetch_jobs(self, query: str = "developer", location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []

        url = f"https://jooble.org/api/{self.api_key}"
        payload = {"keywords": query, "location": location, "page": 1}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    jobs = data.get("jobs", [])
                    return [self.normalize_job(j) for j in jobs if self.validate_job(self.normalize_job(j))]
                return []
        except Exception as e:
            logger.error(f"Jooble fetch error: {e}")
            return []

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        title = raw_job.get("title", "")
        company = raw_job.get("company", "Confidential")
        location = raw_job.get("location", "Remote")
        description = raw_job.get("snippet", "")
        source_url = raw_job.get("link", "")

        req_skills, pref_skills, all_skills = skill_extraction_agent.extract_required_and_preferred(description)
        exp_info = skill_extraction_agent.extract_experience(description)
        domain = classification_agent.classify(title, description, all_skills)

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("id", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company,
            "location": location,
            "country": "US",
            "work_mode": normalization_agent.normalize_work_mode(f"{title} {description} {location}"),
            "employment_type": normalization_agent.normalize_employment_type(raw_job.get("type", "")),
            "description": description,
            "requirements": "",
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
            "salary_min": None,
            "salary_max": None,
            "salary_currency": "USD",
            "source_url": source_url,
            "apply_url": source_url,
            "published_at": datetime.now(timezone.utc),
            "status": "ACTIVE",
            "content_hash": self.compute_content_hash(title, company, location)
        }


class TheMuseSourceAdapter(JobSourceAdapter):
    """Source Adapter: The Muse Public Jobs API."""

    name = "The Muse"
    source_id = "the_muse"
    source_type = "JOB_BOARD"
    requires_api_key = False
    supports_live_fetch = True
    supports_search = True
    attribution_required = True
    terms_url = "https://www.themuse.com/developers/api/v2"
    region = "US"

    def __init__(self):
        self.api_key = settings.THE_MUSE_API_KEY
        self.enabled = True  # Public access without key for basic rate-limited queries

    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 15) -> List[Dict[str, Any]]:
        url = "https://www.themuse.com/api/public/jobs"
        params = {"page": 1, "descending": "true"}
        if self.api_key:
            params["api_key"] = self.api_key

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("results", [])
                    return [self.normalize_job(j) for j in results[:limit] if self.validate_job(self.normalize_job(j))]
                return []
        except Exception as e:
            logger.error(f"The Muse fetch error: {e}")
            return []

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        title = raw_job.get("name", "")
        company = raw_job.get("company", {}).get("name", "Unknown Company")
        locations = raw_job.get("locations", [])
        location = locations[0].get("name") if locations else "Remote"
        description = raw_job.get("contents", "")
        # Remove HTML tags from contents
        import re
        clean_desc = re.sub(r'<[^>]+>', ' ', description)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()

        source_url = raw_job.get("refs", {}).get("landing_page", "")

        req_skills, pref_skills, all_skills = skill_extraction_agent.extract_required_and_preferred(clean_desc)
        exp_info = skill_extraction_agent.extract_experience(clean_desc)
        domain = classification_agent.classify(title, clean_desc, all_skills)

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("id", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company,
            "location": location,
            "country": "US",
            "work_mode": normalization_agent.normalize_work_mode(f"{title} {clean_desc} {location}"),
            "employment_type": "Full-time",
            "description": clean_desc,
            "requirements": clean_desc[:400],
            "responsibilities": "",
            "required_skills": req_skills,
            "preferred_skills": pref_skills,
            "all_skills": all_skills,
            "experience_text": exp_info["experience_text"],
            "experience_min": exp_info["experience_min"],
            "experience_max": exp_info["experience_max"],
            "eligible_for_fresher": exp_info["eligible_for_fresher"],
            "education_text": skill_extraction_agent.extract_education(clean_desc),
            "domain": domain,
            "salary_min": None,
            "salary_max": None,
            "salary_currency": "USD",
            "source_url": source_url,
            "apply_url": source_url,
            "published_at": datetime.now(timezone.utc),
            "status": "ACTIVE",
            "content_hash": self.compute_content_hash(title, company, location)
        }
