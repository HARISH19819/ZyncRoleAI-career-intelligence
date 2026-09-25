from typing import List, Dict, Any
from collections import Counter
from app.agents.job_normalization_agent import normalization_agent


class CareerIntelligenceAgent:
    """Agent 11: Extracts factual market analytics, domain demand, and role insights from collected job data."""

    def compute_market_insights(
        self,
        jobs: List[Dict[str, Any]],
        candidate_skills: List[str],
        user_domains: List[str]
    ) -> Dict[str, Any]:
        """Calculates authentic market aggregates and candidate skill coverage."""
        total_jobs = len(jobs)
        if total_jobs == 0:
            return {
                "total_jobs": 0,
                "selected_domain_jobs": 0,
                "top_skills": [],
                "top_roles": [],
                "domain_distribution": [],
                "work_mode_distribution": [],
                "fresher_friendly_percentage": 0.0,
                "location_trends": [],
                "user_skill_coverage_summary": "No market jobs collected yet."
            }

        # Filter domain jobs
        domain_jobs = [
            j for j in jobs
            if not user_domains or any(d.lower() == j.get("domain", "").lower() for d in user_domains)
        ]
        analyzed_jobs = domain_jobs if domain_jobs else jobs
        analyzed_count = len(analyzed_jobs)

        skill_counter = Counter()
        role_counter = Counter()
        domain_counter = Counter()
        work_mode_counter = Counter()
        location_counter = Counter()
        fresher_count = 0

        for j in analyzed_jobs:
            # Skills
            for s in j.get("all_skills", []) or j.get("required_skills", []):
                norm = normalization_agent.normalize_skill(s)
                skill_counter[norm] += 1

            # Roles (cleaned title)
            clean_title = normalization_agent.normalize_title(j.get("title", ""))
            role_counter[clean_title] += 1

            # Domains
            domain_counter[j.get("domain", "Other")] += 1

            # Work mode
            work_mode_counter[j.get("work_mode", "On-site")] += 1

            # Location
            loc = j.get("location", "Unknown").split(",")[0].strip()
            location_counter[loc] += 1

            # Fresher eligibility
            if j.get("eligible_for_fresher", False) or j.get("experience_min", 0.0) <= 1.0:
                fresher_count += 1

        top_skills = [
            {"name": name, "count": count, "percentage": round((count / analyzed_count) * 100.0, 1)}
            for name, count in skill_counter.most_common(10)
        ]

        top_roles = [
            {"name": name, "count": count, "percentage": round((count / analyzed_count) * 100.0, 1)}
            for name, count in role_counter.most_common(8)
        ]

        domain_dist = [
            {"name": name, "count": count, "percentage": round((count / total_jobs) * 100.0, 1)}
            for name, count in domain_counter.most_common(8)
        ]

        work_mode_dist = [
            {"name": name, "count": count, "percentage": round((count / analyzed_count) * 100.0, 1)}
            for name, count in work_mode_counter.most_common(5)
        ]

        location_trends = [
            {"name": name, "count": count, "percentage": round((count / analyzed_count) * 100.0, 1)}
            for name, count in location_counter.most_common(6)
        ]

        fresher_pct = round((fresher_count / analyzed_count) * 100.0, 1)

        # Candidate coverage of top 10 market skills
        cand_set = {s.lower() for s in candidate_skills}
        matched_top_skills = [s["name"] for s in top_skills if s["name"].lower() in cand_set]
        coverage_count = len(matched_top_skills)
        total_top_skills = len(top_skills)

        if total_top_skills > 0:
            coverage_summary = (
                f"You have {coverage_count} of the {total_top_skills} most requested skills in this domain "
                f"({', '.join(matched_top_skills[:3]) if matched_top_skills else 'None yet'})."
            )
        else:
            coverage_summary = "Collecting skills demand from recent opportunities."

        return {
            "total_jobs": total_jobs,
            "selected_domain_jobs": analyzed_count,
            "top_skills": top_skills,
            "top_roles": top_roles,
            "domain_distribution": domain_dist,
            "work_mode_distribution": work_mode_dist,
            "fresher_friendly_percentage": fresher_pct,
            "location_trends": location_trends,
            "user_skill_coverage_summary": coverage_summary
        }

    def inspect_role(self, role_name: str, jobs: List[Dict[str, Any]], candidate_skills: List[str]) -> Dict[str, Any]:
        """Provides detailed demand intelligence for a single target role or domain."""
        matching_jobs = [
            j for j in jobs
            if role_name.lower() in j.get("title", "").lower() or role_name.lower() == j.get("domain", "").lower()
        ]
        return self.compute_market_insights(matching_jobs, candidate_skills, [role_name])


career_intelligence_agent = CareerIntelligenceAgent()
