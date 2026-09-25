import asyncio
import hashlib
from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from app.db.session import AsyncSessionLocal, init_db
from app.models.all_models import Job, JobSource
from app.agents.job_normalization_agent import normalization_agent
from app.agents.job_classification_agent import classification_agent
from app.ingestion.source_registry import source_registry

DEMO_JOBS = [
    {
        "source_id": "demo_seed",
        "source_job_id": "demo-ml-01",
        "title": "Machine Learning Engineer Intern",
        "company": "DeepPulse AI",
        "location": "San Francisco, CA",
        "country": "US",
        "work_mode": "Remote",
        "employment_type": "Internship",
        "domain": "Machine Learning",
        "required_skills": ["Python", "scikit-learn", "Machine Learning", "SQL", "Pandas"],
        "preferred_skills": ["Docker", "PyTorch", "Git"],
        "experience_text": "0-1 years / Freshers welcome",
        "experience_min": 0.0,
        "experience_max": 1.0,
        "eligible_for_fresher": True,
        "education_text": "B.Tech/B.E. or B.S. in Computer Science, Artificial Intelligence, Data Science or related",
        "salary_min": 80000,
        "salary_max": 105000,
        "salary_currency": "USD",
        "source_url": "https://example.com/jobs/deeppulse-ml-intern",
        "apply_url": "https://example.com/apply/deeppulse-ml-intern",
        "description": "DeepPulse AI is seeking an ambitious Machine Learning Engineer Intern to contribute to our core predictive modeling and algorithmic pipeline. You will collaborate with research engineers to train models using Python, scikit-learn, and Pandas, evaluate performance metrics, and optimize feature engineering with SQL queries.",
        "requirements": "Hands-on proficiency in Python, scikit-learn, SQL, and data analysis with Pandas/NumPy. Solid understanding of regression, classification, and neural network foundations. Fresh graduates and final-year students strongly encouraged to apply.",
        "responsibilities": "Train and evaluate baseline ML models, write modular Python scripts, collaborate on experimental design, and present evaluation metrics to the engineering team.",
        "days_ago": 0,
        "hours_ago": 3
    },
    {
        "source_id": "greenhouse",
        "source_job_id": "demo-ai-02",
        "title": "Associate AI Engineer",
        "company": "CognitiveSphere",
        "location": "New York, NY",
        "country": "US",
        "work_mode": "Hybrid",
        "employment_type": "Full-time",
        "domain": "Artificial Intelligence",
        "required_skills": ["Python", "TensorFlow", "SQL", "Git", "NumPy"],
        "preferred_skills": ["Natural Language Processing", "Large Language Models", "FastAPI"],
        "experience_text": "Entry-level / 0-2 years",
        "experience_min": 0.0,
        "experience_max": 2.0,
        "eligible_for_fresher": True,
        "education_text": "B.Tech or Master's in AI, CS, or Mathematics",
        "salary_min": 95000,
        "salary_max": 120000,
        "salary_currency": "USD",
        "source_url": "https://boards.greenhouse.io/cognitivesphere/jobs/50123",
        "apply_url": "https://boards.greenhouse.io/cognitivesphere/jobs/50123#apply",
        "description": "CognitiveSphere is building next-generation agentic AI workflows. We are looking for an Associate AI Engineer with strong fundamentals in Python, TensorFlow, and SQL. You will build and test evaluation benchmarks, assist with fine-tuning, and integrate models into production services.",
        "requirements": "Proficiency in Python and numerical computing (NumPy). Experience with deep learning frameworks such as TensorFlow or PyTorch. Knowledge of LLMs and prompt engineering is a significant plus.",
        "responsibilities": "Develop model evaluation pipelines, optimize inference latency, and coordinate with backend engineering on API integrations.",
        "days_ago": 1,
        "hours_ago": 8
    },
    {
        "source_id": "adzuna",
        "source_job_id": "demo-ds-03",
        "title": "Junior Data Scientist",
        "company": "Metrix Data Labs",
        "location": "Austin, TX",
        "country": "US",
        "work_mode": "Remote",
        "employment_type": "Full-time",
        "domain": "Data Science",
        "required_skills": ["Python", "Pandas", "NumPy", "SQL", "scikit-learn"],
        "preferred_skills": ["Tableau", "AWS", "Communication"],
        "experience_text": "0-1 years / Fresh graduates welcome",
        "experience_min": 0.0,
        "experience_max": 1.0,
        "eligible_for_fresher": True,
        "education_text": "Degree in Data Science, Statistics, Computer Science, or Engineering",
        "salary_min": 85000,
        "salary_max": 110000,
        "salary_currency": "USD",
        "source_url": "https://www.adzuna.com/land/ad/3891283",
        "apply_url": "https://www.adzuna.com/land/ad/3891283",
        "description": "Metrix Data Labs helps enterprises make data-driven decisions. As a Junior Data Scientist, you will extract insights from complex transactional datasets using Python and SQL, develop predictive customer retention models with scikit-learn, and create executive-ready visualizations.",
        "requirements": "Strong Python data manipulation skills (Pandas/NumPy). Relational database mastery with SQL. Familiarity with exploratory data analysis and hypothesis testing.",
        "responsibilities": "Perform exploratory analysis, build statistical models, write clear technical documentation, and collaborate with business stakeholders.",
        "days_ago": 2,
        "hours_ago": 14
    },
    {
        "source_id": "lever",
        "source_job_id": "demo-py-04",
        "title": "Python Backend Developer",
        "company": "Nexus Systems",
        "location": "Seattle, WA",
        "country": "US",
        "work_mode": "Remote",
        "employment_type": "Full-time",
        "domain": "Backend Development",
        "required_skills": ["Python", "FastAPI", "SQL", "PostgreSQL", "Git"],
        "preferred_skills": ["Docker", "Redis", "CI/CD"],
        "experience_text": "1-3 years experience",
        "experience_min": 1.0,
        "experience_max": 3.0,
        "eligible_for_fresher": False,
        "education_text": "B.S. in Computer Science or equivalent practical experience",
        "salary_min": 105000,
        "salary_max": 135000,
        "salary_currency": "USD",
        "source_url": "https://jobs.lever.co/nexus/4891b2",
        "apply_url": "https://jobs.lever.co/nexus/4891b2/apply",
        "description": "Nexus Systems is scaling our distributed cloud backend. We are seeking a dedicated Python Backend Developer to design high-throughput REST APIs using FastAPI and PostgreSQL. You will optimize database queries and build resilient microservices.",
        "requirements": "Solid experience writing clean, async Python code. Proficiency with FastAPI or Django and relational databases (PostgreSQL). Familiarity with containerization (Docker) and version control.",
        "responsibilities": "Design, build, and maintain efficient REST APIs. Write unit and integration tests. Ensure low latency and high availability.",
        "days_ago": 3,
        "hours_ago": 20
    },
    {
        "source_id": "the_muse",
        "source_job_id": "demo-cloud-05",
        "title": "Cloud Platform Engineer",
        "company": "Aura Cloud Networks",
        "location": "Chicago, IL",
        "country": "US",
        "work_mode": "Hybrid",
        "employment_type": "Full-time",
        "domain": "Cloud Computing",
        "required_skills": ["AWS", "Docker", "Kubernetes", "Linux", "CI/CD"],
        "preferred_skills": ["Python", "Terraform", "Go"],
        "experience_text": "2-4 years experience",
        "experience_min": 2.0,
        "experience_max": 4.0,
        "eligible_for_fresher": False,
        "education_text": "Bachelor's in Information Technology or Computer Science",
        "salary_min": 120000,
        "salary_max": 150000,
        "salary_currency": "USD",
        "source_url": "https://www.themuse.com/jobs/auracloud/cloud-platform-engineer",
        "apply_url": "https://www.themuse.com/jobs/auracloud/cloud-platform-engineer#apply",
        "description": "Aura Cloud Networks powers infrastructure for global fintech. We require a Cloud Platform Engineer to orchestrate AWS infrastructure, manage Kubernetes clusters, and automate deployment pipelines using GitHub Actions and Terraform.",
        "requirements": "Hands-on experience with AWS services (EC2, S3, IAM, EKS), Docker containerization, and Kubernetes cluster management. Scripting ability in Linux/Bash or Python.",
        "responsibilities": "Automate infrastructure provisioning, maintain CI/CD pipelines, monitor cluster uptime, and improve security postures.",
        "days_ago": 4,
        "hours_ago": 5
    },
    {
        "source_id": "demo_seed",
        "source_job_id": "demo-fs-06",
        "title": "Full Stack Software Engineer",
        "company": "Vanguard Tech",
        "location": "Boston, MA",
        "country": "US",
        "work_mode": "Remote",
        "employment_type": "Full-time",
        "domain": "Full Stack Development",
        "required_skills": ["React", "TypeScript", "Node.js", "SQL", "Tailwind CSS"],
        "preferred_skills": ["Next.js", "PostgreSQL", "Docker"],
        "experience_text": "0-2 years experience",
        "experience_min": 0.0,
        "experience_max": 2.0,
        "eligible_for_fresher": True,
        "education_text": "Degree in Computer Science, Software Engineering or bootcamp equivalent",
        "salary_min": 90000,
        "salary_max": 120000,
        "salary_currency": "USD",
        "source_url": "https://example.com/jobs/vanguard-fullstack",
        "apply_url": "https://example.com/apply/vanguard-fullstack",
        "description": "Vanguard Tech creates intuitive SaaS products for modern teams. We need a Full Stack Engineer to build responsive web interfaces in React/TypeScript and scalable server endpoints in Node.js and SQL.",
        "requirements": "Strong proficiency in modern JavaScript/TypeScript, React hooks, and component architecture. Experience with Node.js backend development and SQL databases.",
        "responsibilities": "Deliver end-to-end features from UI components to database schemas. Collaborate with designers and product managers on seamless UX.",
        "days_ago": 1,
        "hours_ago": 12
    },
    {
        "source_id": "demo_seed",
        "source_job_id": "demo-sec-07",
        "title": "Junior Cybersecurity Analyst",
        "company": "Fortress Shield",
        "location": "Reston, VA",
        "country": "US",
        "work_mode": "On-site",
        "employment_type": "Full-time",
        "domain": "Cybersecurity",
        "required_skills": ["Linux", "Python", "Problem Solving", "Networking"],
        "preferred_skills": ["Communication", "CI/CD"],
        "experience_text": "0-1 years / Entry-level",
        "experience_min": 0.0,
        "experience_max": 1.0,
        "eligible_for_fresher": True,
        "education_text": "Degree in Cybersecurity, Computer Science, or Network Engineering",
        "salary_min": 75000,
        "salary_max": 95000,
        "salary_currency": "USD",
        "source_url": "https://example.com/jobs/fortress-cyber-analyst",
        "apply_url": "https://example.com/apply/fortress-cyber-analyst",
        "description": "Monitor and safeguard critical network infrastructure. Investigate vulnerability reports, write Python automation scripts for log analysis, and collaborate with incident response teams.",
        "requirements": "Strong foundation in TCP/IP, Linux command line, and Python scripting. High attention to detail.",
        "responsibilities": "Triage security alerts, analyze packet captures, document threat patterns, and configure defensive rules.",
        "days_ago": 3,
        "hours_ago": 2
    },
    {
        "source_id": "ashby",
        "source_job_id": "demo-fe-08",
        "title": "Frontend React Developer",
        "company": "PixelCraft Studios",
        "location": "Los Angeles, CA",
        "country": "US",
        "work_mode": "Remote",
        "employment_type": "Full-time",
        "domain": "Frontend Development",
        "required_skills": ["React", "JavaScript", "HTML", "CSS", "Tailwind CSS"],
        "preferred_skills": ["TypeScript", "Next.js", "Git"],
        "experience_text": "0-2 years",
        "experience_min": 0.0,
        "experience_max": 2.0,
        "eligible_for_fresher": True,
        "education_text": "B.Tech/B.S. in CS or related field",
        "salary_min": 85000,
        "salary_max": 115000,
        "salary_currency": "USD",
        "source_url": "https://jobs.ashbyhq.com/pixelcraft/1029",
        "apply_url": "https://jobs.ashbyhq.com/pixelcraft/1029/apply",
        "description": "PixelCraft Studios develops creative software for digital artists. We are looking for a Frontend Developer with passion for micro-interactions, responsive CSS layouts, and clean React code.",
        "requirements": "Expertise in React, modern JavaScript, Tailwind CSS, and web performance optimization.",
        "responsibilities": "Implement sleek UI components, optimize client bundle size, and build delightful animations.",
        "days_ago": 0,
        "hours_ago": 6
    }
]


