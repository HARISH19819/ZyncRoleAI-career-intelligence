from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# ----------------------------------------------------
# AUTH SCHEMAS
# ----------------------------------------------------
class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field("", max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]
    onboarding_completed: bool = False


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)


# ----------------------------------------------------
# PROFILE & ONBOARDING SCHEMAS
# ----------------------------------------------------
class ProfileBase(BaseModel):
    first_name: str
    last_name: Optional[str] = ""
    headline: Optional[str] = None
    phone: Optional[str] = None
    current_location: Optional[str] = None
    avatar_url: Optional[str] = None


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    headline: Optional[str] = None
    phone: Optional[str] = None
    current_location: Optional[str] = None
    avatar_url: Optional[str] = None


class CareerPreferencesSchema(BaseModel):
    preferred_roles: List[str] = Field(default_factory=list)
    preferred_domains: List[str] = Field(default_factory=list)
    preferred_locations: List[str] = Field(default_factory=list)
    work_modes: List[str] = Field(default_factory=list)  # Remote, Hybrid, On-site
    employment_types: List[str] = Field(default_factory=list)  # Full-time, Internship
    salary_min: Optional[float] = 0.0
    salary_currency: Optional[str] = "USD"
    preferred_company_types: List[str] = Field(default_factory=list)


class OnboardingStep1(BaseModel):
    degree: Optional[str] = None
    specialization: Optional[str] = None
    college: Optional[str] = None
    graduation_year: Optional[int] = None
    current_status: Optional[str] = None  # Student, Fresher, Employed


class OnboardingStep2(BaseModel):
    desired_roles: List[str] = Field(default_factory=list)
    domains: List[str] = Field(default_factory=list)
    experience_level: Optional[str] = "fresher"
    job_type: Optional[str] = "Full-time"


class OnboardingStep3(BaseModel):
    location: Optional[str] = None
    work_mode: List[str] = Field(default_factory=list)
    preferred_cities: List[str] = Field(default_factory=list)
    salary_preference: Optional[float] = 0.0
    employment_preference: Optional[str] = "Full-time"


class OnboardingStep4(BaseModel):
    technical_skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)


class OnboardingFullRequest(BaseModel):
    education: Optional[OnboardingStep1] = None
    interests: Optional[OnboardingStep2] = None
    preferences: Optional[OnboardingStep3] = None
    skills: Optional[OnboardingStep4] = None


class CandidateProfileSchema(BaseModel):
    career_level: str = "fresher"
    domains: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    education: List[Dict[str, Any]] = Field(default_factory=list)
    projects: List[Dict[str, Any]] = Field(default_factory=list)
    experience: List[Dict[str, Any]] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    preferred_roles: List[str] = Field(default_factory=list)
    preferred_locations: List[str] = Field(default_factory=list)
    work_mode: List[str] = Field(default_factory=list)
    completeness_score: int = 0


class ProfileResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    headline: Optional[str] = None
    phone: Optional[str] = None
    current_location: Optional[str] = None
    avatar_url: Optional[str] = None
    career_preferences: Optional[CareerPreferencesSchema] = None
    candidate_profile: Optional[CandidateProfileSchema] = None
    completeness_percentage: int = 0
    created_at: Optional[datetime] = None


# ----------------------------------------------------
# RESUME & ATS SCHEMAS
# ----------------------------------------------------
class ResumeResponse(BaseModel):
    id: str
    file_name: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    is_current: bool
    processing_status: str


class ATSScoreBreakdown(BaseModel):
    keyword_score: float
    role_relevance_score: float
    section_score: float
    project_score: float
    formatting_score: float
    achievement_score: float
    contact_score: float


class ResumeAnalysisResponse(BaseModel):
    resume_id: str
    ats_score: float
    breakdown: ATSScoreBreakdown
    strengths: List[str]
    weaknesses: List[str]
    detected_skills: List[str]
    detected_projects: List[Dict[str, Any]]
    detected_experience: List[Dict[str, Any]]
    detected_education: List[Dict[str, Any]]
    builder_url: str
    created_at: datetime


