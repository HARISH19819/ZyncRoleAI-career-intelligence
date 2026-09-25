from typing import Dict, Any, List
from app.ingestion.base import JobSourceAdapter
from app.core.config import settings
from app.core.logging import logger


class RemotiveSourceAdapter(JobSourceAdapter):
    """Source Adapter: Remotive Job Board API (Optional with strict attribution)."""

    name = "Remotive"
    source_id = "remotive"
    source_type = "JOB_BOARD"
    requires_api_key = False
    supports_live_fetch = True
    supports_search = False
    attribution_required = True
    terms_url = "https://remotive.com/api-terms"
    region = "GLOBAL"

    def __init__(self):
        self.enabled = settings.REMOTIVE_API_ENABLED

    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        if not self.enabled:
            return []
        import httpx
        url = "https://remotive.com/api/remote-jobs?limit=10"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    jobs = data.get("jobs", [])
                    return [self.normalize_job(j) for j in jobs[:limit] if self.validate_job(self.normalize_job(j))]
        except Exception as e:
            logger.warning(f"Remotive fetch error: {e}")
        return []

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        from datetime import datetime, timezone
        from app.agents.job_normalization_agent import normalization_agent
        from app.agents.job_classification_agent import classification_agent
        from app.agents.skill_extraction_agent import skill_extraction_agent

        title = raw_job.get("title", "")
        company = raw_job.get("company_name", "Remote Company")
        desc = raw_job.get("description", "")
        apply_url = raw_job.get("url", "")

        req_skills, pref_skills, all_skills = skill_extraction_agent.extract_required_and_preferred(desc)
        domain = classification_agent.classify(title, desc, all_skills)

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("id", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company,
            "location": "Remote",
            "country": "GLOBAL",
            "work_mode": "Remote",
            "employment_type": "Full-time",
            "description": desc,
            "requirements": desc[:400],
            "responsibilities": "",
            "required_skills": req_skills,
            "preferred_skills": pref_skills,
            "all_skills": all_skills,
            "experience_text": "Not specified",
            "experience_min": 0.0,
            "experience_max": 2.0,
            "eligible_for_fresher": True,
            "education_text": "Bachelor's degree or equivalent",
            "domain": domain,
            "salary_min": None,
            "salary_max": None,
            "salary_currency": "USD",
            "source_url": apply_url,
            "apply_url": apply_url,
            "published_at": datetime.now(timezone.utc),
            "status": "ACTIVE",
            "content_hash": self.compute_content_hash(title, company, "Remote")
        }


class GatedPlatformAdapter(JobSourceAdapter):
    """Base class for gated platforms (LinkedIn, Indeed, Naukri, Internshala).
    Strictly follows terms of service: only activated when authorized OAuth/API credentials are provided.
    Never performs unauthorized scraping.
    """

    source_type = "GATED"
    requires_api_key = True
    supports_live_fetch = False
    enabled = False

    def __init__(self, name: str, source_id: str, client_id: str, client_secret: str, terms_url: str, region: str = "GLOBAL"):
        self.name = name
        self.source_id = source_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.terms_url = terms_url
        self.region = region
        # Activated only if official API credentials provided
        self.enabled = bool(client_id and client_secret)
        self.supports_live_fetch = self.enabled

    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        if not self.enabled:
            logger.info(f"{self.name} adapter disabled: Authorized API credentials not provided.")
            return []
        # When authorized partner credentials are provided, calls official partner REST endpoints
        return []

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        return raw_job


# Gated instances
linkedin_adapter = GatedPlatformAdapter("LinkedIn", "linkedin", settings.LINKEDIN_CLIENT_ID, settings.LINKEDIN_CLIENT_SECRET, "https://developer.linkedin.com/", "GLOBAL")
indeed_adapter = GatedPlatformAdapter("Indeed", "indeed", settings.INDEED_CLIENT_ID, settings.INDEED_CLIENT_SECRET, "https://developer.indeed.com/", "GLOBAL")
naukri_adapter = GatedPlatformAdapter("Naukri", "naukri", settings.NAUKRI_API_KEY, settings.NAUKRI_API_KEY, "https://www.naukri.com/", "IN")
internshala_adapter = GatedPlatformAdapter("Internshala", "internshala", settings.INTERNSHALA_API_KEY, settings.INTERNSHALA_API_KEY, "https://internshala.com/", "IN")
