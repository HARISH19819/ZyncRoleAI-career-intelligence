export interface User {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  headline?: string;
  phone?: string;
  current_location?: string;
  avatar_url?: string;
}

export interface CareerPreferences {
  preferred_roles: string[];
  preferred_domains: string[];
  preferred_locations: string[];
  work_modes: string[];
  employment_types: string[];
  salary_min: number;
  salary_currency: string;
  preferred_company_types: string[];
}

export interface CandidateProfile {
  career_level: string;
  domains: string[];
  skills: string[];
  education: Array<{
    degree: string;
    specialization?: string;
    college?: string;
    graduation_year?: string | number;
  }>;
  projects: Array<{
    title: string;
    description: string;
  }>;
  experience: Array<{
    role: string;
    description: string;
  }>;
  certifications: string[];
  preferred_roles: string[];
  preferred_locations: string[];
  work_mode: string[];
  completeness_score: number;
}

export interface FullProfile extends User {
  career_preferences?: CareerPreferences;
  candidate_profile?: CandidateProfile;
  completeness_percentage: number;
  created_at?: string;
}

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  country: string;
  work_mode: string;
  employment_type: string;
  domain: string;
  salary_min?: number;
  salary_max?: number;
  salary_currency: string;
  source_id: string;
  source_name?: string;
  apply_url: string;
  source_url: string;
  published_at: string;
  freshness_label: string;
  top_skills: string[];
  match_score?: number;
  compatibility_level?: string;
  matched_skills?: string[];
  missing_required_skills?: string[];
  missing_preferred_skills?: string[];
  explanation?: string;
  is_saved?: boolean;
  application_status?: string | null;
}

export interface JobDetail extends Job {
  description: string;
  requirements?: string;
  responsibilities?: string;
  required_skills: string[];
  preferred_skills: string[];
  experience_text?: string;
  experience_min: number;
  experience_max: number;
  eligible_for_fresher: boolean;
  education_text?: string;
  verified_at: string;
  duplicate_sources: string[];
}

export interface ScoreBreakdown {
  skill_score: number;
  role_score: number;
  domain_score: number;
  experience_score: number;
  education_score: number;
  location_score: number;
  preference_score: number;
  semantic_score: number;
}

export interface JobMatchExplanation {
  job_id: string;
  match_score: number;
  compatibility_level: string;
  breakdown: ScoreBreakdown;
  matched_skills: string[];
  missing_required_skills: string[];
  missing_preferred_skills: string[];
  strengths: string[];
  concerns: string[];
  explanation: string;
  how_to_improve: string;
}

export interface ATSScoreBreakdown {
  keyword_score: number;
  role_relevance_score: number;
  section_score: number;
  project_score: number;
  formatting_score: number;
  achievement_score: number;
  contact_score: number;
}

export interface ResumeAnalysis {
  resume_id: string;
  ats_score: number;
  breakdown: ATSScoreBreakdown;
  strengths: string[];
  weaknesses: string[];
  detected_skills: string[];
  detected_projects: Array<{ title: string; description: string }>;
  detected_experience: Array<{ role: string; description: string }>;
  detected_education: Array<{ degree: string; institution?: string }>;
  builder_url: string;
  created_at: string;
}

export interface SkillGapItem {
  skill: string;
  frequency_percentage: number;
  target_job_count: number;
  status: string;
  impact: 'High' | 'Medium' | 'Low' | string;
  category: string;
}

export interface SkillGapResponse {
  target_jobs_analyzed: number;
  top_missing_skills: SkillGapItem[];
  insights_summary: string;
}

export interface MarketTrendItem {
  name: string;
  count: number;
  percentage: number;
}

export interface CareerInsights {
  total_jobs: number;
  selected_domain_jobs: number;
  top_skills: MarketTrendItem[];
  top_roles: MarketTrendItem[];
  domain_distribution: MarketTrendItem[];
  work_mode_distribution: MarketTrendItem[];
  fresher_friendly_percentage: number;
  location_trends: MarketTrendItem[];
  user_skill_coverage_summary: string;
}

export interface ApplicationItem {
  id: string;
  job_id: string;
  job_title: string;
  company: string;
  location: string;
  work_mode: string;
  source_name: string;
  apply_url: string;
  match_score?: number;
  status: string;
  applied_at: string;
  notes?: string;
  follow_up_date?: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  type: string;
  link?: string;
  is_read: boolean;
  created_at: string;
}

export interface DashboardData {
  greeting: string;
  first_name: string;
  headline_status: string;
  profile_readiness_score: number;
  resume_status?: {
    has_resume: boolean;
    file_name?: string;
    uploaded_at?: string;
    ats_score?: number;
    detected_skills_count?: number;
    builder_url: string;
  };
  recommended_jobs: Job[];
  skill_gap_snapshot: SkillGapItem[];
  recent_applications: ApplicationItem[];
  unread_notifications_count: number;
}
