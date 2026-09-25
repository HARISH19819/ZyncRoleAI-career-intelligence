-- ====================================================================
-- ZyncRole AI - PostgreSQL & Supabase Migration: Initial Schema
-- ====================================================================

-- 1. Enable pgvector extension for semantic candidate-to-job matching
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- 2. User Profiles
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    auth_user_id UUID UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) DEFAULT '',
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(50),
    headline VARCHAR(255),
    current_location VARCHAR(150),
    avatar_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Career Preferences
CREATE TABLE IF NOT EXISTS career_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    preferred_roles JSONB DEFAULT '[]'::jsonb,
    preferred_domains JSONB DEFAULT '[]'::jsonb,
    preferred_locations JSONB DEFAULT '[]'::jsonb,
    work_modes JSONB DEFAULT '[]'::jsonb,
    employment_types JSONB DEFAULT '[]'::jsonb,
    salary_min NUMERIC(12, 2) DEFAULT 0,
    salary_currency VARCHAR(10) DEFAULT 'USD',
    preferred_company_types JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_career_preferences_user UNIQUE (user_id)
);

-- 4. Resumes
CREATE TABLE IF NOT EXISTS resumes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    storage_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    raw_text TEXT,
    uploaded_at TIMESTAMPTZ DEFAULT NOW(),
    is_current BOOLEAN DEFAULT TRUE,
    processing_status VARCHAR(50) DEFAULT 'UPLOADED', -- UPLOADED, PROCESSING, COMPLETED, FAILED
    content_hash VARCHAR(64)
);

-- 5. Resume Analyses (ATS Compatibility & Heuristics)
CREATE TABLE IF NOT EXISTS resume_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resume_id UUID NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    ats_score NUMERIC(5, 2) NOT NULL,
    keyword_score NUMERIC(5, 2) NOT NULL,
    role_relevance_score NUMERIC(5, 2) NOT NULL,
    section_score NUMERIC(5, 2) NOT NULL,
    project_score NUMERIC(5, 2) NOT NULL,
    formatting_score NUMERIC(5, 2) NOT NULL,
    achievement_score NUMERIC(5, 2) NOT NULL,
    contact_score NUMERIC(5, 2) NOT NULL,
    strengths JSONB DEFAULT '[]'::jsonb,
    weaknesses JSONB DEFAULT '[]'::jsonb,
    detected_skills JSONB DEFAULT '[]'::jsonb,
    detected_projects JSONB DEFAULT '[]'::jsonb,
    detected_experience JSONB DEFAULT '[]'::jsonb,
    detected_education JSONB DEFAULT '[]'::jsonb,
    raw_structured_profile JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Structured Candidate Profile (Candidate Intelligence)
CREATE TABLE IF NOT EXISTS candidate_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    career_level VARCHAR(50) DEFAULT 'fresher',
    domains JSONB DEFAULT '[]'::jsonb,
    skills JSONB DEFAULT '[]'::jsonb,
    education JSONB DEFAULT '[]'::jsonb,
    projects JSONB DEFAULT '[]'::jsonb,
    experience JSONB DEFAULT '[]'::jsonb,
    certifications JSONB DEFAULT '[]'::jsonb,
    preferred_roles JSONB DEFAULT '[]'::jsonb,
    preferred_locations JSONB DEFAULT '[]'::jsonb,
    work_mode JSONB DEFAULT '[]'::jsonb,
    completeness_score INTEGER DEFAULT 0,
    embedding vector(768),
    embedding_hash VARCHAR(64),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_candidate_profile_user UNIQUE (user_id)
);

-- 7. Job Sources Registry
CREATE TABLE IF NOT EXISTS job_sources (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- AGGREGATED_API, ATS_API, JOB_BOARD, GATED, DEMO
    enabled BOOLEAN DEFAULT FALSE,
    requires_api_key BOOLEAN DEFAULT FALSE,
    supports_live_fetch BOOLEAN DEFAULT FALSE,
    supports_search BOOLEAN DEFAULT FALSE,
    supports_pagination BOOLEAN DEFAULT FALSE,
    supports_incremental_sync BOOLEAN DEFAULT FALSE,
    attribution_required BOOLEAN DEFAULT FALSE,
    terms_url TEXT,
    region VARCHAR(50) DEFAULT 'GLOBAL',
    last_successful_sync TIMESTAMPTZ,
    last_error TEXT,
    job_count INTEGER DEFAULT 0
);

-- 8. Jobs
CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id VARCHAR(50) NOT NULL REFERENCES job_sources(id),
    source_job_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    country VARCHAR(100) DEFAULT 'US',
    work_mode VARCHAR(50) DEFAULT 'On-site', -- Remote, Hybrid, On-site
    employment_type VARCHAR(50) DEFAULT 'Full-time', -- Full-time, Internship, Contract, Part-time
    description TEXT NOT NULL,
    requirements TEXT,
    responsibilities TEXT,
    required_skills JSONB DEFAULT '[]'::jsonb,
    preferred_skills JSONB DEFAULT '[]'::jsonb,
    all_skills JSONB DEFAULT '[]'::jsonb,
    experience_text VARCHAR(150),
    experience_min NUMERIC(4, 1) DEFAULT 0,
    experience_max NUMERIC(4, 1) DEFAULT 0,
    eligible_for_fresher BOOLEAN DEFAULT FALSE,
    education_text VARCHAR(255),
    domain VARCHAR(100) NOT NULL DEFAULT 'Other',
    salary_min NUMERIC(12, 2),
    salary_max NUMERIC(12, 2),
    salary_currency VARCHAR(10) DEFAULT 'USD',
    source_url TEXT NOT NULL,
    apply_url TEXT NOT NULL,
    canonical_url TEXT,
    published_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    collected_at TIMESTAMPTZ DEFAULT NOW(),
    verified_at TIMESTAMPTZ DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'ACTIVE', -- NEW, RECENT, ACTIVE, STALE, EXPIRED, UNAVAILABLE
    content_hash VARCHAR(64) NOT NULL,
    duplicate_of_job_id UUID REFERENCES jobs(id) ON DELETE SET NULL,
    embedding vector(768)
);

