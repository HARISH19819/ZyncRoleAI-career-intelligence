import re
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.services.embeddings.embedding_service import embedding_service
from app.agents.explanation_agent import explanation_agent


class MatchingEngine:
    """ZyncRole Job Matching Engine: Combines deterministic structured evaluation with semantic similarity."""

    def __init__(self):
        self.weights = {
            "skills": settings.SKILLS_WEIGHT,
            "role": settings.ROLE_WEIGHT,
            "domain": settings.DOMAIN_WEIGHT,
            "experience": settings.EXPERIENCE_WEIGHT,
            "education": settings.EDUCATION_WEIGHT,
            "location": settings.LOCATION_WEIGHT,
            "preference": settings.PREFERENCE_WEIGHT,
            "semantic": settings.SEMANTIC_WEIGHT,
        }

    def compute_skill_score(
        self, candidate_skills: List[str], required_skills: List[str], preferred_skills: List[str]
    ) -> Dict[str, Any]:
        """Calculates skill coverage with heavier penalty for missing required skills."""
        cand_set = {s.lower() for s in candidate_skills}
        req_set = [s for s in required_skills]
        pref_set = [s for s in preferred_skills]

        matched = []
        missing_req = []
        missing_pref = []

        for s in req_set:
            if s.lower() in cand_set:
                matched.append(s)
            else:
                missing_req.append(s)

        for s in pref_set:
            if s.lower() in cand_set:
                matched.append(s)
            else:
                missing_pref.append(s)

        # Coverage score
        req_ratio = len([s for s in req_set if s.lower() in cand_set]) / max(1, len(req_set)) if req_set else 1.0
        pref_ratio = len([s for s in pref_set if s.lower() in cand_set]) / max(1, len(pref_set)) if pref_set else 1.0

        # Required skills carry 75% of skill score, preferred carries 25%
        skill_score = (req_ratio * 75.0) + (pref_ratio * 25.0)
        return {
            "score": min(100.0, max(0.0, skill_score)),
            "matched_skills": list(dict.fromkeys(matched)),
            "missing_required": missing_req,
            "missing_preferred": missing_pref
        }

    def compute_role_score(self, preferred_roles: List[str], job_title: str) -> float:
        """Compares user's preferred roles with the job title."""
        if not preferred_roles:
            return 75.0  # Neutral baseline if user hasn't specified roles

        title_lower = job_title.lower()
        for role in preferred_roles:
            role_lower = role.lower()
            if role_lower in title_lower or title_lower in role_lower:
                return 100.0

            # Sub-token overlap
            role_words = set(re.findall(r'\w+', role_lower))
            title_words = set(re.findall(r'\w+', title_lower))
            overlap = role_words.intersection(title_words)
            if overlap:
                return 80.0

        return 40.0

    def compute_domain_score(self, preferred_domains: List[str], job_domain: str) -> float:
        """Scores alignment between candidate domains and job domain."""
        if not preferred_domains:
            return 75.0

        job_domain_lower = job_domain.lower()
        for dom in preferred_domains:
            dom_lower = dom.lower()
            if dom_lower == job_domain_lower:
                return 100.0
            # Sibling domains (e.g., AI and Machine Learning or Data Science)
            ai_cluster = {"artificial intelligence", "machine learning", "data science"}
            web_cluster = {"frontend development", "backend development", "full stack development", "software development"}
            cloud_cluster = {"cloud computing", "devops"}

            if dom_lower in ai_cluster and job_domain_lower in ai_cluster:
                return 85.0
            if dom_lower in web_cluster and job_domain_lower in web_cluster:
                return 85.0
            if dom_lower in cloud_cluster and job_domain_lower in cloud_cluster:
                return 85.0

        return 35.0

    def compute_experience_score(
        self, candidate_level: str, eligible_for_fresher: bool, min_years: float, max_years: float
    ) -> float:
        """Calculates experience fit."""
        is_cand_fresher = candidate_level.lower() in ["fresher", "student", "entry-level", "0-1 years"]

        if is_cand_fresher:
            if eligible_for_fresher or min_years <= 1.0:
                return 100.0
            elif min_years <= 2.0:
                return 75.0
            elif min_years <= 4.0:
                return 40.0
            else:
                return 20.0
        else:
            # Candidate has experienced status
            return 90.0

    def compute_education_score(self, candidate_education: List[Dict[str, Any]], job_education_text: str) -> float:
        """Compares degree and field relevance."""
        if not candidate_education or not job_education_text:
            return 85.0

        edu_blob = " ".join([f"{e.get('degree', '')} {e.get('specialization', '')}" for e in candidate_education]).lower()
        if any(tech_term in edu_blob for tech_term in ["computer", "ai", "data", "information technology", "b.tech", "b.e.", "mca", "bca"]):
            return 100.0

        return 80.0

    def compute_location_score(
        self, preferred_locations: List[str], user_work_modes: List[str], job_location: str, job_work_mode: str
    ) -> float:
        """Scores location and work mode (Remote/Hybrid/On-site)."""
        # If job is remote and candidate accepts remote
        if job_work_mode == "Remote" and (not user_work_modes or "Remote" in user_work_modes):
            return 100.0

        if user_work_modes and job_work_mode not in user_work_modes:
            mode_penalty = 30.0
        else:
            mode_penalty = 0.0

        if not preferred_locations:
            return max(50.0, 100.0 - mode_penalty)

        job_loc_lower = job_location.lower()
        for loc in preferred_locations:
            if loc.lower() in job_loc_lower or job_loc_lower in loc.lower():
                return max(50.0, 100.0 - mode_penalty)

        return max(40.0, 70.0 - mode_penalty)

    def compute_preference_score(
        self, candidate_work_modes: List[str], candidate_types: List[str], job_work_mode: str, job_type: str
    ) -> float:
        """Evaluates employment type and work conditions."""
        score = 100.0
        if candidate_work_modes and job_work_mode not in candidate_work_modes:
            score -= 20.0
        if candidate_types and job_type not in candidate_types:
            score -= 20.0
        return max(40.0, score)

    def calculate_match(
        self,
        candidate: Dict[str, Any],
        job: Dict[str, Any],
        candidate_embedding: Optional[List[float]] = None,
        job_embedding: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """Calculates 8-dimensional weighted compatibility score and explanation."""
        # 1. Skills
        candidate_skills = candidate.get("skills", [])
        req_skills = job.get("required_skills", [])
        pref_skills = job.get("preferred_skills", [])
        skill_res = self.compute_skill_score(candidate_skills, req_skills, pref_skills)
        skill_score = skill_res["score"]

        # 2. Role
        pref_roles = candidate.get("preferred_roles", [])
        role_score = self.compute_role_score(pref_roles, job.get("title", ""))

        # 3. Domain
        pref_domains = candidate.get("domains", [])
        domain_score = self.compute_domain_score(pref_domains, job.get("domain", "Other"))

        # 4. Experience
        cand_level = candidate.get("career_level", "fresher")
        exp_score = self.compute_experience_score(
            cand_level,
            job.get("eligible_for_fresher", False),
            job.get("experience_min", 0.0),
            job.get("experience_max", 0.0)
        )

        # 5. Education
        cand_edu = candidate.get("education", [])
        edu_score = self.compute_education_score(cand_edu, job.get("education_text", ""))

        # 6. Location
        cand_locations = candidate.get("preferred_locations", [])
        cand_modes = candidate.get("work_mode", [])
        loc_score = self.compute_location_score(
            cand_locations, cand_modes, job.get("location", ""), job.get("work_mode", "On-site")
        )

        # 7. Preferences
        pref_score = self.compute_preference_score(
            cand_modes, candidate.get("employment_types", []), job.get("work_mode", "On-site"), job.get("employment_type", "Full-time")
        )

        # 8. Semantic
        candidate_text = f"{' '.join(pref_roles)} {' '.join(pref_domains)} {' '.join(candidate_skills)}"
        job_text = f"{job.get('title', '')} {job.get('domain', '')} {' '.join(job.get('all_skills', []))} {job.get('description', '')[:400]}"
        sim = embedding_service.calculate_similarity(candidate_embedding, job_embedding, candidate_text, job_text)
        semantic_score = round(sim * 100.0, 1)

        # Overall weighted calculation
        total_score = round(
            (skill_score * self.weights["skills"]) +
            (role_score * self.weights["role"]) +
            (domain_score * self.weights["domain"]) +
            (exp_score * self.weights["experience"]) +
            (edu_score * self.weights["education"]) +
            (loc_score * self.weights["location"]) +
            (pref_score * self.weights["preference"]) +
            (semantic_score * self.weights["semantic"]),
            1
        )
        total_score = min(100.0, max(10.0, total_score))

        # Compatibility level label
        if total_score >= 90.0:
            level = "Excellent Match"
        elif total_score >= 75.0:
            level = "Strong Match"
        elif total_score >= 60.0:
            level = "Potential Match"
        elif total_score >= 40.0:
            level = "Partial Match"
        else:
            level = "Low Match"

        # Generate explanation
        expl = explanation_agent.generate_explanation(
            match_score=total_score,
            job_title=job.get("title", ""),
            company=job.get("company", ""),
            matched_skills=skill_res["matched_skills"],
            missing_required=skill_res["missing_required"],
            missing_preferred=skill_res["missing_preferred"],
            eligible_for_fresher=job.get("eligible_for_fresher", False),
            candidate_level=cand_level,
            domain_match=(domain_score >= 80.0),
            location_match=(loc_score >= 80.0),
            work_mode=job.get("work_mode", "On-site")
        )

        return {
            "match_score": total_score,
            "compatibility_level": level,
            "breakdown": {
                "skill_score": round(skill_score, 1),
                "role_score": round(role_score, 1),
                "domain_score": round(domain_score, 1),
                "experience_score": round(exp_score, 1),
                "education_score": round(edu_score, 1),
                "location_score": round(loc_score, 1),
                "preference_score": round(pref_score, 1),
                "semantic_score": round(semantic_score, 1),
            },
            "matched_skills": skill_res["matched_skills"],
            "missing_required_skills": skill_res["missing_required"],
            "missing_preferred_skills": skill_res["missing_preferred"],
            "strengths": expl["strengths"],
            "concerns": expl["concerns"],
            "explanation": expl["summary"],
            "how_to_improve": expl["how_to_improve"],
        }


matching_engine = MatchingEngine()
