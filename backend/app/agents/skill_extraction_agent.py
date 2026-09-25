import re
from typing import Dict, List, Tuple, Any
from app.agents.job_normalization_agent import normalization_agent


class SkillExtractionAgent:
    """Agent 5: Extracts required/preferred skills, experience, and education."""

    FRESHER_PATTERNS = [
        r'\bfreshers?\b',
        r'\bentry[- ]level\b',
        r'\bno experience\b',
        r'\b0[- ]\d+\s*(?:years?|yrs?)\b',
        r'\bcollege graduates?\b',
        r'\bstudent(?:s)? can apply\b',
        r'\bfinal[- ]year students?\b',
        r'\bintern(?:ship)?\b',
        r'\bgraduates? welcome\b',
        r'\b0 years?\b',
    ]

    EXP_RANGE_PATTERN = r'(\d+)(?:\s*(?:to|-)\s*(\d+))?\s*(?:\+)?\s*(?:years?|yrs?)'

    EDUCATION_PATTERNS = [
        r'\bB\.?Tech\b', r'\bB\.?E\.?\b', r'\bBCA\b', r'\bMCA\b',
        r'\bM\.?Tech\b', r'\bM\.?S\.?\b', r'\bB\.?S\.?\b',
        r'\bBachelor(?:\'s)?\b', r'\bMaster(?:\'s)?\b', r'\bPh\.?D\b',
        r'\bComputer Science\b', r'\bInformation Technology\b',
        r'\bArtificial Intelligence\b', r'\bData Science\b'
    ]

    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extracts skills present in text using the canonical skills dictionary."""
        if not text:
            return []
        found_skills = set()
        lower_text = text.lower()

        # Check all canonical skills and their aliases
        for alias_lower, canonical in normalization_agent.alias_to_canonical.items():
            # Check with word boundaries
            pattern = r'(?<![a-zA-Z0-9_\-\./])' + re.escape(alias_lower) + r'(?![a-zA-Z0-9_\-\./])'
            if re.search(pattern, lower_text):
                found_skills.add(canonical)

        return sorted(list(found_skills))

    def extract_required_and_preferred(self, description: str, requirements: str = "") -> Tuple[List[str], List[str], List[str]]:
        """Categorizes skills into required vs preferred based on section headings."""
        full_text = f"{requirements}\n{description}"
        all_skills = self.extract_skills_from_text(full_text)

        # Distinguish preferred section
        preferred_skills = []
        required_skills = []

        preferred_match = re.search(r'(?:nice to have|preferred|bonus|plus|good to have):?(.*?)(?:\n\n|\Z)', full_text, re.IGNORECASE | re.DOTALL)
        if preferred_match:
            preferred_text = preferred_match.group(1)
            preferred_skills = self.extract_skills_from_text(preferred_text)

        required_skills = [s for s in all_skills if s not in preferred_skills]

        # If no explicit preferred section, top skills are required, rest preferred
        if not preferred_skills and len(all_skills) > 4:
            required_skills = all_skills[:4]
            preferred_skills = all_skills[4:]
        elif not preferred_skills:
            required_skills = all_skills

        return required_skills, preferred_skills, all_skills

    def extract_experience(self, text: str) -> Dict[str, Any]:
        """Extracts numerical experience range and fresher eligibility."""
        eligible_for_fresher = False
        lower = text.lower()

        for pat in self.FRESHER_PATTERNS:
            if re.search(pat, lower):
                eligible_for_fresher = True
                break

        min_exp = 0.0
        max_exp = 0.0
        exp_text = "Not specified"

        match = re.search(self.EXP_RANGE_PATTERN, lower)
        if match:
            min_val = float(match.group(1))
            max_val = float(match.group(2)) if match.group(2) else min_val
            min_exp = min_val
            max_exp = max_val
            exp_text = f"{int(min_val)}-{int(max_val)} years" if max_val > min_val else f"{int(min_val)}+ years"
            if min_exp == 0.0:
                eligible_for_fresher = True
        elif eligible_for_fresher:
            exp_text = "Freshers welcome / 0-1 years"
            min_exp = 0.0
            max_exp = 1.0

        return {
            "eligible_for_fresher": eligible_for_fresher,
            "experience_min": min_exp,
            "experience_max": max_exp,
            "experience_text": exp_text
        }

    def extract_education(self, text: str) -> str:
        """Extracts required education credentials."""
        found_edu = []
        for pat in self.EDUCATION_PATTERNS:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                found_edu.append(match.group(0))

        if found_edu:
            # Deduplicate case-insensitively
            unique = list({e.lower(): e for e in found_edu}.values())
            return ", ".join(unique)
        return "Bachelor's degree or equivalent"


skill_extraction_agent = SkillExtractionAgent()
