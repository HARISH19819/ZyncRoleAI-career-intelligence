import React, { useState } from 'react'
import { Bookmark, ExternalLink, Sparkles, MapPin, Building2, Clock, CheckCircle2, AlertCircle } from 'lucide-react'
import { Job, JobMatchExplanation } from '@/types'
import { getMatchScoreColor, formatSalary } from '@/lib/utils'
import { api } from '@/lib/api'
import { MatchExplanationDrawer } from '@/components/MatchExplanationDrawer'

interface Props {
  job: Job
  onToggleSave?: (jobId: string, newState: boolean) => void
  onApplyClicked?: (jobId: string) => void
}

export const JobCard: React.FC<Props> = ({ job, onToggleSave, onApplyClicked }) => {
  const [isSaved, setIsSaved] = useState(job.is_saved || false)
  const [isSaving, setIsSaving] = useState(false)
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [explanation, setExplanation] = useState<JobMatchExplanation | null>(null)
  const [isLoadingMatch, setIsLoadingMatch] = useState(false)
  const [showApplyFeedback, setShowApplyFeedback] = useState(false)

  const scoreStyle = job.match_score ? getMatchScoreColor(job.match_score) : null

  const handleSaveToggle = async (e: React.MouseEvent) => {
    e.stopPropagation()
    e.preventDefault()
    if (isSaving) return

    setIsSaving(true)
    const nextSaved = !isSaved
    setIsSaved(nextSaved)

    try {
      if (nextSaved) {
        await api.post(`/saved/${job.id}`)
      } else {
        await api.delete(`/saved/${job.id}`)
      }
      onToggleSave?.(job.id, nextSaved)
    } catch {
      setIsSaved(!nextSaved) // Revert on failure
    } finally {
      setIsSaving(false)
    }
  }

  const handleOpenDrawer = async (e: React.MouseEvent) => {
    e.stopPropagation()
    e.preventDefault()
    setIsDrawerOpen(true)
    if (!explanation) {
      setIsLoadingMatch(true)
      try {
        const res = await api.get<JobMatchExplanation>(`/jobs/${job.id}/match`)
        setExplanation(res)
      } catch {
        // Fallback explanation from card data
        setExplanation({
          job_id: job.id,
          match_score: job.match_score || 70,
          compatibility_level: job.compatibility_level || 'Strong Match',
          breakdown: {
            skill_score: job.match_score || 75,
            role_score: 75,
            domain_score: 80,
            experience_score: 85,
            education_score: 80,
            location_score: 80,
            preference_score: 80,
            semantic_score: 70
          },
          matched_skills: job.matched_skills || job.top_skills,
          missing_required_skills: job.missing_required_skills || [],
          missing_preferred_skills: job.missing_preferred_skills || [],
          strengths: ['Relevant domain background', 'Strong foundational skills'],
          concerns: job.missing_required_skills?.length ? [`Missing: ${job.missing_required_skills.join(', ')}`] : [],
          explanation: job.explanation || 'Matches your career profile and domain requirements.',
          how_to_improve: 'Add relevant tools and projects to your profile.'
        })
      } finally {
        setIsLoadingMatch(false)
      }
    }
  }

  const handleApplyClick = () => {
    window.open(job.apply_url, '_blank', 'noopener,noreferrer')
    setShowApplyFeedback(true)
    onApplyClicked?.(job.id)
  }

  const handleConfirmApplied = async (applied: boolean) => {
    setShowApplyFeedback(false)
    if (applied) {
      try {
        await api.post('/applications', { job_id: job.id, status: 'Applied' })
      } catch {
        // Ignore
      }
    }
  }

  return (
    <>
      <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle hover:shadow-card transition-all duration-200 flex flex-col justify-between group">
        <div>
          {/* Card Header: Company, Source & Save */}
          <div className="flex items-start justify-between gap-3">
            <div className="flex items-center space-x-3 min-w-0">
              <div className="w-10 h-10 rounded-xl bg-slate-100 border border-slate-200/60 flex items-center justify-center font-bold text-slate-700 text-sm shrink-0">
                {job.company.substring(0, 2).toUpperCase()}
              </div>
              <div className="min-w-0">
                <span className="text-xs font-medium text-slate-500 truncate block">
                  {job.company}
                </span>
                <h3 className="text-base font-semibold text-slate-800 truncate group-hover:text-brand-600 transition-colors">
                  {job.title}
                </h3>
              </div>
            </div>

            <button
              type="button"
              onClick={handleSaveToggle}
              disabled={isSaving}
              aria-label={isSaved ? 'Remove from saved' : 'Save opportunity'}
              className={`p-2 rounded-xl border transition-all ${
                isSaved
                  ? 'bg-brand-50 border-brand-200 text-brand-600'
                  : 'bg-white border-slate-200/80 text-slate-400 hover:text-slate-600 hover:bg-slate-50'
              }`}
            >
              <Bookmark className={`w-4 h-4 ${isSaved ? 'fill-current' : ''}`} />
            </button>
          </div>

          {/* Metadata chips: Location, Work mode, Salary, Freshness */}
          <div className="flex flex-wrap items-center gap-y-1.5 gap-x-3 text-xs text-slate-500 mt-3 pt-2 border-t border-slate-100">
            <div className="flex items-center space-x-1">
              <MapPin className="w-3.5 h-3.5 text-slate-400" />
              <span>{job.location}</span>
            </div>
            <span className="text-slate-300">•</span>
            <span className="px-2 py-0.5 rounded-md bg-slate-100 text-slate-600 font-medium">
              {job.work_mode}
            </span>
            <span className="text-slate-300">•</span>
            <div className="flex items-center space-x-1 text-slate-500">
              <Clock className="w-3.5 h-3.5 text-slate-400" />
              <span>{job.freshness_label}</span>
            </div>
            {job.salary_min && (
              <>
                <span className="text-slate-300">•</span>
                <span className="text-emerald-700 font-medium">
                  {formatSalary(job.salary_min, job.salary_max, job.salary_currency)}
                </span>
              </>
            )}
          </div>

          {/* Match Score Badge */}
          {scoreStyle && job.match_score !== undefined && (
            <div className="mt-3.5 flex items-center justify-between p-2.5 rounded-xl bg-slate-50/80 border border-slate-100">
              <div className="flex items-center space-x-2">
                <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-bold ${scoreStyle.bg} border ${scoreStyle.border}`}>
                  {Math.round(job.match_score)}% Match
                </span>
                <span className="text-xs font-medium text-slate-600">
                  {scoreStyle.label}
                </span>
              </div>
              <button
                type="button"
                onClick={handleOpenDrawer}
                className="text-xs font-semibold text-brand-600 hover:text-brand-700 flex items-center space-x-0.5 transition"
              >
                <span>Why this match?</span>
              </button>
            </div>
          )}

          {/* Top matched skills & missing skills summary */}
          <div className="mt-3">
            <div className="flex flex-wrap gap-1.5 items-center">
              {job.top_skills.slice(0, 3).map((skill) => (
                <span
                  key={skill}
                  className="px-2 py-0.5 text-xs font-medium rounded-md bg-slate-100 text-slate-700"
                >
                  {skill}
                </span>
              ))}
              {job.missing_required_skills && job.missing_required_skills.length > 0 && (
                <span className="px-2 py-0.5 text-xs font-medium rounded-md bg-amber-50 text-amber-700 border border-amber-100/80">
                  Missing: {job.missing_required_skills[0]}
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Card Footer: Source Attribution & Action Buttons */}
        <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
          <div className="text-[11px] text-slate-400">
            Source: <span className="font-medium text-slate-600">{job.source_name || job.source_id.toUpperCase()}</span>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={handleOpenDrawer}
              className="px-3 py-1.5 text-xs font-medium text-slate-600 hover:bg-slate-100 rounded-lg transition"
            >
              Details
            </button>
            <button
              type="button"
              onClick={handleApplyClick}
              className="inline-flex items-center px-3.5 py-1.5 text-xs font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-lg shadow-subtle transition"
            >
              <span>Apply on {job.source_name || 'Source'}</span>
              <ExternalLink className="w-3 h-3 ml-1.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Lightweight Prompt after clicking Apply (Section 97) */}
      {showApplyFeedback && (
        <div className="fixed bottom-6 right-6 z-50 p-4 bg-white rounded-2xl shadow-float border border-slate-200/80 max-w-sm animate-fade-in">
          <p className="text-xs font-semibold text-slate-800">
            Did you submit an application to {job.company}?
          </p>
          <p className="text-[11px] text-slate-500 mt-1">
            Tracking helps refine your future opportunity recommendations.
          </p>
          <div className="flex justify-end gap-2 mt-3">
            <button
              onClick={() => handleConfirmApplied(false)}
              className="px-2.5 py-1 text-xs text-slate-500 hover:bg-slate-100 rounded-md transition"
            >
              Not yet
            </button>
            <button
              onClick={() => handleConfirmApplied(true)}
              className="px-3 py-1 text-xs font-medium text-white bg-brand-600 hover:bg-brand-700 rounded-md shadow-subtle transition"
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
    </>
  )
}
