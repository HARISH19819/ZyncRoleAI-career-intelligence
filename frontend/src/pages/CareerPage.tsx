import React, { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { CareerInsights } from '@/types'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from 'recharts'
import {
  TrendingUp,
  PieChart as PieIcon,
  AlertCircle,
  RefreshCw
} from 'lucide-react'

export const CareerPage: React.FC = () => {
  const [data, setData] = useState<CareerInsights | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const fetchInsights = async () => {
    setIsLoading(true)
    try {
      const res = await api.get<CareerInsights>('/career/insights')
      setData(res)
    } catch {
      setData(null)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchInsights()
  }, [])

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto px-4 py-16 text-center animate-pulse">
        <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-xs text-slate-500">Aggregating real-time career market metrics...</span>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center">
        <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center mx-auto mb-4">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="text-lg font-bold text-slate-800">Career Insights Unavailable</h2>
        <p className="mt-2 text-sm text-slate-500">
          We could not load real-time market metrics right now. Please verify your connection or try again.
        </p>
        <button
          onClick={fetchInsights}
          className="mt-5 inline-flex items-center px-4 py-2 text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-xl transition"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          <span>Retry</span>
        </button>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Header (Section 50 & 154) */}
      <div className="pb-4 border-b border-slate-200/60">
        <div className="flex items-center space-x-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-brand-600 bg-brand-50 px-2.5 py-1 rounded-md">
            Market Intelligence
          </span>
          <span className="text-xs text-slate-400">
            Computed from {data.total_jobs} active market opportunities
          </span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight mt-2">
          Understand the market you want to enter
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-2xl">
          {data.user_skill_coverage_summary}
        </p>
      </div>

      {/* Top 3 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Total Market Jobs
          </span>
          <div className="text-2xl font-extrabold text-slate-900 mt-1">{data.total_jobs}</div>
          <span className="text-xs text-slate-400 mt-1 block">Live & verified listings</span>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Fresher Friendly Ratio
          </span>
          <div className="text-2xl font-extrabold text-emerald-600 mt-1">
            {data.fresher_friendly_percentage}%
          </div>
          <span className="text-xs text-slate-400 mt-1 block">Welcoming 0-1 yrs experience</span>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            Domain Focus
          </span>
          <div className="text-2xl font-extrabold text-brand-600 mt-1">
            {data.domain_distribution[0]?.name || 'Technology'}
          </div>
          <span className="text-xs text-slate-400 mt-1 block">Highest opportunity density</span>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Most Requested Skills (Horizontal Bar Chart) */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">Most Requested Skills</h2>
              <p className="text-xs text-slate-500 mt-0.5">Frequency across collected listings</p>
            </div>
            <TrendingUp className="w-5 h-5 text-brand-600" />
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data.top_skills}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
              >
                <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fontSize: 11 }} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 11 }} width={80} />
                <Tooltip
                  formatter={(value: any) => [`${value}% of jobs`, 'Frequency']}
                  contentStyle={{ borderRadius: '12px', fontSize: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
                />
                <Bar dataKey="percentage" fill="#6366f1" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Domain Distribution (Pie / Bar) */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-slate-900">Opportunities by Domain</h2>
              <p className="text-xs text-slate-500 mt-0.5">Share of open listings by sector</p>
            </div>
            <PieIcon className="w-5 h-5 text-brand-600" />
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={data.domain_distribution.slice(0, 6)}
                margin={{ top: 10, right: 10, left: -20, bottom: 25 }}
              >
                <XAxis dataKey="name" angle={-20} textAnchor="end" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip
                  formatter={(val: any) => [`${val} postings`, 'Volume']}
                  contentStyle={{ borderRadius: '12px', fontSize: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.08)' }}
                />
                <Bar dataKey="count" fill="#10b981" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Work Mode & Location Distribution */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-3">
          <h3 className="text-sm font-bold text-slate-800">Work Mode Flexibility</h3>
          <div className="space-y-3">
            {data.work_mode_distribution.map((mode) => (
              <div key={mode.name} className="space-y-1 text-xs">
                <div className="flex justify-between font-medium text-slate-700">
                  <span>{mode.name}</span>
                  <span className="text-slate-500">{mode.count} jobs ({mode.percentage}%)</span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div className="bg-blue-600 h-full rounded-full" style={{ width: `${mode.percentage}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-3">
          <h3 className="text-sm font-bold text-slate-800">Top Opportunity Hubs</h3>
          <div className="space-y-3">
            {data.location_trends.slice(0, 4).map((loc) => (
              <div key={loc.name} className="space-y-1 text-xs">
                <div className="flex justify-between font-medium text-slate-700">
                  <span>{loc.name}</span>
                  <span className="text-slate-500">{loc.count} jobs ({loc.percentage}%)</span>
                </div>
                <div className="w-full bg-slate-100 h-2 rounded-full overflow-hidden">
                  <div className="bg-brand-600 h-full rounded-full" style={{ width: `${loc.percentage}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
