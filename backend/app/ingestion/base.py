from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import hashlib
import httpx
from app.core.logging import logger

BLOCKED_SUBSTRINGS = ["example.com", "pixelcraft", "nexus", "localhost", "test.com", "demo.com"]


async def verify_url_live(url: str, timeout: float = 4.0) -> bool:
    """Verifies that an external job URL is active, live, and not a 404 or dead dummy link."""
    if not url or not (url.startswith("http://") or url.startswith("https://")):
        return False

    url_lower = url.lower()
    if any(dummy in url_lower for dummy in BLOCKED_SUBSTRINGS):
        return False

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    try:
        async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=timeout) as client:
            resp = await client.get(url)
            return resp.status_code < 400
    except Exception as e:
        logger.debug(f"URL liveness check failed for {url}: {e}")
        return False



class JobSourceAdapter(ABC):
    """Abstract base class for all job source adapters."""

    name: str = "Base"
    source_id: str = "base"
    source_type: str = "JOB_BOARD"  # AGGREGATED_API, ATS_API, JOB_BOARD, GATED, DEMO
    enabled: bool = False
    requires_api_key: bool = False
    supports_live_fetch: bool = False
    supports_search: bool = False
    supports_pagination: bool = False
    supports_incremental_sync: bool = False
    attribution_required: bool = False
    terms_url: Optional[str] = None
    region: str = "GLOBAL"

    @abstractmethod
    async def fetch_jobs(self, query: str = "", location: str = "", limit: int = 20) -> List[Dict[str, Any]]:
        """Fetches raw job postings from the external source."""
        pass

    @abstractmethod
    def normalize_job(self, raw_job: Dict[str, Any]) -> Dict[str, Any]:
        """Normalizes external raw job data into canonical ZyncRole Job structure."""
        pass

    def validate_job(self, job_dict: Dict[str, Any]) -> bool:
        """Validates that all essential canonical fields are present and safe."""
        required_fields = ["title", "company", "location", "source_url", "apply_url", "description"]
        for field in required_fields:
            val = job_dict.get(field)
            if not val or not str(val).strip():
                return False

        # Safe URL scheme check
        apply_url = str(job_dict.get("apply_url", ""))
        if not (apply_url.startswith("http://") or apply_url.startswith("https://")):
            return False

        return True

    def compute_content_hash(self, title: str, company: str, location: str) -> str:
        """Generates SHA-256 fingerprint."""
        raw = f"{title.strip().lower()}:{company.strip().lower()}:{location.strip().lower()}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get_source_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.source_id,
            "name": self.name,
            "source_type": self.source_type,
            "enabled": self.enabled,
            "requires_api_key": self.requires_api_key,
            "supports_live_fetch": self.supports_live_fetch,
            "supports_search": self.supports_search,
            "supports_pagination": self.supports_pagination,
            "attribution_required": self.attribution_required,
            "terms_url": self.terms_url,
            "region": self.region,
        }
