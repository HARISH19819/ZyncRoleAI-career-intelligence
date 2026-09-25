import json
import os
import re
from typing import List, Dict, Any, Optional

SKILLS_DICT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "skills_dictionary.json")


class JobNormalizationAgent:
    """Agent 2: Normalizes titles, skills, locations, work modes, and employment types."""

    def __init__(self):
        self.skills_dict: Dict[str, Dict[str, Any]] = {}
        self.alias_to_canonical: Dict[str, str] = {}
        self.domains: List[str] = []
        self._load_dictionary()

    def _load_dictionary(self):
        try:
            if os.path.exists(SKILLS_DICT_PATH):
                with open(SKILLS_DICT_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.skills_dict = data.get("skills", {})
                    self.domains = data.get("domains", [])
                    for canonical, info in self.skills_dict.items():
                        canon = info.get("canonical", canonical)
                        self.alias_to_canonical[canon.lower()] = canon
                        for alias in info.get("aliases", []):
                            self.alias_to_canonical[alias.lower()] = canon
        except Exception as e:
            # Fallback mapping
            self.alias_to_canonical = {
                "python": "Python", "py": "Python",
                "javascript": "JavaScript", "js": "JavaScript",
                "typescript": "TypeScript", "ts": "TypeScript",
                "react": "React", "reactjs": "React", "react.js": "React",
                "sql": "SQL", "docker": "Docker", "aws": "AWS",
                "fastapi": "FastAPI", "machine learning": "Machine Learning",
                "sklearn": "scikit-learn", "scikit-learn": "scikit-learn",
                "tf": "TensorFlow", "tensorflow": "TensorFlow",
                "pytorch": "PyTorch", "pandas": "Pandas", "numpy": "NumPy"
            }

    def normalize_skill(self, skill_name: str) -> str:
        """Normalizes skill alias to its canonical representation."""
        clean = skill_name.strip()
        lower = clean.lower()
        return self.alias_to_canonical.get(lower, clean)

    def normalize_skills(self, skills: List[str]) -> List[str]:
        """Normalizes and deduplicates a list of skills."""
        seen = set()
        result = []
        for s in skills:
            norm = self.normalize_skill(s)
            if norm and norm.lower() not in seen:
                seen.add(norm.lower())
                result.append(norm)
        return result

    def normalize_work_mode(self, text: str) -> str:
        """Normalizes work mode into Remote, Hybrid, or On-site."""
        lower = text.lower() if text else ""
        if "remote" in lower or "wfh" in lower or "work from home" in lower:
            return "Remote"
        elif "hybrid" in lower or "flexible" in lower:
            return "Hybrid"
        return "On-site"

    def normalize_employment_type(self, text: str) -> str:
        """Normalizes employment type."""
        lower = text.lower() if text else ""
        if "intern" in lower or "trainee" in lower or "student" in lower:
            return "Internship"
        elif "contract" in lower or "freelance" in lower or "temp" in lower:
            return "Contract"
        elif "part" in lower:
            return "Part-time"
        return "Full-time"

    def normalize_title(self, title: str) -> str:
        """Cleans title from redundant buzzwords or special symbols."""
        if not title:
            return "Software Professional"
        clean = re.sub(r'[\(\[\{].*?[\)\]\}]', '', title)  # remove parenthesized suffixes
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean or title


normalization_agent = JobNormalizationAgent()
