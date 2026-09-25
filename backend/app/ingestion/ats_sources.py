import httpx
import re
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.ingestion.base import JobSourceAdapter
from app.core.logging import logger
from app.agents.job_normalization_agent import normalization_agent
from app.agents.job_classification_agent import classification_agent
from app.agents.skill_extraction_agent import skill_extraction_agent


class GreenhouseSourceAdapter(JobSourceAdapter):
    """Source Adapter: Greenhouse public employer Job Board API."""

    name = "Greenhouse"
    source_id = "greenhouse"
    source_type = "ATS_API"
    requires_api_key = False
    supports_live_fetch = True
    supports_search = False
    attribution_required = True
    terms_url = "https://developers.greenhouse.io/job-board.html"
    region = "GLOBAL"
    enabled = True

    DEFAULT_BOARDS = ["github", "gitlab", "cloudflare", "stripe"]

    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 15) -> List[Dict[str, Any]]:
        all_jobs = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            for board in self.DEFAULT_BOARDS[:2]:
                url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
                try:
                    resp = await client.get(url)
                    if resp.status_code == 200:
                        data = resp.json()
                        jobs = data.get("jobs", [])
                        for j in jobs[:8]:
                            norm = self.normalize_job(j, company_name=board.capitalize())
                            if self.validate_job(norm):
                                all_jobs.append(norm)
                except Exception as e:
                    logger.warning(f"Greenhouse board {board} fetch error: {e}")
        return all_jobs[:limit]

    def normalize_job(self, raw_job: Dict[str, Any], company_name: str = "Technology Company") -> Dict[str, Any]:
        title = raw_job.get("title", "")
        location = raw_job.get("location", {}).get("name", "Remote")
        content = raw_job.get("content", "")
        clean_desc = re.sub(r'<[^>]+>', ' ', content)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
        apply_url = raw_job.get("absolute_url", "")

        req_skills, pref_skills, all_skills = skill_extraction_agent.extract_required_and_preferred(clean_desc)
        exp_info = skill_extraction_agent.extract_experience(clean_desc)
        domain = classification_agent.classify(title, clean_desc, all_skills)

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("id", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company_name,
            "location": location,
            "country": "US",
            "work_mode": normalization_agent.normalize_work_mode(f"{title} {location}"),
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
            "content_hash": self.compute_content_hash(title, company_name, location)
        }


class LeverSourceAdapter(JobSourceAdapter):
    """Source Adapter: Lever public postings endpoint."""

    name = "Lever"
    source_id = "lever"
    source_type = "ATS_API"
    requires_api_key = False
    supports_live_fetch = True
    supports_search = False
    attribution_required = True
    terms_url = "https://hire.lever.co/"
    region = "GLOBAL"
    enabled = True

    DEFAULT_SITES = ["netflix", "palantir"]

    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        all_jobs = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            for site in self.DEFAULT_SITES[:1]:
                url = f"https://api.lever.co/v0/postings/{site}?mode=json"
                try:
                    resp = await client.get(url)
                    if resp.status_code == 200:
                        postings = resp.json()
                        for p in postings[:8]:
                            norm = self.normalize_job(p, company_name=site.capitalize())
                            if self.validate_job(norm):
                                all_jobs.append(norm)
                except Exception as e:
                    logger.warning(f"Lever site {site} fetch error: {e}")
        return all_jobs[:limit]

    def normalize_job(self, raw_job: Dict[str, Any], company_name: str = "Tech Company") -> Dict[str, Any]:
        title = raw_job.get("text", "")
        categories = raw_job.get("categories", {})
        location = categories.get("location", "Remote")
        description = raw_job.get("descriptionPlain", "") or raw_job.get("additionalPlain", "")
        apply_url = raw_job.get("hostedUrl", "")

        req_skills, pref_skills, all_skills = skill_extraction_agent.extract_required_and_preferred(description)
        exp_info = skill_extraction_agent.extract_experience(description)
        domain = classification_agent.classify(title, description, all_skills)

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("id", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company_name,
            "location": location,
            "country": "US",
            "work_mode": normalization_agent.normalize_work_mode(f"{title} {location}"),
            "employment_type": normalization_agent.normalize_employment_type(categories.get("commitment", "")),
            "description": description or title,
            "requirements": description[:400],
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
            "source_url": apply_url,
            "apply_url": apply_url,
            "published_at": datetime.now(timezone.utc),
            "status": "ACTIVE",
            "content_hash": self.compute_content_hash(title, company_name, location)
        }


class AshbySourceAdapter(JobSourceAdapter):
    """Source Adapter: Ashby public Job Posting API for configured job boards."""

    name = "Ashby"
    source_id = "ashby"
    source_type = "ATS_API"
    requires_api_key = False
    supports_live_fetch = True
    supports_search = False
    attribution_required = True
    terms_url = "https://www.ashbyhq.com/"
    region = "GLOBAL"
    enabled = True

    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 10) -> List[Dict[str, Any]]:
        # Example public ashby job board
        url = "https://api.ashbyhq.com/posting-api/job-board/openai"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    jobs = data.get("jobs", [])
                    return [self.normalize_job(j, "OpenAI") for j in jobs[:limit] if self.validate_job(self.normalize_job(j, "OpenAI"))]
        except Exception as e:
            logger.warning(f"Ashby fetch error: {e}")
        return []

    def normalize_job(self, raw_job: Dict[str, Any], company_name: str = "Company") -> Dict[str, Any]:
        title = raw_job.get("title", "")
        location = raw_job.get("location", "Remote")
        description = raw_job.get("descriptionHtml", "")
        clean_desc = re.sub(r'<[^>]+>', ' ', description)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
        apply_url = raw_job.get("jobUrl", "") or f"https://jobs.ashbyhq.com/{company_name.lower()}/{raw_job.get('id')}"

        req_skills, pref_skills, all_skills = skill_extraction_agent.extract_required_and_preferred(clean_desc)
        exp_info = skill_extraction_agent.extract_experience(clean_desc)
        domain = classification_agent.classify(title, clean_desc, all_skills)

        return {
            "source_id": self.source_id,
            "source_job_id": str(raw_job.get("id", "")),
            "title": normalization_agent.normalize_title(title),
            "company": company_name,
            "location": location,
            "country": "US",
            "work_mode": normalization_agent.normalize_work_mode(f"{title} {location}"),
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
            "content_hash": self.compute_content_hash(title, company_name, location)
        }
