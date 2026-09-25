# ZyncRole AI

<div align="center">

# ZyncRole AI
### *"One Resume. Every Opportunity. One Intelligent Career Feed."*

[![Backend Tests](https://github.com/your-org/zyncrole-ai/actions/workflows/test.yml/badge.svg)](https://github.com/your-org/zyncrole-ai/actions)
[![Frontend Build](https://github.com/your-org/zyncrole-ai/actions/workflows/frontend-build.yml/badge.svg)](https://github.com/your-org/zyncrole-ai/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React 19](https://img.shields.io/badge/React-19.0-61DAFB.svg?style=flat&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8-3178C6.svg?style=flat&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An autonomous AI career intelligence and personalized job matching platform.**  
*Lightweight, free to operate within free tiers, deterministic, and built for national-level hackathon evaluation.*

</div>

---

## 🌟 Overview & Key Innovations

Job hunting is fragmented across dozens of disconnected job boards, aggregator sites, and opaque applicant tracking systems. Candidates submit generic resumes into black-box algorithms without understanding why they were rejected or what skills they were missing.

**ZyncRole AI solves this end-to-end:**
1. **Aggregates Opportunities Ethically:** Normalizes listings from public ATS boards (Greenhouse, Lever, Ashby), open tech APIs (Remotive, The Muse), and partner feeds into one unified feed with **zero unauthorized scraping**.
2. **Deterministic 8-Dimension Matching:** Replaces hallucinated LLM scores with an auditable mathematical compatibility engine.
3. **Transparent "Why This Match?" Breakdown:** Shows the exact percentage contribution of skills, target roles, experience level, education, work modes, and semantic vector similarity.
4. **7-Dimension ATS Evaluation:** Analyzes resumes (PDF, DOCX, TXT) across key ATS metrics and connects candidates directly to **OpenResume** to build compliant resumes.
5. **Real-Time Skill Gap Intelligence:** Surfaces the exact recurring missing skills across target opportunities with actionable impact ratings (High, Medium, Low).
6. **Application Pipeline Tracker:** Tracks recruitment stages (Applied, Assessment, Interview, Offer, Rejected) via interactive Kanban and Table views.
7. **Complete Data Sovereignty:** Self-service JSON data export and permanent 1-click right to erasure.
8. **No Admin Interface (Hard Product Boundary):** Operates autonomously with zero administrative routes, dashboards, or privileged tables.

---

## 🏗️ System Architecture

```mermaid
graph TD
    Client["React 19 + TypeScript + Vite SPA<br/>(Tailwind CSS, TanStack Query, Recharts)"]
    API["FastAPI 0.115 Application Gateway<br/>(Async Coroutines, Bcrypt, PyJWT)"]
    
    subgraph Intelligence ["Autonomous AI & ML Agents"]
        Norm["Job Normalization Agent"]
        Dedup["Job Deduplication Agent (SHA-256 + RapidFuzz)"]
        Class["Domain Classification Agent (20+ Categories)"]
        Skill["Skill & Experience Extraction Agent"]
        ATS["7-Dimension ATS Evaluation Engine"]
        Match["8-Dimension Deterministic Matching Engine"]
        Embed["Semantic Vectorizer (Gemini / TF-IDF Fallback)"]
        Gap["Skill Gap & Market Intelligence Agent"]
    end

    subgraph Storage ["Zero-Cost Storage Layer"]
        DB["Supabase PostgreSQL 15 + pgvector<br/>(Automatic Local SQLite Fallback)"]
        Uploads["Secure File Storage (/uploads)"]
    end

    Client <-->|REST API + JWT| API
    API <--> Intelligence
    Intelligence <--> Storage
    Client -.->|External CTA| OpenResume["OpenResume ATS Builder"]
```

---

## 🎯 The 8-Dimension Compatibility Formula

The total compatibility score $S_{total} \in [0, 100]$ is computed deterministically:

$$S_{total} = 100 \times \sum_{i=1}^{8} \left( w_i \times s_i \right)$$

| Dimension | Weight | Mathematical Methodology |
|:---|:---:|:---|
| **1. Skill Compatibility** | `30%` | Canonical taxonomy Jaccard overlap on required (75%) and preferred (25%) skills. |
| **2. Role Alignment** | `15%` | `RapidFuzz` token set ratio between target roles and job title. |
| **3. Domain Alignment** | `10%` | Category overlap across 20+ specialized engineering domains. |
| **4. Experience Level** | `10%` | Candidate career level vs job requirements (fresher friendly heuristics). |
| **5. Education Fit** | `5%` | Degree level and technical specialization alignment. |
| **6. Location & Mobility** | `10%` | Geographic distance and remote tolerance scoring. |
| **7. Preferences Fit** | `5%` | Salary threshold compliance and work mode compatibility. |
| **8. Semantic Embeddings** | `15%` | Cosine similarity via **Gemini Embedding 2** or deterministic **TF-IDF**. |

*Note: All weights strictly sum to 1.00 and are dynamically validated on startup.*

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python 3.11+**
- **Node.js 20+** and **npm 10+**

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/your-org/zyncrole-ai.git
cd ZyncRole_AI

# Copy environment variables
cp .env.example .env
```

### 2. Backend Setup
```bash
# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run backend server (auto-creates tables and seeds demo opportunities)
cd backend
python -m uvicorn app.main:app --reload --port 8000
```
*Backend is accessible at: `http://localhost:8000` (Swagger docs at `/docs`)*

### 3. Frontend Setup
In a new terminal:
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
*Frontend is accessible at: `http://localhost:5173`*

---

## ⚡ 1-Click Instant Demo Evaluation

For rapid hackathon jury review:
1. Navigate to `http://localhost:5173/login`.
2. Click the **"Launch Instant Demo Profile"** button.
3. Automatically logs in as **Alex Chen (AI / ML Engineer)** with pre-configured career preferences, evaluated resume, and high-compatibility matched opportunities.

---

## 🐳 Running with Docker Compose

To run the complete platform containerized:
```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`

---

## 🧪 Testing & Verification

The test suite validates agent logic, ATS scoring, fuzzy deduplication, and full API integration:

```bash
# Run all unit and integration tests
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

## ☁️ Free-Tier Production Deployment Guide

ZyncRole AI is specifically engineered to run **100% free of charge** across production cloud tiers:

### 1. Database: Supabase (Free Tier)
1. Create a free project at [supabase.com](https://supabase.com).
2. Go to **SQL Editor** and run the migration script:
   `supabase/migrations/20260325000000_initial_schema.sql`
3. Copy your project URL, anon key, and connection string to `.env`:
   ```env
   SUPABASE_DB_URL=postgresql+asyncpg://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   SUPABASE_URL=https://[PROJECT-REF].supabase.co
   SUPABASE_ANON_KEY=[YOUR-ANON-KEY]
   ```

### 2. Backend: Render / Railway / Fly.io (Free Tier)
1. Connect your GitHub repository to [Render](https://render.com).
2. Create a **Web Service**:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Set environment variables from your `.env`.

### 3. Frontend: Cloudflare Pages / Vercel (Free Tier)
1. Connect your repository to [Cloudflare Pages](https://pages.cloudflare.com) or [Vercel](https://vercel.com).
2. Configure build settings:
   - **Root directory:** `frontend`
   - **Build command:** `npm run build`
   - **Output directory:** `dist`
3. Add environment variable:
   `VITE_API_URL=https://your-backend.onrender.com/api/v1`

---

## 📚 Technical Documentation Index

- [System Architecture & Data Flows](docs/architecture.md)
- [8-Dimension Deterministic Matching Engine](docs/matching-engine.md)
- [Job Ingestion Adapters & Deduplication](docs/job-sources.md)
- [AI & ML Agents Specifications](docs/ai-agents.md)
- [Privacy Architecture & Data Sovereignty](docs/privacy.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
