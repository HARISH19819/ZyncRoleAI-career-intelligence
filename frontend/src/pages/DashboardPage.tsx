import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { DashboardData } from '@/types'
import { JobCard } from '@/components/JobCard'
import { DashboardSkeleton } from '@/components/SkeletonLoader'
import { ExternalResumeBuilderButton } from '@/components/ExternalResumeBuilderButton'
import {
  Sparkles,
  ArrowRight,
  TrendingUp,
  FileText,
  Layers,
  Briefcase,
  CheckCircle2,
  Clock,
  Compass,
  AlertCircle
} from 'lucide-react'

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchDashboard = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const res = await api.get<DashboardData>('/dashboard')
      setData(res)
    } catch (err: any) {
      setError(err.message || 'Unable to load dashboard.')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchDashboard()
  }, [])

  if (isLoading) {
    return <DashboardSkeleton />
  }

  if (error || !data) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-slate-800">Unable to load career dashboard</h2>
        <p className="text-sm text-slate-500 mt-1">{error || 'Please check your connection and retry.'}</p>
        <button
          onClick={fetchDashboard}
          className="mt-4 px-4 py-2 bg-brand-600 text-white rounded-xl text-xs font-semibold hover:bg-brand-700 transition"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Personalized Header (Section 43 & 82) */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200/60">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
              {data.greeting}, {data.first_name}
            </h1>
            <Sparkles className="w-5 h-5 text-brand-600" />
          </div>
          <p className="text-sm text-slate-500 mt-1">
            {data.headline_status}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/jobs"
            className="inline-flex items-center px-4 py-2 text-xs font-semibold text-slate-700 bg-white border border-slate-200/90 rounded-xl hover:bg-slate-50 shadow-subtle transition"
          >
            <span>Explore All Jobs</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
          </Link>
          <ExternalResumeBuilderButton
            label="Open ATS Builder"
            variant="outline"
            className="text-xs py-2 px-3.5"
          />
        </div>
      </div>

      {/* Overview Cards: Profile Readiness, Resume Status, Quick Insights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Profile Readiness */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                Career Profile
              </span>
              <span className="text-xs font-bold text-brand-600">
                {data.profile_readiness_score}% Complete
              </span>
            </div>
            <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
              <div
                className="bg-brand-600 h-full rounded-full transition-all duration-500"
                style={{ width: `${data.profile_readiness_score}%` }}
              />
            </div>
            <p className="text-xs text-slate-500 mt-3 leading-relaxed">
              {data.profile_readiness_score >= 80
                ? 'Your career profile is well detailed. Recommendation weights are fully active.'
                : 'Adding preferred roles and verified projects will refine recommendation matching.'}
            </p>
          </div>
          <Link
            to="/profile"
            className="inline-flex items-center text-xs font-semibold text-brand-600 hover:text-brand-700 mt-4"
          >
            <span>Review Profile</span>
            <ArrowRight className="w-3 h-3 ml-1" />
          </Link>
        </div>

        {/* Resume ATS Status */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                Resume ATS Health
              </span>
              {data.resume_status?.has_resume && data.resume_status?.ats_score !== undefined && (
                <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-md">
                  {Math.round(data.resume_status.ats_score)}/100
                </span>
              )}
            </div>

            {data.resume_status?.has_resume ? (
              <div className="space-y-1.5 mt-2">
                <p className="text-xs font-medium text-slate-800 truncate">
                  {data.resume_status.file_name}
                </p>
                <p className="text-xs text-slate-500">
                  {data.resume_status.detected_skills_count} detected skills extracted and evaluated.
                </p>
              </div>
            ) : (
              <p className="text-xs text-slate-500 mt-2 leading-relaxed">
                No resume uploaded yet. Upload a PDF or DOCX to unlock ATS analysis and deep matching.
              </p>
            )}
          </div>

          <div className="mt-4 flex items-center justify-between">
            <Link
              to="/resume"
              className="inline-flex items-center text-xs font-semibold text-brand-600 hover:text-brand-700"
            >
              <span>{data.resume_status?.has_resume ? 'View Analysis' : 'Upload Resume'}</span>
              <ArrowRight className="w-3 h-3 ml-1" />
            </Link>
            <ExternalResumeBuilderButton variant="outline" label="Builder" className="text-xs py-1 px-2.5" />
          </div>
        </div>

        {/* Skill Gap Snapshot */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                Top Skill Gaps
              </span>
              <span className="text-xs text-amber-600 font-medium">In demand</span>
            </div>

            {data.skill_gap_snapshot.length > 0 ? (
              <div className="space-y-2 mt-2">
                {data.skill_gap_snapshot.slice(0, 2).map((gap) => (
                  <div key={gap.skill} className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-700">{gap.skill}</span>
                    <span className="text-slate-500">{gap.frequency_percentage}% of roles</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-500 mt-2">
                Your profile covers the key skills for your selected roles!
              </p>
            )}
          </div>

          <Link
            to="/skill-gaps"
            className="inline-flex items-center text-xs font-semibold text-brand-600 hover:text-brand-700 mt-4"
          >
            <span>View Skill Gap Intelligence</span>
            <ArrowRight className="w-3 h-3 ml-1" />
          </Link>
        </div>
      </div>

      {/* Primary Section: Best Matches for You (Section 43 & 82) */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-slate-900 tracking-tight">
              Best matches for you
            </h2>
            <p className="text-xs text-slate-500">
              Ranked highest compatibility first based on skills, domain, and experience
            </p>
          </div>
          <Link
            to="/jobs?sort=match_score"
            className="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center"
          >
            <span>View all</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1" />
          </Link>
        </div>

        {data.recommended_jobs.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {data.recommended_jobs.map((job) => (
              <JobCard
                key={job.id}
                job={job}
                onToggleSave={() => {}}
              />
            ))}
          </div>
        ) : (
          <div className="bg-white rounded-2xl border border-slate-200/80 p-8 text-center max-w-md mx-auto">
            <Compass className="w-10 h-10 text-slate-400 mx-auto mb-3" />
            <h3 className="text-sm font-bold text-slate-800">Your best matches start with your resume</h3>
            <p className="text-xs text-slate-500 mt-1">
              Upload your resume or set career interests to reveal high-compatibility matches.
            </p>
            <Link
              to="/resume"
              className="mt-4 inline-flex items-center px-4 py-2 bg-brand-600 text-white rounded-xl text-xs font-semibold hover:bg-brand-700 shadow-subtle transition"
            >
              Upload Resume
            </Link>
          </div>
        )}
      </section>

      {/* Recent Applications Snapshot */}
      {data.recent_applications.length > 0 && (
        <section className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-slate-800 flex items-center gap-1.5">
              <Briefcase className="w-4 h-4 text-brand-600" />
              <span>Recent Applications ({data.recent_applications.length})</span>
            </h3>
            <Link
              to="/applications"
              className="text-xs font-semibold text-brand-600 hover:underline"
            >
              Manage all
            </Link>
          </div>

          <div className="divide-y divide-slate-100">
            {data.recent_applications.map((app) => (
              <div key={app.id} className="py-2.5 flex items-center justify-between text-xs">
                <div>
                  <span className="font-semibold text-slate-800">{app.job_title}</span>
                  <span className="text-slate-400 mx-1.5">•</span>
                  <span className="text-slate-600">{app.company}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-0.5 rounded-md font-medium text-[11px] bg-blue-50 text-blue-700">
                    {app.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
