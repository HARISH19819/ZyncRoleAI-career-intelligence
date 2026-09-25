import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.session import init_db


@pytest.fixture(autouse=True)
async def init_test_db():
    await init_db()



async def test_health_and_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r_root = await ac.get("/")
        assert r_root.status_code == 200
        assert r_root.json()["product"] == "ZyncRole AI"
        print("PASS: test_health_and_root -> root ok")

        r_health = await ac.get("/health")
        assert r_health.status_code == 200
        assert r_health.json()["status"] in ["healthy", "degraded"]
        print("PASS: test_health_and_root -> health ok")


async def test_auth_and_profile_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        email = f"alex_morgan_{os.getpid()}@example.com"
        # Register
        r_reg = await ac.post("/auth/register", json={
            "first_name": "Alex",
            "last_name": "Morgan",
            "email": email,
            "password": "Password123!"
        })
        assert r_reg.status_code == 200
        token = r_reg.json()["access_token"]
        print("PASS: test_auth_and_profile_flow -> registration ok")

        headers = {"Authorization": f"Bearer {token}"}

        # Get profile
        r_prof = await ac.get("/users/profile", headers=headers)
        assert r_prof.status_code == 200
        assert r_prof.json()["first_name"] == "Alex"
        print("PASS: test_auth_and_profile_flow -> get_profile ok")

        # Onboarding
        r_onboard = await ac.post("/users/onboarding", json={
            "education": {
                "degree": "B.Tech",
                "specialization": "Artificial Intelligence",
                "college": "State University",
                "graduation_year": 2026,
                "current_status": "Fresher"
            },
            "interests": {
                "desired_roles": ["Machine Learning Engineer", "AI Developer"],
                "domains": ["Machine Learning", "Artificial Intelligence"],
                "experience_level": "fresher",
                "job_type": "Full-time"
            },
            "preferences": {
                "location": "San Francisco, CA",
                "work_mode": ["Remote", "Hybrid"],
                "salary_preference": 90000,
                "employment_preference": "Full-time"
            },
            "skills": {
                "technical_skills": ["Python", "SQL", "scikit-learn"],
                "tools": ["Git"],
                "frameworks": ["Pandas", "NumPy"],
                "soft_skills": ["Problem Solving"]
            }
        }, headers=headers)
        assert r_onboard.status_code == 200
        print("PASS: test_auth_and_profile_flow -> onboarding ok")

        # Dashboard
        r_dash = await ac.get("/dashboard", headers=headers)
        assert r_dash.status_code == 200
        dash_data = r_dash.json()
        assert "recommended_jobs" in dash_data
        assert len(dash_data["recommended_jobs"]) > 0
        print(f"PASS: test_auth_and_profile_flow -> dashboard ok ({len(dash_data['recommended_jobs'])} recommended jobs)")

        # Verify job explorer
        r_jobs = await ac.get("/jobs", headers=headers)
        assert r_jobs.status_code == 200
        jobs_list = r_jobs.json()
        assert len(jobs_list) > 0
        job_id = jobs_list[0]["id"]
        print(f"PASS: test_auth_and_profile_flow -> jobs explorer ok ({len(jobs_list)} active jobs)")

        # Job detail
        r_detail = await ac.get(f"/jobs/{job_id}", headers=headers)
        assert r_detail.status_code == 200
        print(f"PASS: test_auth_and_profile_flow -> job detail ok ({r_detail.json()['title']})")

        # Job match explanation
        r_match = await ac.get(f"/jobs/{job_id}/match", headers=headers)
        assert r_match.status_code == 200
        match_expl = r_match.json()
        assert "match_score" in match_expl
        assert "breakdown" in match_expl
        print(f"PASS: test_auth_and_profile_flow -> match explanation ok ({match_expl['match_score']}% {match_expl['compatibility_level']})")

        # Save job
        r_save = await ac.post(f"/saved/{job_id}", headers=headers)
        assert r_save.status_code == 200
        assert r_save.json()["is_saved"] is True
        print("PASS: test_auth_and_profile_flow -> save job ok")

        # Track application
        r_app = await ac.post("/applications", json={"job_id": job_id, "status": "Applied"}, headers=headers)
        assert r_app.status_code == 200
        assert r_app.json()["status"] == "Applied"
        print("PASS: test_auth_and_profile_flow -> track application ok")

        # Skill gaps
        r_gaps = await ac.get("/skill-gaps", headers=headers)
        assert r_gaps.status_code == 200
        print(f"PASS: test_auth_and_profile_flow -> skill gaps ok ({len(r_gaps.json()['top_missing_skills'])} recurring gaps identified)")

        # Career insights
        r_career = await ac.get("/career/insights", headers=headers)
        assert r_career.status_code == 200
        assert "top_skills" in r_career.json()
        print(f"PASS: test_auth_and_profile_flow -> career insights ok ({len(r_career.json()['top_skills'])} market skills analyzed)")


async def main():
    await test_health_and_root()
    await test_auth_and_profile_flow()
    print("\nALL API INTEGRATION TESTS PASSED PERFECTLY!")


if __name__ == "__main__":
    asyncio.run(main())