-- 9. Job Matches (Computed compatibility & explanation)
CREATE TABLE IF NOT EXISTS job_matches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    match_score NUMERIC(5, 2) NOT NULL,
    skill_score NUMERIC(5, 2) NOT NULL,
    role_score NUMERIC(5, 2) NOT NULL,
    domain_score NUMERIC(5, 2) NOT NULL,
    experience_score NUMERIC(5, 2) NOT NULL,
    education_score NUMERIC(5, 2) NOT NULL,
    location_score NUMERIC(5, 2) NOT NULL,
    preference_score NUMERIC(5, 2) NOT NULL,
    semantic_score NUMERIC(5, 2) NOT NULL,
    matched_skills JSONB DEFAULT '[]'::jsonb,
    missing_required_skills JSONB DEFAULT '[]'::jsonb,
    missing_preferred_skills JSONB DEFAULT '[]'::jsonb,
    strengths JSONB DEFAULT '[]'::jsonb,
    concerns JSONB DEFAULT '[]'::jsonb,
    explanation TEXT NOT NULL,
    how_to_improve TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_user_job_match UNIQUE (user_id, job_id)
);

-- 10. Saved Jobs
CREATE TABLE IF NOT EXISTS saved_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_saved_jobs_user_job UNIQUE (user_id, job_id)
);

-- 11. Applications
CREATE TABLE IF NOT EXISTS applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'Applied', -- Saved, Viewed, Applied, Assessment, Interview, Selected, Rejected
    applied_at TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT,
    follow_up_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT uq_applications_user_job UNIQUE (user_id, job_id)
);

-- 12. In-App Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) DEFAULT 'opportunity', -- opportunity, resume, profile, match, system
    link TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 13. Job Ingestion Runs
CREATE TABLE IF NOT EXISTS job_ingestion_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id VARCHAR(50) REFERENCES job_sources(id),
    status VARCHAR(50) NOT NULL, -- RUNNING, COMPLETED, FAILED
    jobs_fetched INTEGER DEFAULT 0,
    jobs_added INTEGER DEFAULT 0,
    jobs_updated INTEGER DEFAULT 0,
    jobs_duplicates INTEGER DEFAULT 0,
    error_message TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- 14. User Activity Events
CREATE TABLE IF NOT EXISTS user_activity (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    event_data JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ====================================================================
-- INDEXES FOR PERFORMANCE
-- ====================================================================
CREATE INDEX IF NOT EXISTS idx_jobs_domain ON jobs(domain);
CREATE INDEX IF NOT EXISTS idx_jobs_location ON jobs(location);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_published_at ON jobs(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_jobs_source_id ON jobs(source_id);
CREATE INDEX IF NOT EXISTS idx_jobs_content_hash ON jobs(content_hash);
CREATE INDEX IF NOT EXISTS idx_job_matches_user_score ON job_matches(user_id, match_score DESC);
CREATE INDEX IF NOT EXISTS idx_saved_jobs_user ON saved_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_applications_user ON applications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_user_unread ON notifications(user_id, is_read);

-- ====================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ====================================================================
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE career_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE candidate_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE resumes ENABLE ROW LEVEL SECURITY;
ALTER TABLE resume_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_matches ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activity ENABLE ROW LEVEL SECURITY;

-- Jobs and Job Sources are public read-only to all authenticated users
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE job_sources ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to jobs" ON jobs FOR SELECT USING (true);
CREATE POLICY "Allow public read access to job_sources" ON job_sources FOR SELECT USING (true);

-- User Isolation Policies
CREATE POLICY "Users can view own profile" ON profiles FOR ALL USING (auth.uid() = auth_user_id);
CREATE POLICY "Users can manage own career preferences" ON career_preferences FOR ALL USING (auth.uid() IN (SELECT auth_user_id FROM profiles WHERE id = career_preferences.user_id));
CREATE POLICY "Users can manage own candidate profile" ON candidate_profiles FOR ALL USING (auth.uid() IN (SELECT auth_user_id FROM profiles WHERE id = candidate_profiles.user_id));
CREATE POLICY "Users can manage own resumes" ON resumes FOR ALL USING (auth.uid() IN (SELECT auth_user_id FROM profiles WHERE id = resumes.user_id));
CREATE POLICY "Users can view own resume analyses" ON resume_analyses FOR ALL USING (auth.uid() IN (SELECT auth_user_id FROM profiles p JOIN resumes r ON r.user_id = p.id WHERE r.id = resume_analyses.resume_id));
CREATE POLICY "Users can manage own matches" ON job_matches FOR ALL USING (auth.uid() IN (SELECT auth_user_id FROM profiles WHERE id = job_matches.user_id));
CREATE POLICY "Users can manage own saved jobs" ON saved_jobs FOR ALL USING (auth.uid() IN (SELECT auth_user_id FROM profiles WHERE id = saved_jobs.user_id));
CREATE POLICY "Users can manage own applications" ON applications FOR ALL USING (auth.uid() IN (SELECT auth_user_id FROM profiles WHERE id = applications.user_id));
CREATE POLICY "Users can manage own notifications" ON notifications FOR ALL USING (auth.uid() IN (SELECT auth_user_id FROM profiles WHERE id = notifications.user_id));
