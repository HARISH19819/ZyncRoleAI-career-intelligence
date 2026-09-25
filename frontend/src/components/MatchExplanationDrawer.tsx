import React from 'react'
import { X, CheckCircle2, AlertCircle, ArrowUpRight, ShieldCheck, Sparkles, TrendingUp } from 'lucide-react'
import { JobMatchExplanation } from '@/types'
import { getMatchScoreColor } from '@/lib/utils'

interface Props {
  isOpen: boolean
  onClose: () => void
  explanation: JobMatchExplanation | null
  jobTitle: string
  company: string
  applyUrl: string
  sourceName?: string
}

export const MatchExplanationDrawer: React.FC<Props> = ({
  isOpen,
  onClose,
  explanation,
  jobTitle,
  company,
  applyUrl,
  sourceName = 'Source'
}) => {
  if (!isOpen || !explanation) return null

  const scoreStyle = getMatchScoreColor(explanation.match_score)

  const breakdownItems = [
    { label: 'Skill Match', score: explanation.breakdown.skill_score, weight: '25%' },
    { label: 'Role Alignment', score: explanation.breakdown.role_score, weight: '15%' },
    { label: 'Domain Relevance', score: explanation.breakdown.domain_score, weight: '15%' },
    { label: 'Experience Fit', score: explanation.breakdown.experience_score, weight: '15%' },
    { label: 'Education Alignment', score: explanation.breakdown.education_score, weight: '10%' },
    { label: 'Semantic Similarity', score: explanation.breakdown.semantic_score, weight: '10%' },
    { label: 'Location & Work Mode', score: explanation.breakdown.location_score, weight: '5%' },
    { label: 'Preferences', score: explanation.breakdown.preference_score, weight: '5%' },
  ]

  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-slate-900/30 backdrop-blur-xs transition-opacity"
        onClick={onClose}
      />

      <div className="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div className="w-screen max-w-lg bg-white shadow-2xl border-l border-slate-100 flex flex-col animate-fade-in">
          {/* Header */}
          <div className="p-6 border-b border-slate-100 flex items-start justify-between bg-slate-50/50">
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2 py-0.5 rounded">
                  AI Match Intelligence
                </span>
                <span className="text-xs text-slate-500">Verified factual facts</span>
              </div>
              <h2 className="text-xl font-bold text-slate-800 mt-2">{jobTitle}</h2>
              <p className="text-sm text-slate-600">{company}</p>
            </div>
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Scrollable Content */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {/* Top Match Score Card */}
            <div className={`p-5 rounded-2xl border ${scoreStyle.border} ${scoreStyle.bg}`}>
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-medium uppercase tracking-wider opacity-75">
                    Compatibility Level
                  </span>
                  <div className="text-2xl font-bold mt-0.5">{scoreStyle.label}</div>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-extrabold tracking-tight">
                    {Math.round(explanation.match_score)}%
                  </div>
                  <span className="text-xs opacity-75">ZyncRole Compatibility</span>
                </div>
              </div>
              <p className="mt-3 text-sm leading-relaxed border-t border-current/10 pt-3">
                {explanation.explanation}
              </p>
            </div>

            {/* Matched Skills */}
            <div>
              <h3 className="text-sm font-semibold text-slate-800 flex items-center gap-1.5 mb-2.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                <span>Matched Skills ({explanation.matched_skills.length})</span>
              </h3>
              {explanation.matched_skills.length > 0 ? (
                <div className="flex flex-wrap gap-1.5">
                  {explanation.matched_skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2.5 py-1 text-xs font-medium rounded-md bg-emerald-50 text-emerald-700 border border-emerald-100"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-slate-500">No overlapping primary skills detected yet.</p>
              )}
            </div>

            {/* Missing Skills */}
            {(explanation.missing_required_skills.length > 0 || explanation.missing_preferred_skills.length > 0) && (
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-slate-800 flex items-center gap-1.5">
                  <AlertCircle className="w-4 h-4 text-amber-500" />
                  <span>Identified Skill Gaps</span>
                </h3>

                {explanation.missing_required_skills.length > 0 && (
                  <div>
                    <span className="text-xs text-slate-500 font-medium block mb-1">
                      Required for role:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {explanation.missing_required_skills.map((skill) => (
                        <span
                          key={skill}
                          className="px-2.5 py-1 text-xs font-medium rounded-md bg-amber-50 text-amber-800 border border-amber-200"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {explanation.missing_preferred_skills.length > 0 && (
                  <div>
                    <span className="text-xs text-slate-500 font-medium block mb-1">
                      Preferred / bonus:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {explanation.missing_preferred_skills.map((skill) => (
                        <span
                          key={skill}
                          className="px-2.5 py-1 text-xs font-medium rounded-md bg-slate-100 text-slate-700"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Dimension Breakdown */}
            <div>
              <h3 className="text-sm font-semibold text-slate-800 flex items-center gap-1.5 mb-3">
                <TrendingUp className="w-4 h-4 text-brand-600" />
                <span>Score Breakdown by Dimension</span>
              </h3>
              <div className="space-y-2.5 bg-slate-50 p-4 rounded-xl border border-slate-100">
                {breakdownItems.map((item) => (
                  <div key={item.label} className="text-xs">
                    <div className="flex justify-between text-slate-700 mb-1 font-medium">
                      <span>{item.label} <span className="text-slate-400 font-normal">({item.weight})</span></span>
                      <span>{Math.round(item.score)}%</span>
                    </div>
                    <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                      <div
                        className="bg-brand-600 h-full rounded-full transition-all duration-500"
                        style={{ width: `${Math.min(100, Math.max(0, item.score))}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* How to improve match */}
            {explanation.how_to_improve && (
              <div className="p-4 rounded-xl bg-blue-50/70 border border-blue-100 text-xs text-blue-900 leading-relaxed">
                <div className="flex items-center space-x-1.5 font-semibold text-blue-800 mb-1">
                  <Sparkles className="w-4 h-4 text-blue-600" />
                  <span>How to improve your compatibility</span>
                </div>
                <p>{explanation.how_to_improve}</p>
              </div>
            )}

            {/* Transparency Note */}
            <div className="text-[11px] text-slate-400 flex items-center space-x-1 pt-2">
              <ShieldCheck className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span>
                Scores are deterministic estimates calculated from listed job specifications and your current profile.
              </span>
            </div>
          </div>

          {/* Footer CTA */}
          <div className="p-4 border-t border-slate-100 bg-slate-50 flex items-center justify-between gap-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-200 rounded-lg transition"
            >
              Close
            </button>
            <a
              href={applyUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center px-5 py-2 text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-lg shadow-subtle transition"
            >
              <span>Apply on {sourceName}</span>
              <ArrowUpRight className="w-4 h-4 ml-1.5" />
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
