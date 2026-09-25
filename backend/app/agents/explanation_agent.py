from typing import List, Dict, Any


class ExplanationAgent:
    """Agent 9: Generates human, constructive, and fact-grounded explanations from computed match facts."""

    def generate_explanation(
        self,
        match_score: float,
        job_title: str,
        company: str,
        matched_skills: List[str],
        missing_required: List[str],
        missing_preferred: List[str],
        eligible_for_fresher: bool,
        candidate_level: str,
        domain_match: bool,
        location_match: bool,
        work_mode: str
    ) -> Dict[str, Any]:
        """Produces clear, constructive text for why the job matches or has gaps."""
        strengths = []
        concerns = []

        if matched_skills:
            top_matched = ", ".join(matched_skills[:4])
            strengths.append(f"Strong overlap with your core skills: {top_matched}")

        if domain_match:
            strengths.append("Directly aligns with your targeted career domain")

        if eligible_for_fresher and candidate_level in ["fresher", "student", "entry-level"]:
            strengths.append("Fresher & entry-level candidates are explicitly welcomed for this position")

        if location_match:
            strengths.append(f"Matches your work preference ({work_mode})")

        # Concerns / gaps
        if missing_required:
            missing_req_str = ", ".join(missing_required[:3])
            concerns.append(f"Required skills not yet detected in your profile: {missing_req_str}")

        if missing_preferred:
            missing_pref_str = ", ".join(missing_preferred[:3])
            concerns.append(f"Preferred/bonus skills: {missing_pref_str}")

        # Construct primary narrative summary
        if match_score >= 85:
            matched_text = f" because the role requires {', '.join(matched_skills[:3])}, which are well demonstrated in your profile" if matched_skills else ""
            summary = (
                f"Strong compatibility with {company}'s {job_title}{matched_text}. "
                f"The position aligns closely with your domain interests and background."
            )
        elif match_score >= 70:
            matched_text = f"matches key requirements in {', '.join(matched_skills[:3])}" if matched_skills else "aligns with your primary interests"
            gap_text = f", though the listing highlights {', '.join(missing_required[:2])}" if missing_required else ""
            summary = (
                f"Solid match for this role. Your profile {matched_text}{gap_text}."
            )
        elif match_score >= 50:
            gap_text = f" such as {', '.join(missing_required[:2])}" if missing_required else ""
            summary = (
                f"Partial compatibility with this role. Your foundation is relevant, but the listing specifies additional criteria{gap_text}."
            )
        else:
            summary = (
                f"Lower match score. This opportunity requires skills or specialized experience outside your primary focus areas."
            )

        # Actionable recommendations on how to improve this match
        how_to_improve = []
        if missing_required:
            how_to_improve.append(f"Highlight or acquire experience with {missing_required[0]}")
        if missing_preferred:
            how_to_improve.append(f"Add projects demonstrating {missing_preferred[0]}")
        if not strengths:
            how_to_improve.append("Update your resume summary with target role keywords")
        how_to_improve_text = " • ".join(how_to_improve) if how_to_improve else "Your profile currently meets all primary listed requirements for this position."

        return {
            "summary": summary,
            "strengths": strengths,
            "concerns": concerns,
            "how_to_improve": how_to_improve_text
        }


explanation_agent = ExplanationAgent()
