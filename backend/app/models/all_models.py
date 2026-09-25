import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column, String, Text, Boolean, Integer, Float, DateTime,
    ForeignKey, UniqueConstraint, JSON
)
from sqlalchemy.orm import relationship
from app.db.session import Base


def generate_uuid():
    return str(uuid.uuid4())


def get_utc_now():
    return datetime.now(timezone.utc)


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    auth_user_id = Column(String(36), unique=True, index=True, nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), default="", nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)  # For local fallback auth
    phone = Column(String(50), nullable=True)
    headline = Column(String(255), nullable=True)
    current_location = Column(String(150), nullable=True)
    avatar_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    career_preferences = relationship("CareerPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    candidate_profile = relationship("CandidateProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    job_matches = relationship("JobMatch", back_populates="user", cascade="all, delete-orphan")
    saved_jobs = relationship("SavedJob", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class CareerPreference(Base):
    __tablename__ = "career_preferences"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    preferred_roles = Column(JSON, default=list)
    preferred_domains = Column(JSON, default=list)
    preferred_locations = Column(JSON, default=list)
    work_modes = Column(JSON, default=list)  # Remote, Hybrid, On-site
    employment_types = Column(JSON, default=list)  # Full-time, Internship
    salary_min = Column(Float, default=0.0)
    salary_currency = Column(String(10), default="USD")
    preferred_company_types = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    user = relationship("Profile", back_populates="career_preferences")


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), unique=True, nullable=False)
    career_level = Column(String(50), default="fresher")
    domains = Column(JSON, default=list)
    skills = Column(JSON, default=list)
    education = Column(JSON, default=list)
    projects = Column(JSON, default=list)
    experience = Column(JSON, default=list)
    certifications = Column(JSON, default=list)
    preferred_roles = Column(JSON, default=list)
    preferred_locations = Column(JSON, default=list)
    work_mode = Column(JSON, default=list)
    completeness_score = Column(Integer, default=0)
    embedding = Column(JSON, nullable=True)  # Stored as list of floats for portable JSON/pgvector
    embedding_hash = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    user = relationship("Profile", back_populates="candidate_profile")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    storage_path = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    raw_text = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), default=get_utc_now)
    is_current = Column(Boolean, default=True)
    processing_status = Column(String(50), default="UPLOADED")  # UPLOADED, PROCESSING, COMPLETED, FAILED
    content_hash = Column(String(64), nullable=True)

    user = relationship("Profile", back_populates="resumes")
    analysis = relationship("ResumeAnalysis", back_populates="resume", uselist=False, cascade="all, delete-orphan")


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    resume_id = Column(String(36), ForeignKey("resumes.id", ondelete="CASCADE"), unique=True, nullable=False)
    ats_score = Column(Float, nullable=False)
    keyword_score = Column(Float, nullable=False)
    role_relevance_score = Column(Float, nullable=False)
    section_score = Column(Float, nullable=False)
    project_score = Column(Float, nullable=False)
    formatting_score = Column(Float, nullable=False)
    achievement_score = Column(Float, nullable=False)
    contact_score = Column(Float, nullable=False)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    detected_skills = Column(JSON, default=list)
    detected_projects = Column(JSON, default=list)
    detected_experience = Column(JSON, default=list)
    detected_education = Column(JSON, default=list)
    raw_structured_profile = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    resume = relationship("Resume", back_populates="analysis")


