import re
from typing import Dict, Any, List, Optional
from app.core.config import settings


class ATSEngine:
    """ZyncRole ATS Compatibility Engine: Evaluates resume readiness across 7 weighted dimensions."""

    def evaluate(
        self,
        raw_text: str,
        sections: Dict[str, str],
        detected_skills: List[str],
        detected_projects: List[Dict[str, Any]],
        detected_experience: List[Dict[str, Any]],
        contact_info: Dict[str, Optional[str]],
        achievements: List[str],
        target_roles: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Calculates ATS score (0-100) and actionable strengths/improvements."""
        strengths = []
        weaknesses = []

        # 1. Keyword / Skill Coverage (25 points)
        skill_count = len(detected_skills)
        if skill_count >= 12:
            keyword_score = 25.0
            strengths.append(f"Excellent technical skill coverage ({skill_count} detected skills)")
        elif skill_count >= 8:
            keyword_score = 20.0
            strengths.append(f"Good technical keyword density ({skill_count} detected skills)")
        elif skill_count >= 4:
            keyword_score = 15.0
            weaknesses.append("Moderate skill coverage; adding more relevant tools or frameworks will boost ATS matching")
        else:
            keyword_score = 8.0
            weaknesses.append("Low detected technical keywords. List specific languages, libraries, and tools")

        # 2. Role Relevance (20 points)
        role_matches = 0
        target_roles = target_roles or ["Software Engineer", "Developer", "Data Scientist", "Machine Learning"]
        text_lower = raw_text.lower()
        for role in target_roles:
            if re.search(r'\b' + re.escape(role.lower()) + r'\b', text_lower):
                role_matches += 1

        if role_matches >= 2:
            role_relevance_score = 20.0
            strengths.append("Strong alignment with targeted career roles")
        elif role_matches >= 1:
            role_relevance_score = 15.0
            strengths.append("Relevant role titles present in summary or experience")
        else:
            role_relevance_score = 10.0
            weaknesses.append("Explicit target role titles not found in headline or summary; include clear target titles")

        # 3. Resume Section Completeness (15 points)
        standard_sections = ["summary", "education", "experience", "projects", "skills"]
        present_sections = [s for s in standard_sections if s in sections and len(sections[s]) > 20]
        section_ratio = len(present_sections) / len(standard_sections)
        section_score = round(section_ratio * 15.0, 1)

        if section_ratio >= 0.8:
            strengths.append("Clean resume structure with all essential ATS sections present")
        else:
            missing = [s.capitalize() for s in standard_sections if s not in present_sections]
            weaknesses.append(f"Missing recommended standard sections: {', '.join(missing)}")

        # 4. Project & Experience Relevance (15 points)
        has_projects = len(detected_projects) > 0 or "project" in sections
        has_experience = len(detected_experience) > 0 or "experience" in sections
        if has_projects and has_experience:
            project_score = 15.0
            strengths.append("Balanced combination of hands-on projects and practical experience")
        elif has_projects:
            project_score = 13.0
            strengths.append("Solid project showcase highlighting practical implementation skills")
        elif has_experience:
            project_score = 13.0
            strengths.append("Clear work and internship history")
        else:
            project_score = 6.0
            weaknesses.append("Project and experience sections are sparse; detail at least 2 key projects")

        # 5. Formatting & Readability (10 points)
        formatting_score = 10.0
        # Check for excessive special symbols or weird characters
        special_char_count = len(re.findall(r'[\u2022\u25CF\u25B6\u25C6\u2714\u2713★☆]', raw_text))
        if special_char_count > 30:
            formatting_score -= 3.0
            weaknesses.append("High number of non-standard bullet symbols; standard ASCII bullets are preferred for ATS")

        # Check line length / paragraph density
        lines = [l for l in raw_text.split("\n") if l.strip()]
        long_paragraphs = [l for l in lines if len(l.split()) > 75]
        if len(long_paragraphs) > 3:
            formatting_score -= 2.0
            weaknesses.append("Dense paragraphs detected; convert long blocks of text into concise bullet points")

        formatting_score = max(4.0, formatting_score)
        if formatting_score >= 8.5:
            strengths.append("High readability with clean parsing and line breaks")

        # 6. Achievement Evidence & Quantified Results (10 points)
        achieve_count = len(achievements)
        if achieve_count >= 3:
            achievement_score = 10.0
            strengths.append(f"Contains {achieve_count} quantified achievements with measurable metrics (%, numbers, scale)")
        elif achieve_count >= 1:
            achievement_score = 7.0
            weaknesses.append("Add more measurable outcomes (e.g. 'reduced latency by 20%', 'served 500+ users')")
        else:
            achievement_score = 4.0
            weaknesses.append("No quantified achievements detected. Highlight measurable results and metrics")

        # 7. Contact & Profile Completeness (5 points)
        contact_points = 0.0
        if contact_info.get("email"):
            contact_points += 2.0
        if contact_info.get("phone"):
            contact_points += 1.0
        if contact_info.get("github") or contact_info.get("linkedin") or contact_info.get("portfolio"):
            contact_points += 2.0
        contact_score = min(5.0, contact_points)

        if contact_score == 5.0:
            strengths.append("Complete contact profile including links to professional profiles/code repositories")
        else:
            missing_contact = []
            if not contact_info.get("email"): missing_contact.append("email")
            if not contact_info.get("phone"): missing_contact.append("phone number")
            if not (contact_info.get("github") or contact_info.get("linkedin")): missing_contact.append("GitHub/LinkedIn")
            weaknesses.append(f"Add missing contact details: {', '.join(missing_contact)}")

        total_score = round(
            keyword_score + role_relevance_score + section_score +
            project_score + formatting_score + achievement_score + contact_score,
            1
        )
        total_score = min(100.0, max(0.0, total_score))

        return {
            "ats_score": total_score,
            "keyword_score": keyword_score,
            "role_relevance_score": role_relevance_score,
            "section_score": section_score,
            "project_score": project_score,
            "formatting_score": formatting_score,
            "achievement_score": achievement_score,
            "contact_score": contact_score,
            "strengths": strengths,
            "weaknesses": weaknesses,
        }


ats_engine = ATSEngine()
