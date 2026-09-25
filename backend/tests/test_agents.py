import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.agents.job_normalization_agent import normalization_agent
from app.agents.job_deduplication_agent import deduplication_agent
from app.agents.job_classification_agent import classification_agent
from app.agents.skill_extraction_agent import skill_extraction_agent
from app.services.ats.ats_engine import ats_engine
from app.services.matching.matching_engine import matching_engine
from app.agents.skill_gap_agent import skill_gap_agent


def test_skill_normalization():
    assert normalization_agent.normalize_skill("sklearn") == "scikit-learn"
    assert normalization_agent.normalize_skill("js") == "JavaScript"
    assert normalization_agent.normalize_skill("reactjs") == "React"
    assert normalization_agent.normalize_skill("tf") == "TensorFlow"

    skills = ["sklearn", "PYTHON", "react.js", "Docker"]
    normalized = normalization_agent.normalize_skills(skills)
    assert "scikit-learn" in normalized
    assert "Python" in normalized
    assert "React" in normalized
    assert "Docker" in normalized
    print("PASS: test_skill_normalization")


def test_job_deduplication():
    h1 = deduplication_agent.compute_content_hash("ML Engineer", "Acme AI", "San Francisco")
    h2 = deduplication_agent.compute_content_hash("ml engineer", "acme ai", "san francisco")
    assert h1 == h2

    is_dup, ratio = deduplication_agent.is_fuzzy_duplicate(
        new_title="Senior Machine Learning Engineer",
        new_company="Acme AI Corporation",
        new_desc="Working with Python and PyTorch",
        existing_title="Sr. Machine Learning Engineer",
        existing_company="Acme AI Corp",
        existing_desc="Working with Python and PyTorch on algorithms"
    )
    assert is_dup is True
    assert ratio >= 80.0
    print("PASS: test_job_deduplication")


def test_job_classification():
    d1 = classification_agent.classify("Machine Learning Engineer Intern", "Training PyTorch models")
    assert d1 == "Machine Learning"

    d2 = classification_agent.classify("Cloud SRE", "Managing Kubernetes clusters on AWS")
    assert d2 in ["Cloud Computing", "DevOps"]

    d3 = classification_agent.classify("Frontend React Developer", "Building web interfaces in Next.js")
    assert d3 == "Frontend Development"
    print("PASS: test_job_classification")


def test_experience_extraction():
    res1 = skill_extraction_agent.extract_experience("We welcome freshers and final-year students! 0-1 years experience.")
    assert res1["eligible_for_fresher"] is True
    assert res1["experience_min"] == 0.0

    res2 = skill_extraction_agent.extract_experience("Minimum 3-5 years of industry experience required.")
    assert res2["eligible_for_fresher"] is False
    assert res2["experience_min"] == 3.0
    assert res2["experience_max"] == 5.0
    print("PASS: test_experience_extraction")


def test_ats_engine():
    res = ats_engine.evaluate(
        raw_text="Jane Doe\njane@example.com\n555-123-4567\nhttps://github.com/janedoe\n\nSummary:\nMachine Learning Engineer with hands-on experience.\n\nSkills:\nPython, PyTorch, SQL, Pandas, NumPy, scikit-learn, Git, Docker, Linux, C++\n\nExperience:\nBuilt automated model pipeline that improved inference speed by 35% across 50k users.\n\nEducation:\nB.Tech in Artificial Intelligence\n\nProjects:\nObject detection model with 92% accuracy.",
        sections={"summary": "Machine Learning Engineer", "skills": "Python, PyTorch", "experience": "Built pipeline", "education": "B.Tech AI", "projects": "Object detection"},
        detected_skills=["Python", "PyTorch", "SQL", "Pandas", "NumPy", "scikit-learn", "Git", "Docker", "Linux", "C++"],
        detected_projects=[{"title": "Object detection", "description": "92% accuracy"}],
        detected_experience=[{"role": "ML Intern", "description": "Improved inference by 35%"}],
        contact_info={"email": "jane@example.com", "phone": "555-123-4567", "github": "https://github.com/janedoe", "linkedin": None, "portfolio": None},
        achievements=["improved inference speed by 35% across 50k users", "92% accuracy"],
        target_roles=["Machine Learning Engineer"]
    )
    assert res["ats_score"] >= 75.0
    assert len(res["strengths"]) >= 3
    assert res["contact_score"] == 5.0
    print(f"PASS: test_ats_engine (Score: {res['ats_score']}/100)")


def test_matching_engine():
    candidate = {
        "skills": ["Python", "scikit-learn", "SQL", "Pandas", "NumPy"],
        "preferred_roles": ["Machine Learning Engineer", "Data Scientist"],
        "domains": ["Machine Learning", "Data Science"],
        "career_level": "fresher",
        "education": [{"degree": "B.Tech", "specialization": "Artificial Intelligence"}],
        "preferred_locations": ["San Francisco, CA"],
        "work_mode": ["Remote", "Hybrid"]
    }

    job_high = {
        "title": "Machine Learning Engineer Intern",
        "company": "DeepPulse AI",
        "location": "San Francisco, CA",
        "work_mode": "Remote",
        "employment_type": "Internship",
        "domain": "Machine Learning",
        "required_skills": ["Python", "scikit-learn", "SQL"],
        "preferred_skills": ["Docker", "Pandas"],
        "all_skills": ["Python", "scikit-learn", "SQL", "Docker", "Pandas"],
        "eligible_for_fresher": True,
        "experience_min": 0.0,
        "experience_max": 1.0,
        "education_text": "B.Tech in CS or AI",
        "description": "Develop ML algorithms"
    }

    match_res = matching_engine.calculate_match(candidate, job_high)
    assert match_res["match_score"] >= 80.0
    assert "Python" in match_res["matched_skills"]
    assert "SQL" in match_res["matched_skills"]
    assert match_res["compatibility_level"] in ["Excellent Match", "Strong Match"]
    print(f"PASS: test_matching_engine (Match Score: {match_res['match_score']}%, Level: {match_res['compatibility_level']})")


def test_skill_gap_analysis():
    candidate_skills = ["Python", "SQL"]
    target_jobs = [
        {"required_skills": ["Python", "Docker", "AWS"], "preferred_skills": ["Kubernetes"], "domain": "Cloud", "title": "DevOps"},
        {"required_skills": ["Python", "Docker"], "preferred_skills": ["AWS"], "domain": "Cloud", "title": "Backend"},
        {"required_skills": ["Python", "Docker", "FastAPI"], "preferred_skills": [], "domain": "Cloud", "title": "Engineer"}
    ]
    gaps = skill_gap_agent.analyze_skill_gaps(candidate_skills, target_jobs)
    assert gaps["target_jobs_analyzed"] == 3
    top_skill = gaps["top_missing_skills"][0]
    assert top_skill["skill"] == "Docker"
    assert top_skill["frequency_percentage"] == 100.0
    assert top_skill["impact"] == "High"
    print("PASS: test_skill_gap_analysis")


if __name__ == "__main__":
    test_skill_normalization()
    test_job_deduplication()
    test_job_classification()
    test_experience_extraction()
    test_ats_engine()
    test_matching_engine()
    test_skill_gap_analysis()
    print("ALL 7 AGENT & ENGINE TESTS PASSED PERFECTLY!")
