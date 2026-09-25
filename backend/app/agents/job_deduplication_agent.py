import hashlib
import re
from typing import Optional, List, Tuple
from rapidfuzz import fuzz


class JobDeduplicationAgent:
    """Agent 3: Multi-stage duplicate detection using exact fingerprints, URLs, and RapidFuzz."""

    COMPANY_ABBREVIATIONS = {
        r'\bcorp\b\.?': 'corporation',
        r'\binc\b\.?': 'incorporated',
        r'\bltd\b\.?': 'limited',
        r'\bco\b\.?': 'company',
        r'\bsr\b\.?': 'senior',
        r'\bjr\b\.?': 'junior',
    }

    def _normalize_text_for_fuzzy(self, text: str) -> str:
        lower = text.lower()
        for pat, repl in self.COMPANY_ABBREVIATIONS.items():
            lower = re.sub(pat, repl, lower)
        return re.sub(r'\s+', ' ', lower).strip()

    def compute_content_hash(self, title: str, company: str, location: str) -> str:
        """Computes a normalized SHA-256 hash fingerprint for rapid exact matching."""
        clean_title = re.sub(r'[^a-zA-Z0-9]', '', title.lower())
        clean_company = re.sub(r'[^a-zA-Z0-9]', '', company.lower())
        clean_location = re.sub(r'[^a-zA-Z0-9]', '', location.lower())
        raw = f"{clean_title}:{clean_company}:{clean_location}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def is_fuzzy_duplicate(
        self,
        new_title: str,
        new_company: str,
        new_desc: str,
        existing_title: str,
        existing_company: str,
        existing_desc: str
    ) -> Tuple[bool, float]:
        """Calculates fuzzy similarity between two postings using token_set_ratio."""
        norm_new_comp = self._normalize_text_for_fuzzy(new_company)
        norm_exist_comp = self._normalize_text_for_fuzzy(existing_company)
        company_ratio = fuzz.token_set_ratio(norm_new_comp, norm_exist_comp)
        if company_ratio < 75:
            return False, 0.0

        norm_new_title = self._normalize_text_for_fuzzy(new_title)
        norm_exist_title = self._normalize_text_for_fuzzy(existing_title)
        title_ratio = fuzz.token_set_ratio(norm_new_title, norm_exist_title)
        if title_ratio < 75:
            return False, 0.0

        # Description similarity snippet check
        desc_snippet_new = (new_desc or "")[:300].lower()
        desc_snippet_old = (existing_desc or "")[:300].lower()
        desc_ratio = fuzz.partial_ratio(desc_snippet_new, desc_snippet_old) if desc_snippet_new and desc_snippet_old else 80

        avg_score = (company_ratio * 0.45) + (title_ratio * 0.45) + (desc_ratio * 0.10)
        is_dup = avg_score >= 78.0
        return is_dup, avg_score


deduplication_agent = JobDeduplicationAgent()
