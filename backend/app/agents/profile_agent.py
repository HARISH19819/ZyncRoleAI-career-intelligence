from typing import Dict, Any, List, Optional
from app.agents.job_normalization_agent import normalization_agent
from app.agents.job_classification_agent import classification_agent


class CandidateProfileAgent:
    """Agent 6: Synthesizes candidate resume, preferences, and activity into a structured intelligence profile."""

    def build_profile(
        self,
        resume_data: Optional[Dict[str, Any]] = None,
        preferences: Optional[Dict[str, Any]] = None,
        existing_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Combines resume parsing and onboarding preferences into a unified candidate model."""
        existing = existing_profile or {}
        prefs = preferences or {}
        resume = resume_data or {}

        # 1. Merge and normalize skills
        resume_skills = resume.get("detected_skills", [])
        pref_skills = prefs.get("skills", [])
        manual_skills = existing.get("skills", [])
        combined_skills = list(dict.fromkeys(resume_skills + pref_skills + manual_skills))
        normalized_skills = normalization_agent.normalize_skills(combined_skills)

        # 2. Preferred roles & domains
        pref_roles = prefs.get("preferred_roles", []) or existing.get("preferred_roles", [])
        pref_domains = prefs.get("preferred_domains", []) or existing.get("domains", [])

        # Inferred domains from skills if not provided
        if not pref_domains and normalized_skills:
            inferred_domain = classification_agent.classify(
                title="Candidate Profile",
                description=" ".join(normalized_skills),
                skills=normalized_skills
            )
            pref_domains = [inferred_domain]

        # 3. Education
        education = resume.get("detected_education", []) or existing.get("education", [])
        if prefs.get("degree"):
            education.append({
                "degree": prefs.get("degree"),
                "specialization": prefs.get("specialization", ""),
                "college": prefs.get("college", ""),
                "graduation_year": prefs.get("graduation_year", "")
            })

        # 4. Career level
        career_level = prefs.get("experience_level") or existing.get("career_level") or "fresher"

        # 5. Projects and experience
        projects = resume.get("detected_projects", []) or existing.get("projects", [])
        experience = resume.get("detected_experience", []) or existing.get("experience", [])

        # 6. Work modes and locations
        work_modes = prefs.get("work_modes", []) or existing.get("work_mode", ["Remote", "Hybrid"])
        preferred_locations = prefs.get("preferred_locations", []) or existing.get("preferred_locations", [])

        # 7. Calculate completeness score (0-100)
        completeness = self.calculate_completeness(
            skills=normalized_skills,
            roles=pref_roles,
            domains=pref_domains,
            education=education,
            projects=projects,
            experience=experience,
            has_resume=bool(resume_data)
        )

        return {
            "career_level": career_level,
            "domains": pref_domains,
            "skills": normalized_skills,
            "education": education,
            "projects": projects,
            "experience": experience,
            "certifications": existing.get("certifications", []),
            "preferred_roles": pref_roles,
            "preferred_locations": preferred_locations,
            "work_mode": work_modes,
            "completeness_score": completeness,
        }

    def calculate_completeness(
        self,
        skills: List[str],
        roles: List[str],
        domains: List[str],
        education: List[Any],
        projects: List[Any],
        experience: List[Any],
        has_resume: bool
    ) -> int:
        """Calculates profile completeness percentage constructively."""
        score = 0
        if has_resume: score += 25
        if skills and len(skills) >= 5: score += 20
        elif skills: score += 10
        if roles: score += 15
        if domains: score += 10
        if education: score += 10
        if projects or experience: score += 15
        if score > 0: score += 5  # Baseline registration
        return min(100, score)


profile_agent = CandidateProfileAgent()
