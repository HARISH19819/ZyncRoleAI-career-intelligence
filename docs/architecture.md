# ZyncRole AI - System Architecture & Engineering Design

> **"One Resume. Every Opportunity. One Intelligent Career Feed."**

---

## 1. High-Level System Architecture

```mermaid
graph TD
    subgraph Client ["Client Layer (React / Vite / TypeScript)"]
        SPA["Vite SPA (Tailwind CSS, TanStack Query)"]
        AuthCtx["Auth Context (JWT + Local/Supabase)"]
        Drawer["Match Explanation & ATS Drawer"]
    end

    subgraph API ["Application Server (FastAPI / Python 3.11)"]
        Router["FastAPI APIRouter (/api/v1)"]
        AuthMiddleware["Security & Auth Middleware (Bcrypt, JWT)"]
        LoggerMiddleware["Structured Correlation Logger"]
    end

    subgraph Intelligence ["Autonomous AI & ML Agents"]
        NormAgent["Job Normalization Agent"]
        DedupAgent["Job Deduplication Agent (SHA-256 + RapidFuzz)"]
        ClassAgent["Domain Classification Agent (20+ Taxonomy)"]
        SkillAgent["Skill Extraction Agent (Canonical Dictionary)"]
        ATSEngine["7-Dimension ATS Evaluation Engine"]
        MatchEngine["8-Dimension Deterministic Matching Engine"]
        EmbedEngine["Gemini Embedding 2 / TF-IDF Vectorizer"]
        GapAgent["Skill Gap & Market Intelligence Agent"]
    end

    subgraph Data ["Data & Storage Layer"]
        DB["Supabase PostgreSQL + pgvector (or SQLite aiosqlite)"]
        FileStore["Secure Resume Storage (/uploads)"]
        ExternalBuilder["External ATS Resume Builder (OpenResume)"]
    end

    SPA --> Router
    Router --> AuthMiddleware
    AuthMiddleware --> Intelligence
    Intelligence --> DB
    Intelligence --> FileStore
    SPA -.-> ExternalBuilder
```

---

## 2. Architectural Principles & Zero-Cost Operation

1. **Lightweight & Free Tier Optimized:**
   - **Backend:** FastAPI async coroutines running on standard Python 3.11 with zero memory-bloated runtime dependencies.
   - **Database:** Supabase Free Tier (PostgreSQL 15 with pgvector extension) with automatic zero-config local SQLite fallback for offline demo execution.
   - **AI/ML:** Local deterministic algorithms (TF-IDF + Cosine similarity, RapidFuzz token matching, Regex heuristic parsing) combined with free-tier Google Gemini 2.0 Flash / text-embedding-004.
   - **External ATS Builder:** Configured to direct users to OpenResume without hosting an unmaintainable PDF canvas engine.

2. **No Admin Interface (Hard Product Boundary):**
   - In accordance with core system constraints, ZyncRole AI contains **no administrative portals, no admin login routes, and no privileged operator tables**.
   - Platform administration is handled autonomously via scheduled ingestion workers and secure environment credentials.

3. **Pluggable Ingestion Pipeline:**
   - Every job source adheres to `BaseSourceAdapter`.
   - Free/open adapters (Remotive, Adzuna, The Muse, Greenhouse, Lever, Ashby, Generic Feeds) are active.
   - Gated or proprietary sources (LinkedIn, Indeed, Naukri, Internshala) operate via official/partner APIs and are gracefully disabled unless valid partner credentials are provided. **No unauthorized scraping is executed.**

---

## 3. Database Entity Relationship Model

```mermaid
erDiagram
    PROFILES ||--o| CAREER_PREFERENCES : has
    PROFILES ||--o| CANDIDATE_PROFILES : has
    PROFILES ||--o{ RESUMES : uploads
    PROFILES ||--o{ SAVED_JOBS : bookmarks
    PROFILES ||--o{ APPLICATIONS : tracks
    PROFILES ||--o{ NOTIFICATIONS : receives
    PROFILES ||--o{ USER_ACTIVITY : logs
    RESUMES ||--o| RESUME_ANALYSES : evaluates
    JOB_SOURCES ||--o{ JOBS : ingests
    JOBS ||--o{ SAVED_JOBS : saved_in
    JOBS ||--o{ APPLICATIONS : applied_to
    JOBS ||--o{ JOB_MATCHES : computed_for

    PROFILES {
        string id PK
        string email UK
        string first_name
        string last_name
        string headline
        string current_location
    }

    CAREER_PREFERENCES {
        string id PK
        string user_id FK
        json preferred_roles
        json preferred_domains
        json work_modes
        float salary_min
    }

    CANDIDATE_PROFILES {
        string id PK
        string user_id FK
        string career_level
        json skills
        json education
        json experience
        int completeness_score
        vector embedding
    }

    JOBS {
        string id PK
        string source_id FK
        string title
        string company
        string location
        string work_mode
        string domain
        json required_skills
        json preferred_skills
        vector embedding
        string apply_url
        string content_hash UK
    }

    APPLICATIONS {
        string id PK
        string user_id FK
        string job_id FK
        string status
        datetime applied_at
        text notes
    }
```

---

## 4. End-to-End User Journey

1. **Discovery & Onboarding:**
   - User registers or clicks **1-Click Instant Demo Evaluation**.
   - Completes 4 calm, intuitive onboarding steps: Education, Career Interests, Preferences, and Skills.
   - Profile Agent synthesizes candidate intelligence and computes readiness percentage.

2. **Resume Intelligence & ATS Evaluation:**
   - User uploads resume (PDF, DOCX, or TXT).
   - PyMuPDF / python-docx extracts raw structured text and detects contact details, projects, education, and skills.
   - ATS Engine benchmarks resume across 7 dimensions (Keywords, Role Relevance, Formatting, Achievements, Sections, Projects, Contact info) outputting actionable strengths and weaknesses.
   - One-click CTA links to OpenResume to rebuild in ATS-compliant format.

3. **Autonomous Career Feed & Matching:**
   - 8-Dimension Deterministic Engine benchmarks user against all ingested, deduplicated opportunities.
   - Match Score Drawer reveals exact mathematical breakdown and explains *why* the candidate fits and *how to improve*.
   - User bookmarks roles or clicks "Apply", which opens authentic employer posting and logs progress in the Application Pipeline.