async def seed_database():
    """Idempotently seeds job sources and diverse demo opportunities."""
    await init_db()

    async with AsyncSessionLocal() as session:
        # 1. Seed job sources
        sources_meta = source_registry.list_all_sources()
        for meta in sources_meta:
            stmt = select(JobSource).where(JobSource.id == meta["id"])
            res = await session.execute(stmt)
            existing_source = res.scalar_one_or_none()
            if not existing_source:
                new_source = JobSource(
                    id=meta["id"],
                    name=meta["name"],
                    source_type=meta["source_type"],
                    enabled=meta["enabled"],
                    requires_api_key=meta["requires_api_key"],
                    supports_live_fetch=meta["supports_live_fetch"],
                    supports_search=meta["supports_search"],
                    supports_pagination=meta["supports_pagination"],
                    attribution_required=meta["attribution_required"],
                    terms_url=meta["terms_url"],
                    region=meta["region"],
                    job_count=0
                )
                session.add(new_source)

        await session.commit()

        # 2. Seed jobs
        now = datetime.now(timezone.utc)
        jobs_added = 0

        for item in DEMO_JOBS:
            clean_title = normalization_agent.normalize_title(item["title"])
            clean_company = item["company"]
            clean_location = item["location"]
            content_hash = hashlib.sha256(
                f"{clean_title.lower()}:{clean_company.lower()}:{clean_location.lower()}".encode("utf-8")
            ).hexdigest()

            stmt = select(Job).where(Job.content_hash == content_hash)
            res = await session.execute(stmt)
            existing_job = res.scalar_one_or_none()

            if not existing_job:
                pub_time = now - timedelta(days=item.get("days_ago", 0), hours=item.get("hours_ago", 0))
                req_skills = normalization_agent.normalize_skills(item.get("required_skills", []))
                pref_skills = normalization_agent.normalize_skills(item.get("preferred_skills", []))
                all_skills = list(dict.fromkeys(req_skills + pref_skills))

                job = Job(
                    source_id=item["source_id"],
                    source_job_id=item["source_job_id"],
                    title=clean_title,
                    company=clean_company,
                    location=clean_location,
                    country=item.get("country", "US"),
                    work_mode=item.get("work_mode", "Remote"),
                    employment_type=item.get("employment_type", "Full-time"),
                    description=item["description"],
                    requirements=item.get("requirements", ""),
                    responsibilities=item.get("responsibilities", ""),
                    required_skills=req_skills,
                    preferred_skills=pref_skills,
                    all_skills=all_skills,
                    experience_text=item.get("experience_text", "0-1 years"),
                    experience_min=item.get("experience_min", 0.0),
                    experience_max=item.get("experience_max", 1.0),
                    eligible_for_fresher=item.get("eligible_for_fresher", True),
                    education_text=item.get("education_text", "Bachelor's degree"),
                    domain=item.get("domain", "Other"),
                    salary_min=item.get("salary_min"),
                    salary_max=item.get("salary_max"),
                    salary_currency=item.get("salary_currency", "USD"),
                    source_url=item["source_url"],
                    apply_url=item["apply_url"],
                    published_at=pub_time,
                    updated_at=pub_time,
                    collected_at=now,
                    verified_at=now,
                    status="ACTIVE",
                    content_hash=content_hash,
                )
                session.add(job)
                jobs_added += 1

        await session.commit()
        print(f"Successfully seeded database! Added {jobs_added} opportunities.")


if __name__ == "__main__":
    asyncio.run(seed_database())
