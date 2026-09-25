from typing import List, Dict, Any
from collections import Counter
from app.agents.job_normalization_agent import normalization_agent


class SkillGapAgent:
    """Agent 10: Aggregates recurring skill gaps across target opportunities and calculates real impact."""

    def analyze_skill_gaps(
        self,
        candidate_skills: List[str],
        relevant_jobs: List[Dict[str, Any]],
        top_n: int = 8
    ) -> Dict[str, Any]:
        """Calculates exact missing skill frequencies and impact from available job data."""
        if not relevant_jobs:
            return {
                "target_jobs_analyzed": 0,
                "top_missing_skills": [],
                "insights_summary": "Explore more opportunities in your target domains to generate personalized skill gap insights."
            }

        total_jobs = len(relevant_jobs)
        candidate_skill_set = {s.lower() for s in candidate_skills}

        # Track frequency of skills across required and preferred lists
        req_counter = Counter()
        pref_counter = Counter()
        all_job_skills = Counter()

        for job in relevant_jobs:
            reqs = job.get("required_skills", [])
            prefs = job.get("preferred_skills", [])
            for s in reqs:
                norm = normalization_agent.normalize_skill(s)
                req_counter[norm] += 1
                all_job_skills[norm] += 1
            for s in prefs:
                norm = normalization_agent.normalize_skill(s)
                pref_counter[norm] += 1
                all_job_skills[norm] += 1

        missing_skills_data = []

        for skill, total_count in all_job_skills.most_common():
            if skill.lower() not in candidate_skill_set:
                pct = round((total_count / total_jobs) * 100.0, 1)
                req_count = req_counter.get(skill, 0)

                # Determine impact based on frequency and requirement strength
                if pct >= 40.0 or req_count >= 3:
                    impact = "High"
                elif pct >= 20.0 or req_count >= 1:
                    impact = "Medium"
                else:
                    impact = "Low"

                # Look up category in dictionary
                cat = "Technical Skills"
                if skill in normalization_agent.skills_dict:
                    cat = normalization_agent.skills_dict[skill].get("category", "Technical Skills")

                missing_skills_data.append({
                    "skill": skill,
                    "frequency_percentage": pct,
                    "target_job_count": total_count,
                    "status": "Missing",
                    "impact": impact,
                    "category": cat
                })

        top_missing = missing_skills_data[:top_n]

        if top_missing:
            top_skill_names = [item["skill"] for item in top_missing[:3]]
            insights_summary = (
                f"Among the {total_jobs} opportunities analyzed in your target domains, "
                f"{', '.join(top_skill_names)} appear most frequently. "
                f"Adding verified project experience with these will unlock higher compatibility scores."
            )
        else:
            insights_summary = (
                f"Your profile currently covers all key technical skills listed across the {total_jobs} analyzed roles!"
            )

        return {
            "target_jobs_analyzed": total_jobs,
            "top_missing_skills": top_missing,
            "insights_summary": insights_summary
        }


skill_gap_agent = SkillGapAgent()