class JobSource(Base):
    __tablename__ = "job_sources"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    source_type = Column(String(50), nullable=False)  # AGGREGATED_API, ATS_API, JOB_BOARD, GATED, DEMO
    enabled = Column(Boolean, default=False)
    requires_api_key = Column(Boolean, default=False)
    supports_live_fetch = Column(Boolean, default=False)
    supports_search = Column(Boolean, default=False)
    supports_pagination = Column(Boolean, default=False)
    supports_incremental_sync = Column(Boolean, default=False)
    attribution_required = Column(Boolean, default=False)
    terms_url = Column(Text, nullable=True)
    region = Column(String(50), default="GLOBAL")
    last_successful_sync = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(Text, nullable=True)
    job_count = Column(Integer, default=0)

    jobs = relationship("Job", back_populates="source")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(50), ForeignKey("job_sources.id"), nullable=False)
    source_job_id = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    country = Column(String(100), default="US")
    work_mode = Column(String(50), default="On-site")  # Remote, Hybrid, On-site
    employment_type = Column(String(50), default="Full-time")  # Full-time, Internship, Contract
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    all_skills = Column(JSON, default=list)
    experience_text = Column(String(150), nullable=True)
    experience_min = Column(Float, default=0.0)
    experience_max = Column(Float, default=0.0)
    eligible_for_fresher = Column(Boolean, default=False)
    education_text = Column(String(255), nullable=True)
    domain = Column(String(100), default="Other", nullable=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String(10), default="USD")
    source_url = Column(Text, nullable=False)
    apply_url = Column(Text, nullable=False)
    canonical_url = Column(Text, nullable=True)
    published_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    collected_at = Column(DateTime(timezone=True), default=get_utc_now)
    verified_at = Column(DateTime(timezone=True), default=get_utc_now)
    status = Column(String(50), default="ACTIVE")  # NEW, RECENT, ACTIVE, STALE, EXPIRED, UNAVAILABLE
    content_hash = Column(String(64), nullable=False, index=True)
    duplicate_of_job_id = Column(String(36), ForeignKey("jobs.id"), nullable=True)
    embedding = Column(JSON, nullable=True)  # Portable embedding vector (768 dimensions)

    source = relationship("JobSource", back_populates="jobs")
    matches = relationship("JobMatch", back_populates="job", cascade="all, delete-orphan")
    saved_by = relationship("SavedJob", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")


class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=False)
    role_score = Column(Float, nullable=False)
    domain_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    education_score = Column(Float, nullable=False)
    location_score = Column(Float, nullable=False)
    preference_score = Column(Float, nullable=False)
    semantic_score = Column(Float, nullable=False)
    matched_skills = Column(JSON, default=list)
    missing_required_skills = Column(JSON, default=list)
    missing_preferred_skills = Column(JSON, default=list)
    strengths = Column(JSON, default=list)
    concerns = Column(JSON, default=list)
    explanation = Column(Text, nullable=False)
    how_to_improve = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_user_job_match"),
    )

    user = relationship("Profile", back_populates="job_matches")
    job = relationship("Job", back_populates="matches")


class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_saved_jobs_user_job"),
    )

    user = relationship("Profile", back_populates="saved_jobs")
    job = relationship("Job", back_populates="saved_by")


class Application(Base):
    __tablename__ = "applications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="Applied")  # Saved, Viewed, Applied, Assessment, Interview, Selected, Rejected
    applied_at = Column(DateTime(timezone=True), default=get_utc_now)
    notes = Column(Text, nullable=True)
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now)

    __table_args__ = (
        UniqueConstraint("user_id", "job_id", name="uq_applications_user_job"),
    )

    user = relationship("Profile", back_populates="applications")
    job = relationship("Job", back_populates="applications")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="opportunity")  # opportunity, resume, profile, match, system
    link = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)

    user = relationship("Profile", back_populates="notifications")


class JobIngestionRun(Base):
    __tablename__ = "job_ingestion_runs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source_id = Column(String(50), nullable=True)
    status = Column(String(50), nullable=False)  # RUNNING, COMPLETED, FAILED
    jobs_fetched = Column(Integer, default=0)
    jobs_added = Column(Integer, default=0)
    jobs_updated = Column(Integer, default=0)
    jobs_duplicates = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), default=get_utc_now)
    completed_at = Column(DateTime(timezone=True), nullable=True)


class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_data = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)