# ----------------------------------------------------
# JOB & MATCH SCHEMAS
# ----------------------------------------------------
class JobSummary(BaseModel):
    id: str
    title: str
    company: str
    location: str
    country: str
    work_mode: str
    employment_type: str
    domain: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_currency: Optional[str] = "USD"
    source_id: str
    source_name: Optional[str] = None
    apply_url: str
    source_url: str
    published_at: datetime
    freshness_label: str
    top_skills: List[str]
    match_score: Optional[float] = None
    is_saved: bool = False
    application_status: Optional[str] = None


class JobDetail(JobSummary):
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    required_skills: List[str]
    preferred_skills: List[str]
    experience_text: Optional[str] = None
    experience_min: float
    experience_max: float
    eligible_for_fresher: bool
    education_text: Optional[str] = None
    verified_at: datetime
    duplicate_sources: List[str] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    skill_score: float
    role_score: float
    domain_score: float
    experience_score: float
    education_score: float
    location_score: float
    preference_score: float
    semantic_score: float


class JobMatchExplanation(BaseModel):
    job_id: str
    match_score: float
    compatibility_level: str  # Excellent Match, Strong Match, Potential Match, Partial Match, Low Match
    breakdown: ScoreBreakdown
    matched_skills: List[str]
    missing_required_skills: List[str]
    missing_preferred_skills: List[str]
    strengths: List[str]
    concerns: List[str]
    explanation: str
    how_to_improve: str


# ----------------------------------------------------
# SKILL GAP SCHEMAS
# ----------------------------------------------------
class SkillGapItem(BaseModel):
    skill: str
    frequency_percentage: float
    target_job_count: int
    status: str  # Missing, Partial, Acquired
    impact: str  # High, Medium, Low
    category: str


class SkillGapResponse(BaseModel):
    target_jobs_analyzed: int
    top_missing_skills: List[SkillGapItem]
    insights_summary: str


# ----------------------------------------------------
# CAREER INTELLIGENCE SCHEMAS
# ----------------------------------------------------
class MarketTrendItem(BaseModel):
    name: str
    count: int
    percentage: float


class CareerInsightsResponse(BaseModel):
    total_jobs: int
    selected_domain_jobs: int
    top_skills: List[MarketTrendItem]
    top_roles: List[MarketTrendItem]
    domain_distribution: List[MarketTrendItem]
    work_mode_distribution: List[MarketTrendItem]
    fresher_friendly_percentage: float
    location_trends: List[MarketTrendItem]
    user_skill_coverage_summary: str


# ----------------------------------------------------
# APPLICATIONS & SAVED SCHEMAS
# ----------------------------------------------------
class ApplicationCreate(BaseModel):
    job_id: str
    status: Optional[str] = "Applied"
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None


class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None


class ApplicationItem(BaseModel):
    id: str
    job_id: str
    job_title: str
    company: str
    location: str
    work_mode: str
    source_name: str
    apply_url: str
    match_score: Optional[float] = None
    status: str
    applied_at: datetime
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None


# ----------------------------------------------------
# NOTIFICATION SCHEMAS
# ----------------------------------------------------
class NotificationItem(BaseModel):
    id: str
    title: str
    message: str
    type: str
    link: Optional[str] = None
    is_read: bool
    created_at: datetime


# ----------------------------------------------------
# DASHBOARD SCHEMAS
# ----------------------------------------------------
class DashboardResponse(BaseModel):
    greeting: str
    first_name: str
    headline_status: str
    profile_readiness_score: int
    resume_status: Optional[Dict[str, Any]] = None
    recommended_jobs: List[JobSummary]
    skill_gap_snapshot: List[SkillGapItem]
    recent_applications: List[ApplicationItem]
    unread_notifications_count: int
