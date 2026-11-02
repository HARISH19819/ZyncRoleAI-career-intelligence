# ⚡ ZyncRole AI

<div align="center">

# 🌐 ZyncRole AI
### *"One Resume. Every Opportunity. One Intelligent Career Feed."*

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-carrer--feed--ai--frontend.onrender.com-00C7B7?style=for-the-badge&logo=render&logoColor=white)](https://carrer-feed-ai-frontend.onrender.com)
[![GitHub Repository](https://img.shields.io/badge/GitHub-ZyncRoleAI--career--intelligence-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/HARISH19819/ZyncRoleAI-career-intelligence)

<br/>

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19.2-61DAFB.svg?style=flat-square&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6.svg?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg?style=flat-square&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL_15_+_pgvector-3ECF8E.svg?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com/)
[![Gemini](https://img.shields.io/badge/AI-Google_Gemini_Embedding_2-4285F4.svg?style=flat-square&logo=google-gemini&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-F59E0B.svg?style=flat-square)](https://opensource.org/licenses/MIT)

<br/>

> **An autonomous AI career intelligence and personalized job matching platform.**  
> *Deterministic 8-Dimension Compatibility Engine • 7-Dimension ATS Diagnostics • Real-Time Market Skill Gaps • 100% Free-Tier Cloud Architecture.*

[**Explore Live Application ↗**](https://carrer-feed-ai-frontend.onrender.com) • [**Slide Deck (.pptx)**](ZyncRole_AI_Presentation.pptx) • [**Instant Demo Login**](#-1-click-instant-demo-evaluation) • [**System Architecture**](#-system-architecture--technical-workflow)

</div>

---

## 🔗 Live Deployed Links

| Resource | URL | Status | Details |
|:---|:---|:---:|:---|
| **Live Web App** | [https://carrer-feed-ai-frontend.onrender.com](https://carrer-feed-ai-frontend.onrender.com) | 🟢 **Active** | Production deployment on Render |
| **GitHub Repo** | [HARISH19819/ZyncRoleAI-career-intelligence](https://github.com/HARISH19819/ZyncRoleAI-career-intelligence) | 🟢 **Main** | Source code & full history |
| **Slide Deck** | [`ZyncRole_AI_Presentation.pptx`](ZyncRole_AI_Presentation.pptx) | 📄 **Included** | 8-slide executive pitch presentation |

---

## 🌟 About The Project

Job hunting today is broken, opaque, and deeply exhausting. Candidates submit hundreds of resumes into corporate Applicant Tracking Systems (ATS) only to disappear into a "black hole" without ever knowing why they were rejected or what skills they lacked. Meanwhile, job listings are fragmented across dozens of disconnected websites, and AI job recommendation tools frequently hallucinate fit scores without any mathematical justification.

**ZyncRole AI** transforms job hunting into an **autonomous, transparent, and mathematically grounded career intelligence experience**:

### ⚔️ Legacy Job Portals vs. ZyncRole AI

| Feature | Legacy Job Boards (LinkedIn, Indeed) | Typical "AI" Job Apps | ⚡ ZyncRole AI |
|:---|:---|:---|:---|
| **Opportunity Sourcing** | Fragmented across 20+ isolated silos | Unregulated scraping that breaks | **Ethical APIs + Public ATS (Greenhouse, Lever, Ashby)** |
| **Matching Engine** | Primitive keyword search | Hallucinated black-box LLM guesses | **Deterministic 8-Dimension Formula ($0\text{–}100\%$)** |
| **Match Transparency** | *"You might be a fit"* (opaque) | Zero explanations | **Exact % contribution breakdown + improvement tips** |
| **ATS Feedback** | None; silent rejection | Generic resume score | **7-Dimension ATS Diagnostic + 1-Click OpenResume CTA** |
| **Skill Gap Guidance** | None | Generic suggestions | **Aggregated market demand (High/Med/Low impact)** |
| **Recruitment Tracking** | Manual spreadsheets | None | **Integrated Kanban Pipeline with follow-up dates** |
| **Operational Cost** | High enterprise subscription | Expensive LLM tokens per search | **100% Free-Tier ($0) Cloud Architecture** |

---

## 🎯 The 8-Dimension Compatibility Formula

Rather than relying on hallucinated generative AI output, ZyncRole computes compatibility using a **deterministic mathematical formula** $S_{total} \in [0, 100]$:

$$S_{total} = 100 \times \sum_{i=1}^{8} \left( w_i \times s_i \right)$$

*All weights strictly sum to 1.00 and are dynamically verified on application startup.*

```
┌────────────────────────────────────────────────────────────────────────┐
│               8-DIMENSION COMPATIBILITY WEIGHT DISTRIBUTION             │
├──────────────────────────┬────────┬────────────────────────────────────┤
│ Dimension                │ Weight │ Evaluation Methodology             │
├──────────────────────────┼────────┼────────────────────────────────────┤
│ 1. Skill Compatibility   │  30%   │ Canonical Jaccard (75% req / 25% pref)│
│ 2. Role Alignment        │  15%   │ RapidFuzz Token Set Ratio          │
│ 3. Domain Alignment      │  10%   │ 20+ Domain Cluster Mapping         │
│ 4. Experience Level      │  10%   │ Fresher-friendly heuristic parser  │
│ 5. Education Fit         │   5%   │ Degree & tech specialization match │
│ 6. Location & Mobility   │  10%   │ Remote tolerance & geo scoring     │
│ 7. Preferences Fit       │   5%   │ Work mode & salary compliance      │
│ 8. Semantic Embeddings   │  15%   │ Gemini Embedding 2 Cosine Vector   │
└──────────────────────────┴────────┴────────────────────────────────────┘
```

---

## 🏗️ System Architecture & Technical Workflow

### End-to-End System Pipeline

```mermaid
flowchart TD
    subgraph ClientLayer ["Client Application (React 19 + TypeScript + Vite)"]
        UI["Tailwind CSS + Recharts UI"]
        TQ["TanStack Query (Async Caching)"]
        Router["React Router DOM v7"]
    end

    subgraph Gateway ["FastAPI 0.115 Application Gateway"]
        Auth["PyJWT + Bcrypt Auth"]
        RateLimit["CORS & Request Validation"]
        Routes["Async REST API Endpoints"]
    end

    subgraph AutonomousAgents ["Autonomous AI & ML Agents"]
        Ingest["Job Ingestion Agent<br/>(Greenhouse, Lever, Ashby, Remotive, Adzuna)"]
        Dedup["Deduplication Agent<br/>(SHA-256 Fingerprint + RapidFuzz)"]
        Norm["Job Normalization Agent<br/>(Canonical Skills + 20+ Domains)"]
        ATS["7-Dimension ATS Diagnostic Engine<br/>(PyMuPDF + python-docx)"]
        Vector["Dual Vectorizer<br/>(Gemini Embedding 2 + TF-IDF Fallback)"]
        Match["8-Dimension Deterministic Match Engine"]
        Explain["Factual Explanation Agent"]
        Gap["Skill Gap & Market Intelligence Agent"]
    end

    subgraph StorageLayer ["Zero-Cost Storage Layer"]
        DB["Supabase PostgreSQL 15 + pgvector<br/>(Fallback: Local SQLite zyncrole.db)"]
        Uploads["Secure Resume Storage (/uploads)"]
    end

    ClientLayer <-->|HTTPS / REST / JWT| Gateway
    Gateway <--> AutonomousAgents
    AutonomousAgents <--> StorageLayer
    ClientLayer -.->|1-Click External CTA| OpenResume["OpenResume ATS Resume Builder"]
```

### 1. Ethical Job Ingestion & Deduplication Pipeline
```mermaid
sequenceDiagram
    autonumber
    participant Source as ATS & Open APIs (Greenhouse/Lever/Adzuna)
    participant Ingest as Ingestion Service
    participant Dedup as Deduplication Agent
    participant DB as PostgreSQL / SQLite

    Source->>Ingest: Fetch active listings (JSON REST API)
    Ingest->>Ingest: Normalize titles, clean HTML, extract skills & fresher criteria
    Ingest->>Dedup: Generate SHA-256 hash (title + company + location)
    Dedup->>DB: Check exact hash index
    alt Hash exists
        Dedup-->>Ingest: Mark as duplicate (skip insertion)
    else Hash not found
        Dedup->>Dedup: Run RapidFuzz Token Set Ratio against recent active listings
        alt Fuzzy similarity > 85%
            Dedup-->>Ingest: Mark as cross-board duplicate
        else Unique job
            Dedup->>DB: Save normalized job record
        end
    end
```

### 2. Resume Parsing & 7-Dimension ATS Evaluation Flow
```mermaid
sequenceDiagram
    autonumber
    participant User as Candidate
    participant API as Resumes Endpoint
    participant Parser as ResumeParser (PyMuPDF / docx)
    participant ATS as 7-Dimension ATS Engine
    participant Gemini as Gemini Embedding 2
    participant DB as Database

    User->>API: Upload resume (PDF / DOCX / TXT)
    API->>Parser: Extract clean raw text, contact links & sections
    Parser->>ATS: Send text, detected sections, and skills
    ATS->>ATS: Evaluate Keywords (25), Roles (20), Sections (15), Projects (15), Format (10), Achievements (10), Contact (5)
    ATS->>Gemini: Vectorize candidate profile into 768-dim float vector
    Gemini-->>ATS: Dense vector representation (or TF-IDF fallback)
    ATS->>DB: Save ResumeAnalysis & CandidateProfile records
    ATS-->>User: Return ATS readiness score (0-100), strengths, gaps & OpenResume link
```

---

## 🛠️ Complete Tech Stack

<div align="center">

| Layer | Technologies | Purpose |
|:---|:---|:---|
| **Frontend Framework** | **React 19**, TypeScript 5.8, Vite 8.3 | High-performance SPA with modern React compiler & strict typing |
| **Styling & UI** | **Tailwind CSS 3.4**, PostCSS, Autoprefixer, Lucide React | Clean dark-mode utility-first UI and iconography |
| **Data Fetching & State** | **TanStack React Query v5**, React Hook Form, Zod | Optimistic server state management, caching & validation |
| **Visualizations** | **Recharts 3.10** | Interactive 8-dimension match radars, ATS gauge charts & gap bar graphs |
| **Backend Framework** | **FastAPI 0.115**, Python 3.11, Uvicorn 0.32 | Asynchronous high-throughput ASGI web framework |
| **Data Validation** | **Pydantic v2**, Pydantic-Settings | Strict request/response typing and environment config |
| **Database & Vector Store** | **Supabase PostgreSQL 15** + **`pgvector`** | Production relational storage + native 768-dim cosine vector queries |
| **Local Database Fallback** | **SQLite 3** (`zyncrole.db`) + **`aiosqlite`** | 100% zero-cost local operation without external infrastructure |
| **ORM & Database Driver** | **SQLAlchemy 2.0 (Async)**, `asyncpg`, `greenlet` | Full asynchronous database interaction layer |
| **AI & Embeddings** | **Google Gemini Embedding 2** (`gemini-embedding-2`) | 768-dimensional dense vector embeddings for semantic matching |
| **Generative LLM** | **Google Gemini Flash** (`gemini-3.8-flash`) | Deep reasoning, resume insight synthesis & LLM tasks |
| **Fuzzy Matching** | **RapidFuzz 3.10** | C-optimized token matching for job deduplication and role alignment |
| **NLP & Fallback ML** | **Scikit-Learn 1.5**, NumPy, Pandas | TF-IDF text vectorization, Jaccard overlap, matrix math |
| **Document Processing** | **PyMuPDF (fitz)**, `python-docx` | Fast text, table, and metadata extraction from PDF & DOCX resumes |
| **Security & Auth** | **PyJWT**, Passlib, Bcrypt | Stateless JWT authorization and salted password hashing |
| **HTTP Client** | **HTTPX 0.27** | Asynchronous HTTP requests for external job board ingestion |
| **DevOps & Cloud** | **Docker**, Docker Compose, Render, Vercel | Multi-stage container builds and production deployment |

</div>

---

## 💡 Core Features & Capabilities

### 1. ⚡ 1-Click Instant Demo Evaluation
For hackathon judges and evaluators who want to test immediately without signing up:
- One click logs in as **Alex Chen (AI / Machine Learning Engineer)**.
- Pre-loaded with an evaluated resume, complete career preferences, and pre-computed compatibility scores across fresh tech opportunities.

### 2. 📡 Ethical Opportunity Aggregation
- Ingests from **Greenhouse, Lever, Ashby, Remotive, Adzuna, Arbeitnow, and The Muse**.
- Zero scraping; 100% compliant with robots.txt and platform terms of service.
- Multi-tier deduplication prevents duplicate postings across multiple aggregators.

### 3. 🎯 Transparent "Why This Match?" Breakdown
- Every match explains **why** the candidate scored what they scored.
- Highlights:
  - **Strengths:** Explicit skills and experience that matched the job.
  - **Concerns / Gaps:** Missing required or preferred technologies.
  - **Actionable Steps:** Specific suggestions on what to highlight or learn next to boost the match score.

### 4. 📄 7-Dimension ATS Resume Diagnostic
- Analyzes uploaded resumes against 7 key dimensions:
  1. **Keyword Coverage (25%)** — Canonical skill density.
  2. **Role Relevance (20%)** — Target title presence in headlines & experience.
  3. **Section Completeness (15%)** — Summary, Education, Experience, Projects, Skills.
  4. **Project Depth (15%)** — Implementation quality and project showcase.
  5. **Formatting & Readability (10%)** — Paragraph density and symbol validation.
  6. **Quantified Achievements (10%)** — Metrics, percentages, and impact verbs.
  7. **Contact Completeness (5%)** — Email, phone, GitHub, LinkedIn, portfolio links.
- Direct integration with **OpenResume** to help candidates generate clean, ATS-compliant resumes immediately.

### 5. 📊 Real-Time Market Skill Gap Intelligence
- Aggregates recurring missing skills across target opportunities.
- Classifies missing skills by **High, Medium, or Low impact** to guide candidate upskilling efficiently.

### 6. 📋 Integrated Recruitment Pipeline (Kanban & Table)
- Track applications across 5 stages: **Applied ➔ Assessment ➔ Interview ➔ Selected / Offer ➔ Rejected**.
- Store interview notes, salary details, and follow-up dates.

### 7. 🔒 Complete Data Sovereignty & Zero Admin Interface
- **Self-Service Export:** Candidates can export their complete profile, resume text, analyses, and saved jobs as clean JSON in 1 click.
- **Right to Erasure:** Permanent 1-click account and data deletion cascading across all tables.
- **Zero Admin Routes:** Hard product boundary with zero administrative backdoors, dashboards, or privileged accounts.

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.11+**
- **Node.js 20+** and **npm 10+**

### 1. Clone & Configure
```bash
git clone https://github.com/HARISH19819/ZyncRoleAI-career-intelligence.git
cd ZyncRoleAI-career-intelligence

# Copy environment template
cp .env.example .env
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv

# Windows:
.\venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Start backend server (auto-creates tables and seeds demo opportunities)
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
- API Base: `http://localhost:8000`
- Interactive Swagger Docs: `http://localhost:8000/docs`

### 3. Frontend Setup
In a new terminal window:
```bash
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
- Web Application: `http://localhost:5173`

---

## 🐳 Running with Docker Compose

To spin up the entire application containerized:
```bash
docker-compose up --build
```
- **Frontend:** `http://localhost:3000`
- **Backend API:** `http://localhost:8000`
- **Swagger Docs:** `http://localhost:8000/docs`

---

## 🧪 Testing & Verification

Run the comprehensive unit, agent, and API integration test suite:
```bash
pytest backend/tests/ -v
```

Expected output:
```text
tests/test_agents.py::test_skill_normalization PASSED
tests/test_agents.py::test_job_deduplication PASSED
tests/test_agents.py::test_job_classification PASSED
tests/test_agents.py::test_experience_extraction PASSED
tests/test_agents.py::test_ats_engine PASSED
tests/test_agents.py::test_matching_engine PASSED
tests/test_agents.py::test_skill_gap_analysis PASSED
tests/test_api.py::test_health_and_root PASSED
tests/test_api.py::test_auth_and_profile_flow PASSED
========================= 9 passed in ~4s =========================
```

---

## ☁️ Free-Tier Cloud Deployment Guide

ZyncRole AI is specifically engineered to run **100% free of charge** across production cloud tiers:

### 1. Database: Supabase (Free Tier)
1. Create a free project at [supabase.com](https://supabase.com).
2. Run the migration script in Supabase's SQL Editor:  
   [`supabase/migrations/20260325000000_initial_schema.sql`](supabase/migrations/20260325000000_initial_schema.sql)
3. Set your connection string in `.env`:
   ```env
   SUPABASE_DB_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   SUPABASE_URL=https://[PROJECT-REF].supabase.co
   SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
   ```

### 2. Backend: Render / Railway / Fly.io (Free Tier)
- **Build Command:** `pip install -r backend/requirements.txt`
- **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 3. Frontend: Render / Vercel / Cloudflare Pages (Free Tier)
- **Root Directory:** `frontend`
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Environment Variable:** `VITE_API_URL=https://your-backend.onrender.com/api/v1`

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
<b>ZyncRole AI</b> — Built with ❤️ for autonomous, transparent, and fair career intelligence.
</div>
