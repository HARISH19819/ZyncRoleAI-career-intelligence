import re
import hashlib
from typing import Dict, List, Optional
from app.core.config import settings
from app.core.logging import logger


class JobClassificationAgent:
    """Agent 4: Classifies jobs into standardized career domains using deterministic rules and AI fallback."""

    DOMAIN_KEYWORDS = {
        "Machine Learning": [
            "machine learning", "ml engineer", "mlops", "deep learning", "neural network",
            "pytorch", "tensorflow", "computer vision", "reinforcement learning"
        ],
        "Artificial Intelligence": [
            "artificial intelligence", "ai engineer", "generative ai", "llm", "large language model",
            "prompt engineer", "ai research", "nlp", "natural language processing"
        ],
        "Data Science": [
            "data scientist", "data science", "predictive model", "statistical modeling",
            "scikit-learn", "pandas", "data modeling"
        ],
        "Data Analytics": [
            "data analyst", "bi analyst", "business intelligence", "tableau", "power bi",
            "sql analyst", "data visualization", "analytics engineer"
        ],
        "Frontend Development": [
            "frontend", "front-end", "react", "react.js", "vue", "angular", "next.js",
            "ui developer", "client-side", "css", "html"
        ],
        "Backend Development": [
            "backend", "back-end", "fastapi", "django", "node.js", "express", "spring boot",
            "api development", "golang", "microservices"
        ],
        "Full Stack Development": [
            "full stack", "fullstack", "mern", "mean stack", "full-stack"
        ],
        "Mobile Development": [
            "mobile developer", "ios", "android", "flutter", "react native", "swift", "kotlin"
        ],
        "DevOps": [
            "devops", "sre", "site reliability", "ci/cd", "kubernetes", "docker",
            "terraform", "infrastructure engineer"
        ],
        "Cloud Computing": [
            "cloud engineer", "aws", "azure", "gcp", "cloud architect", "cloud solutions"
        ],
        "Cybersecurity": [
            "security engineer", "cybersecurity", "infosec", "penetration testing",
            "soc analyst", "vulnerability", "cryptography"
        ],
        "QA / Testing": [
            "qa engineer", "quality assurance", "test automation", "selenium", "cypress",
            "manual tester", "sdet"
        ],
        "Database": [
            "database administrator", "dba", "postgresql", "mysql", "database engineer", "data warehouse"
        ],
        "UI/UX": [
            "ui/ux", "ux designer", "ui designer", "product design", "figma", "wireframe"
        ],
        "Product Management": [
            "product manager", "associate product manager", "apm", "technical product manager"
        ],
        "Embedded Systems": [
            "embedded engineer", "embedded systems", "firmware", "microcontroller", "rtos", "arm"
        ],
        "IoT": [
            "iot", "internet of things", "sensors", "arduino", "raspberry pi"
        ],
        "Salesforce": [
            "salesforce", "apex", "visualforce", "salesforce developer"
        ],
        "Software Development": [
            "software engineer", "software developer", "sde", "programmer", "application developer"
        ]
    }

    def __init__(self):
        self._cache: Dict[str, str] = {}

    def classify(self, title: str, description: str, skills: Optional[List[str]] = None) -> str:
        """Deterministically classifies job domain with high speed and zero cost."""
        content = f"{title} {' '.join(skills or [])} {description[:600]}".lower()
        title_lower = title.lower()

        # Cache check
        content_hash = hashlib.md5(content[:300].encode("utf-8")).hexdigest()
        if content_hash in self._cache:
            return self._cache[content_hash]

        # 1. Prioritize high-signal title matches
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            for kw in keywords:
                # Direct word boundary or phrase match in title
                if re.search(r'\b' + re.escape(kw) + r'\b', title_lower):
                    self._cache[content_hash] = domain
                    return domain

        # 2. Score based on content occurrences
        domain_scores = {}
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            score = 0
            for kw in keywords:
                matches = len(re.findall(r'\b' + re.escape(kw) + r'\b', content))
                score += matches
            if score > 0:
                domain_scores[domain] = score

        if domain_scores:
            best_domain = max(domain_scores, key=domain_scores.get)
            self._cache[content_hash] = best_domain
            return best_domain

        return "Software Development"


classification_agent = JobClassificationAgent()
