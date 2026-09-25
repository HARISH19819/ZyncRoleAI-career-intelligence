import re
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.ingestion.base import JobSourceAdapter
from app.core.logging import logger
from app.agents.job_normalization_agent import normalization_agent
from app.agents.job_classification_agent import classification_agent
from app.agents.skill_extraction_agent import skill_extraction_agent


class ArbeitnowSourceAdapter(JobSourceAdapter):
    """Source Adapter: Arbeitnow open job board API (Authentic global and European tech jobs)."""

    name = "Arbeitnow"
    source_id = "arbeitnow"
    source_type = "JOB_BOARD"
    requires_api_key = False
    supports_live_fetch = True
    supports_search = False
    attribution_required = True
    terms_url = "https://www.arbeitnow.com/api"
    region = "GLOBAL"
    enabled = True

    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 25) -> List[Dict[str, Any]]:
        url = "https://www.arbeitnow.com/api/job-board-api"
        all_jobs = []
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    jobs = data.get("data", [])
                    for j in jobs[:limit]:
                        norm = self.normalize_job(j)
                        if self.validate_job(norm):
                            all_jobs.append(norm)
        except Exception as e:
            logger.warning(f"Arbeitnow fetch error: {e}")
        return all_jobs

    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        title = raw_job.get("title", "")
        company = raw_job.get("company_name", "Technology Employer")
        raw_desc = raw_job.get("description", "")
        clean_desc = re.sub(r'<[^>]+>', ' ', raw_desc)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
        apply_url = raw_job.get("url", "")
        is_remote = raw_job.get("remote", False)
        loc = raw_job.get("location", "Remote" if is_remote else "Global")

        req_skills, pref_skills, all_skills = skill_extraction_agent.extract_required_and_preferred(clean_desc)
        # Add tags as skills if present
        for t in raw_job.get("tags", []):
            if t and t.lower() not in [s.lower() for s in all_skills]:
                all_skills.append(t)

        exp_info = skill_extraction_agent.extract_experience(clean_desc)
        domain = classification_agent.classify(title, clean_desc, all_skills)

        work_mode = "Remote" if is_remote else normalization_agent.normalize_work_mode(f"{title} {loc}")

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("slug", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company,
            "location": loc,
            "country": "GLOBAL",
            "work_mode": work_mode,
            "employment_type": "Full-time",
            "description": clean_desc or title,
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
            "source_url": apply_url,
            "apply_url": apply_url,
            "published_at": datetime.now(timezone.utc),
            "status": "ACTIVE",
            "content_hash": self.compute_content_hash(title, company, loc)
        }
