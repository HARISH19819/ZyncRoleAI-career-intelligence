import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { ResumeAnalysis } from '@/types'
import { ExternalResumeBuilderButton } from '@/components/ExternalResumeBuilderButton'
import {
  ArrowLeft,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  TrendingUp,
  FileText,
  ShieldCheck,
  Check,
  Upload
} from 'lucide-react'

export const ResumeAnalysisPage: React.FC = () => {
  const [analysis, setAnalysis] = useState<ResumeAnalysis | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAnalysis = async () => {
      setIsLoading(true)
      try {
        const res = await api.get<ResumeAnalysis>('/resume/analysis')
        setAnalysis(res)
      } catch (err: any) {
        setError(err.message || 'No resume analysis available.')
      } finally {
        setIsLoading(false)
      }
    }
    fetchAnalysis()
  }, [])

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto px-4 py-16 text-center animate-pulse">
        <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-xs text-slate-500">Evaluating ATS criteria...</span>
      </div>
    )
  }

  if (error || !analysis) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center">
        <FileText className="w-12 h-12 text-slate-300 mx-auto mb-3" />
        <h2 className="text-lg font-bold text-slate-800">No Resume Analysis Available</h2>
        <p className="text-xs text-slate-500 mt-1">Please upload a resume first to view the ATS evaluation.</p>
        <Link
          to="/resume"
          className="mt-4 inline-flex items-center px-4 py-2 bg-brand-600 text-white rounded-xl text-xs font-semibold"
        >
          <Upload className="w-3.5 h-3.5 mr-1.5" />
          <span>Upload Resume</span>
        </Link>
      </div>
    )
  }

  const breakdownItems = [
    { label: 'Technical Keyword & Skill Coverage', score: analysis.breakdown.keyword_score, max: 25 },
    { label: 'Target Role Relevance', score: analysis.breakdown.role_relevance_score, max: 20 },
    { label: 'Section Completeness (Standard ATS)', score: analysis.breakdown.section_score, max: 15 },
    { label: 'Project & Experience Substance', score: analysis.breakdown.project_score, max: 15 },
    { label: 'Formatting & Machine Readability', score: analysis.breakdown.formatting_score, max: 10 },
    { label: 'Quantified Results & Metrics Evidence', score: analysis.breakdown.achievement_score, max: 10 },
    { label: 'Contact & Repository Profile Details', score: analysis.breakdown.contact_score, max: 5 },
  ]

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 animate-fade-in">
      {/* Back link */}
      <div>
        <Link
          to="/resume"
          className="inline-flex items-center text-xs font-semibold text-slate-500 hover:text-slate-800 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5 mr-1" />
          <span>Back to Resume Center</span>
        </Link>
      </div>

      {/* Hero ATS Score Header */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-card flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2.5 py-1 rounded-md">
            ZyncRole ATS Readiness
          </span>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight mt-2">
            ATS Compatibility Score
          </h1>
          <p className="text-xs text-slate-500 mt-1 max-w-xl">
            Calculated across 7 structural and keyword dimensions based on standard automated tracking heuristics.
          </p>
        </div>

        <div className="flex items-center gap-4">
          <div className="text-center sm:text-right">
            <div className="text-4xl sm:text-5xl font-extrabold text-brand-600">
              {Math.round(analysis.ats_score)}
              <span className="text-lg text-slate-400 font-normal">/100</span>
            </div>
            <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
              High Compatibility
            </span>
          </div>
          <div className="hidden sm:block pl-4 border-l border-slate-100">
            <ExternalResumeBuilderButton label="Build ATS Template" variant="primary" className="text-xs py-2 px-3" />
          </div>
        </div>
      </div>

      {/* 2-column: Strengths & Improvements */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-3">
          <h2 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>Strengths & Strong Areas</span>
          </h2>
          <ul className="space-y-2 text-xs text-slate-600">
            {analysis.strengths.map((str, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-emerald-500 mt-0.5">•</span>
                <span className="font-medium text-slate-700">{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Improvement Areas */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-3">
          <h2 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
            <AlertCircle className="w-4 h-4 text-amber-500" />
            <span>Opportunities for Improvement</span>
          </h2>
          <ul className="space-y-2 text-xs text-slate-600">
            {analysis.weaknesses.map((weak, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-amber-500 mt-0.5">•</span>
                <span>{weak}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Detailed Dimension Breakdown */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-subtle space-y-5">
        <div>
          <h2 className="text-base font-bold text-slate-900">Score Breakdown by Heuristic</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Each weight is mathematically verified and never fabricated.
          </p>
        </div>

        <div className="space-y-4">
          {breakdownItems.map((item) => {
            const pct = Math.round((item.score / item.max) * 100)
            return (
              <div key={item.label} className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="font-semibold text-slate-700">{item.label}</span>
                  <span className="font-bold text-slate-800">
                    {item.score} / {item.max} pts ({pct}%)
                  </span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-brand-600 h-full rounded-full transition-all duration-500"
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Detected Technical Keywords */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-subtle space-y-4">
        <div>
          <h2 className="text-base font-bold text-slate-900">Detected Technical Competencies</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            These keywords directly drive your job matching engine compatibility.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          {analysis.detected_skills.map((skill) => (
            <span
              key={skill}
              className="px-3 py-1 text-xs font-semibold rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-100"
            >
              {skill}
            </span>
          ))}
        </div>
      </div>

      {/* Footer CTAs */}
      <div className="p-6 bg-slate-50 rounded-2xl border border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <p className="text-xs font-bold text-slate-800">Ready to boost your compatibility?</p>
          <p className="text-xs text-slate-500">Use our free ATS builder integration to optimize your formatting.</p>
        </div>
        <div className="flex items-center gap-3">
          <Link
            to="/resume"
            className="px-4 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-xl hover:bg-slate-50"
          >
            Update Resume
          </Link>
          <ExternalResumeBuilderButton label="Create ATS-Friendly Resume" variant="primary" />
        </div>
      </div>
    </div>
  )
}
