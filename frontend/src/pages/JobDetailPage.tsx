import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { JobDetail, JobMatchExplanation } from '@/types'
import { getMatchScoreColor, formatSalary, ensureAbsoluteUrl } from '@/lib/utils'
import { MatchExplanationDrawer } from '@/components/MatchExplanationDrawer'
import {
  ArrowLeft,
  Building2,
  MapPin,
  Clock,
  Bookmark,
  ExternalLink,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  ShieldCheck,
  Share2
} from 'lucide-react'

export const JobDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [job, setJob] = useState<JobDetail | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaved, setIsSaved] = useState(false)
  const [isSaving, setIsSaving] = useState(false)
  const [explanation, setExplanation] = useState<JobMatchExplanation | null>(null)
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [showApplyFeedback, setShowApplyFeedback] = useState(false)

  useEffect(() => {
    const fetchJob = async () => {
      setIsLoading(true)
      try {
        const res = await api.get<JobDetail>(`/jobs/${id}`)
        setJob(res)
        setIsSaved(!!res.is_saved)

        // Fetch match breakdown
        const mRes = await api.get<JobMatchExplanation>(`/jobs/${id}/match`)
        setExplanation(mRes)
      } catch {
        // Fallback
      } finally {
        setIsLoading(false)
      }
    }

    if (id) fetchJob()
  }, [id])

  const handleSaveToggle = async () => {
    if (!job || isSaving) return
    setIsSaving(true)
    const nextState = !isSaved
    setIsSaved(nextState)

    try {
      if (nextState) {
        await api.post(`/saved/${job.id}`)
      } else {
        await api.delete(`/saved/${job.id}`)
      }
    } catch {
      setIsSaved(!nextState)
    } finally {
      setIsSaving(false)
    }
  }

  const handleApplyClick = () => {
    if (!job) return
    window.open(job.apply_url, '_blank', 'noopener,noreferrer')
    setShowApplyFeedback(true)
  }

  const handleConfirmApplied = async (applied: boolean) => {
    setShowApplyFeedback(false)
    if (applied && job) {
      try {
        await api.post('/applications', { job_id: job.id, status: 'Applied' })
      } catch {
        // Ignore
      }
    }
  }

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16 text-center animate-pulse">
        <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-xs text-slate-500">Loading opportunity details...</span>
      </div>
    )
  }

  if (!job) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center">
        <h2 className="text-lg font-bold text-slate-800">Job opportunity not found</h2>
        <p className="text-xs text-slate-500 mt-1">This opportunity may have expired or was removed.</p>
        <Link to="/jobs" className="mt-4 inline-block px-4 py-2 bg-brand-600 text-white rounded-xl text-xs font-semibold">
          Back to Explorer
        </Link>
      </div>
    )
  }

  const scoreStyle = explanation ? getMatchScoreColor(explanation.match_score) : null

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 animate-fade-in">
      {/* Back button */}
      <div>
        <Link
          to="/jobs"
          className="inline-flex items-center text-xs font-semibold text-slate-500 hover:text-slate-800 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5 mr-1" />
          <span>Back to Opportunities</span>
        </Link>
      </div>

      {/* Main 2-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Left Column: Job Description, Requirements, Responsibilities */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-subtle space-y-6">
            {/* Header info */}
            <div>
              <div className="flex items-center space-x-2 text-xs text-brand-600 font-semibold mb-2">
                <span className="px-2 py-0.5 rounded bg-brand-50 border border-brand-100">
                  {job.domain}
                </span>
                <span className="text-slate-400">•</span>
                <span className="text-slate-500">Source: {job.source_name || job.source_id.toUpperCase()}</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
                {job.title}
              </h1>
              <p className="text-base font-semibold text-slate-700 mt-1">{job.company}</p>

              {/* Chips */}
              <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mt-4 text-xs text-slate-500 pt-3 border-t border-slate-100">
                <div className="flex items-center space-x-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  <span>{job.location}</span>
                </div>
                <span>•</span>
                <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">
                  {job.work_mode}
                </span>
                <span>•</span>
                <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-700 font-medium">
                  {job.employment_type}
                </span>
                <span>•</span>
                <div className="flex items-center space-x-1">
                  <Clock className="w-3.5 h-3.5 text-slate-400" />
                  <span>{job.freshness_label}</span>
                </div>
                {job.salary_min && (
                  <>
                    <span>•</span>
                    <span className="text-emerald-700 font-semibold">
                      {formatSalary(job.salary_min, job.salary_max, job.salary_currency)}
                    </span>
                  </>
                )}
              </div>
            </div>

            {/* Description Body */}
            <div className="pt-4 border-t border-slate-100 space-y-6 text-sm text-slate-700 leading-relaxed">
              <div>
                <h2 className="text-base font-bold text-slate-900 mb-2">About the Role</h2>
                <p className="whitespace-pre-line text-slate-600">{job.description}</p>
              </div>

              {job.requirements && (
                <div>
                  <h2 className="text-base font-bold text-slate-900 mb-2">Qualifications & Requirements</h2>
                  <p className="whitespace-pre-line text-slate-600">{job.requirements}</p>
                </div>
              )}

              {/* Required & Preferred Skills */}
              <div>
                <h2 className="text-base font-bold text-slate-900 mb-3">Key Technologies & Skills</h2>
                <div className="space-y-3">
                  <div>
                    <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1.5">
                      Required Skills
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {job.required_skills.map((s) => (
                        <span
                          key={s}
                          className="px-2.5 py-1 text-xs font-semibold rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-100"
                        >
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>

                  {job.preferred_skills.length > 0 && (
                    <div>
                      <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1.5">
                        Preferred / Bonus
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {job.preferred_skills.map((s) => (
                          <span
                            key={s}
                            className="px-2.5 py-1 text-xs font-medium rounded-lg bg-slate-100 text-slate-700"
                          >
                            {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Experience & Education */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4 border-t border-slate-100 text-xs">
                <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                  <span className="font-semibold text-slate-500 block mb-0.5">Experience Level</span>
                  <span className="font-bold text-slate-800">{job.experience_text || 'Not specified'}</span>
                  {job.eligible_for_fresher && (
                    <span className="block text-emerald-700 font-medium mt-1">
                      ✓ Fresh graduates welcome
                    </span>
                  )}
                </div>

                <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                  <span className="font-semibold text-slate-500 block mb-0.5">Education Requirements</span>
                  <span className="font-bold text-slate-800">{job.education_text || "Bachelor's degree or equivalent"}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Persistent Match Panel & Actions (Section 85) */}
        <div className="space-y-5 lg:sticky lg:top-24">
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-card space-y-5">
            {/* Match score hero */}
            {scoreStyle && explanation && (
              <div className={`p-5 rounded-2xl border ${scoreStyle.border} ${scoreStyle.bg}`}>
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-semibold opacity-75 uppercase tracking-wider">
                      ZyncRole Compatibility
                    </span>
                    <div className="text-xl font-bold mt-0.5">{scoreStyle.label}</div>
                  </div>
                  <div className="text-3xl font-extrabold tracking-tight">
                    {Math.round(explanation.match_score)}%
                  </div>
                </div>
                <p className="mt-2.5 text-xs leading-relaxed border-t border-current/10 pt-2.5">
                  {explanation.explanation}
                </p>
                <button
                  type="button"
                  onClick={() => setIsDrawerOpen(true)}
                  className="mt-3 text-xs font-bold underline hover:opacity-80 block"
                >
                  View full dimension breakdown →
                </button>
              </div>
            )}

            {/* Matched skills summary */}
            {explanation && explanation.matched_skills.length > 0 && (
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2 flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Matched from your profile</span>
                </h3>
                <div className="flex flex-wrap gap-1.5">
                  {explanation.matched_skills.map((s) => (
                    <span
                      key={s}
                      className="px-2 py-0.5 text-xs font-medium rounded-md bg-emerald-50 text-emerald-700 border border-emerald-100"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Missing skills summary */}
            {explanation && explanation.missing_required_skills.length > 0 && (
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2 flex items-center gap-1.5">
                  <AlertCircle className="w-3.5 h-3.5 text-amber-500" />
                  <span>Missing required skills</span>
                </h3>
                <div className="flex flex-wrap gap-1.5">
                  {explanation.missing_required_skills.map((s) => (
                    <span
                      key={s}
                      className="px-2 py-0.5 text-xs font-medium rounded-md bg-amber-50 text-amber-800 border border-amber-200"
                    >
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Primary Action Buttons */}
            <div className="space-y-2.5 pt-2">
              <a
                href={ensureAbsoluteUrl(job.apply_url)}
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => setShowApplyFeedback(true)}
                className="w-full inline-flex items-center justify-center px-5 py-3 text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-subtle transition text-center"
              >
                <span>Apply on {job.source_name || job.source_id.toUpperCase()}</span>
                <ExternalLink className="w-4 h-4 ml-1.5" />
              </a>

              <button
                type="button"
                onClick={handleSaveToggle}
                disabled={isSaving}
                className={`w-full inline-flex items-center justify-center px-4 py-2.5 text-xs font-semibold rounded-xl border transition ${
                  isSaved
                    ? 'bg-brand-50 border-brand-200 text-brand-700'
                    : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Bookmark className={`w-3.5 h-3.5 mr-1.5 ${isSaved ? 'fill-current' : ''}`} />
                <span>{isSaved ? 'Saved in Opportunities' : 'Save Opportunity'}</span>
              </button>
            </div>

            <div className="text-[11px] text-slate-400 flex items-center space-x-1 pt-1">
              <ShieldCheck className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>
                Redirects securely to the official posting portal without altering application data.
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Lightweight Prompt after clicking Apply */}
      {showApplyFeedback && (
        <div className="fixed bottom-6 right-6 z-50 p-4 bg-white rounded-2xl shadow-float border border-slate-200 max-w-sm animate-fade-in">
          <p className="text-xs font-semibold text-slate-800">
            Did you submit your application to {job.company}?
          </p>
          <div className="flex justify-end gap-2 mt-3">
            <button
              onClick={() => handleConfirmApplied(false)}
              className="px-2.5 py-1 text-xs text-slate-500 hover:bg-slate-100 rounded-md"
            >
              Not yet
            </button>
            <button
              onClick={() => handleConfirmApplied(true)}
              className="px-3 py-1 text-xs font-medium text-white bg-brand-600 hover:bg-brand-700 rounded-md shadow-subtle"
            >
              Yes, track it
            </button>
          </div>
        </div>
      )}

      {/* Match Explanation Drawer */}
      <MatchExplanationDrawer
        isOpen={isDrawerOpen}
        onClose={() => setIsDrawerOpen(false)}
        explanation={explanation}
        jobTitle={job.title}
        company={job.company}
        applyUrl={job.apply_url}
        sourceName={job.source_name || job.source_id.toUpperCase()}
      />
    </div>
  )
}
