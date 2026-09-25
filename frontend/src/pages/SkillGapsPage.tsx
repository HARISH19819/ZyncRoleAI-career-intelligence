import React, { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { SkillGapResponse, SkillGapItem } from '@/types'
import {
  Layers,
  Sparkles,
  AlertCircle,
  TrendingUp,
  CheckCircle2,
  ArrowRight
} from 'lucide-react'
import { Link } from 'react-router-dom'

export const SkillGapsPage: React.FC = () => {
  const [data, setData] = useState<SkillGapResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const fetchGaps = async () => {
      setIsLoading(true)
      try {
        const res = await api.get<SkillGapResponse>('/skill-gaps')
        setData(res)
      } catch {
        setData(null)
      } finally {
        setIsLoading(false)
      }
    }
    fetchGaps()
  }, [])

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16 text-center animate-pulse">
        <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-xs text-slate-500">Calculating target opportunity skill gaps...</span>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Page Header (Section 48) */}
      <div className="pb-4 border-b border-slate-200/60">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-amber-700 bg-amber-50 px-2.5 py-1 rounded-md">
            Market Gap Analysis
          </span>
          <span className="text-xs text-slate-400">
            Based on {data?.target_jobs_analyzed || 0} target opportunities
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight mt-2">
          What is holding back your matches?
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
          {data?.insights_summary ||
            'These are the technical skills appearing most frequently across your targeted roles that were not detected in your current profile.'}
        </p>
      </div>

      {/* Main Skill Gaps Grid */}
      {data && data.top_missing_skills.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {data.top_missing_skills.map((gap) => {
            const isHigh = gap.impact === 'High'
            const isMedium = gap.impact === 'Medium'

            return (
              <div
                key={gap.skill}
                className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle flex flex-col justify-between hover:shadow-card transition"
              >
                <div>
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                        {gap.category}
                      </span>
                      <h3 className="text-lg font-bold text-slate-900 mt-0.5">{gap.skill}</h3>
                    </div>

                    <span
                      className={`text-xs px-2.5 py-1 rounded-lg font-bold ${
                        isHigh
                          ? 'bg-rose-50 text-rose-700 border border-rose-100'
                          : isMedium
                          ? 'bg-amber-50 text-amber-800 border border-amber-200'
                          : 'bg-slate-100 text-slate-700'
                      }`}
                    >
                      {gap.impact} Impact
                    </span>
                  </div>

                  {/* Percentage Bar */}
                  <div className="mt-4 space-y-1.5">
                    <div className="flex justify-between text-xs text-slate-600">
                      <span>Found in target listings:</span>
                      <span className="font-bold text-slate-800">{gap.frequency_percentage}%</span>
                    </div>
                    <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                      <div
                        className={`h-full rounded-full ${
                          isHigh ? 'bg-rose-500' : isMedium ? 'bg-amber-500' : 'bg-slate-400'
                        }`}
                        style={{ width: `${Math.min(100, gap.frequency_percentage)}%` }}
                      />
                    </div>
                  </div>

                  <p className="text-xs text-slate-500 mt-3 leading-relaxed">
                    Required by <strong>{gap.target_job_count}</strong> active target opportunities. Adding project or coursework evidence of {gap.skill} will directly enhance your compatibility.
                  </p>
                </div>

                <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="text-slate-400">Status: <span className="font-medium text-amber-700">Missing from resume</span></span>
                  <Link
                    to="/profile"
                    className="text-brand-600 font-semibold hover:underline flex items-center"
                  >
                    <span>Add to profile</span>
                    <ArrowRight className="w-3 h-3 ml-1" />
                  </Link>
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        <div className="bg-white rounded-3xl border border-slate-200/80 p-12 text-center max-w-lg mx-auto">
          <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto mb-3" />
          <h2 className="text-base font-bold text-slate-800">No Significant Skill Gaps Detected</h2>
          <p className="text-xs text-slate-500 mt-1">
            Your profile currently covers the key skills found across your selected opportunities.
          </p>
          <Link
            to="/jobs"
            className="mt-4 inline-flex items-center px-4 py-2 bg-brand-600 text-white rounded-xl text-xs font-semibold"
          >
            <span>Explore Opportunities</span>
          </Link>
        </div>
      )}
    </div>
  )
}
