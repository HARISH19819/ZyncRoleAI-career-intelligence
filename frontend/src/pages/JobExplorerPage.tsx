import React, { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { Job } from '@/types'
import { JobCard } from '@/components/JobCard'
import { JobCardSkeleton } from '@/components/SkeletonLoader'
import {
  Search,
  Filter,
  SlidersHorizontal,
  X,
  Briefcase,
  CheckCircle2
} from 'lucide-react'

export const JobExplorerPage: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [selectedDomain, setSelectedDomain] = useState<string>('All')
  const [selectedWorkMode, setSelectedWorkMode] = useState<string>('All')
  const [selectedEmpType, setSelectedEmpType] = useState<string>('All')
  const [fresherOnly, setFresherOnly] = useState(false)
  const [sortBy, setSortBy] = useState('match_score')
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false)

  const domains = [
    'All',
    'Machine Learning',
    'Artificial Intelligence',
    'Data Science',
    'Full Stack Development',
    'Frontend Development',
    'Backend Development',
    'Cloud Computing',
    'Cybersecurity'
  ]

  // Debounce search input
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(searchQuery)
    }, 300)
    return () => clearTimeout(handler)
  }, [searchQuery])

  useEffect(() => {
    const fetchJobs = async () => {
      setIsLoading(true)
      try {
        const params = new URLSearchParams()
        if (debouncedQuery.trim()) params.append('q', debouncedQuery.trim())
        if (selectedDomain !== 'All') params.append('domain', selectedDomain)
        if (selectedWorkMode !== 'All') params.append('work_mode', selectedWorkMode)
        if (selectedEmpType !== 'All') params.append('employment_type', selectedEmpType)
        if (fresherOnly) params.append('fresher_only', 'true')
        params.append('sort', sortBy)

        const res = await api.get<Job[]>(`/jobs?${params.toString()}`)
        setJobs(res)
      } catch {
        setJobs([])
      } finally {
        setIsLoading(false)
      }
    }

    fetchJobs()
  }, [debouncedQuery, selectedDomain, selectedWorkMode, selectedEmpType, fresherOnly, sortBy])

  const handleClearFilters = () => {
    setSearchQuery('')
    setSelectedDomain('All')
    setSelectedWorkMode('All')
    setSelectedEmpType('All')
    setFresherOnly(false)
    setSortBy('match_score')
  }

  const hasActiveFilters =
    searchQuery ||
    selectedDomain !== 'All' ||
    selectedWorkMode !== 'All' ||
    selectedEmpType !== 'All' ||
    fresherOnly

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 animate-fade-in">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200/60">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Explore Opportunities
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            {isLoading ? 'Scanning opportunities...' : `${jobs.length} verified opportunities matching criteria`}
          </p>
        </div>

        {/* Sort & Mobile Filter Toggle */}
        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => setMobileFilterOpen(!mobileFilterOpen)}
            className="md:hidden inline-flex items-center px-3 py-2 text-xs font-semibold text-slate-700 bg-white border border-slate-200 rounded-xl"
          >
            <Filter className="w-3.5 h-3.5 mr-1.5" />
            <span>Filters</span>
          </button>

          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-500 hidden sm:inline">Sort by:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-white border border-slate-200 text-slate-700 text-xs font-medium rounded-xl px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
            >
              <option value="match_score">Highest Match</option>
              <option value="newest">Newest First</option>
              <option value="salary">Highest Compensation</option>
            </select>
          </div>
        </div>
      </div>

      {/* Search Input Bar */}
      <div className="relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search roles, skills, or companies (e.g. Python, Machine Learning Intern, DeepPulse)..."
          className="w-full pl-10 pr-10 py-3 rounded-2xl bg-white border border-slate-200 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600 shadow-subtle transition"
        />
        {searchQuery && (
          <button
            onClick={() => setSearchQuery('')}
            className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Filter Row (Desktop) */}
      <div className="hidden md:flex flex-wrap items-center justify-between gap-3 bg-white p-3.5 rounded-2xl border border-slate-200/80 shadow-subtle">
        {/* Domain Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5">
          {domains.slice(0, 7).map((dom) => (
            <button
              key={dom}
              type="button"
              onClick={() => setSelectedDomain(dom)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium transition ${
                selectedDomain === dom
                  ? 'bg-brand-600 text-white shadow-xs font-semibold'
                  : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200/70'
              }`}
            >
              {dom}
            </button>
          ))}
        </div>

        {/* Secondary Selects */}
        <div className="flex items-center gap-2">
          {/* Work Mode */}
          <select
            value={selectedWorkMode}
            onChange={(e) => setSelectedWorkMode(e.target.value)}
            className="bg-slate-50 border border-slate-200 text-xs font-medium text-slate-700 rounded-xl px-2.5 py-1.5 focus:outline-none"
          >
            <option value="All">All Modes</option>
            <option value="Remote">Remote</option>
            <option value="Hybrid">Hybrid</option>
            <option value="On-site">On-site</option>
          </select>

          {/* Employment Type */}
          <select
            value={selectedEmpType}
            onChange={(e) => setSelectedEmpType(e.target.value)}
            className="bg-slate-50 border border-slate-200 text-xs font-medium text-slate-700 rounded-xl px-2.5 py-1.5 focus:outline-none"
          >
            <option value="All">All Types</option>
            <option value="Full-time">Full-time</option>
            <option value="Internship">Internship</option>
          </select>

          {/* Fresher Checkbox */}
          <label className="flex items-center space-x-1.5 text-xs text-slate-600 cursor-pointer ml-1">
            <input
              type="checkbox"
              checked={fresherOnly}
              onChange={(e) => setFresherOnly(e.target.checked)}
              className="rounded text-brand-600 focus:ring-brand-500"
            />
            <span>Fresher-friendly</span>
          </label>

          {hasActiveFilters && (
            <button
              type="button"
              onClick={handleClearFilters}
              className="text-xs text-rose-600 hover:underline font-medium ml-2"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Mobile Filter Sheet */}
      {mobileFilterOpen && (
        <div className="md:hidden p-4 bg-white rounded-2xl border border-slate-200 space-y-3 animate-fade-in">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Domain</label>
            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="w-full text-xs p-2 border border-slate-200 rounded-xl bg-slate-50"
            >
              {domains.map((d) => (
                <option key={d} value={d}>{d}</option>
              ))}
            </select>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Work Mode</label>
              <select
                value={selectedWorkMode}
                onChange={(e) => setSelectedWorkMode(e.target.value)}
                className="w-full text-xs p-2 border border-slate-200 rounded-xl bg-slate-50"
              >
                <option value="All">All Modes</option>
                <option value="Remote">Remote</option>
                <option value="Hybrid">Hybrid</option>
                <option value="On-site">On-site</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Type</label>
              <select
                value={selectedEmpType}
                onChange={(e) => setSelectedEmpType(e.target.value)}
                className="w-full text-xs p-2 border border-slate-200 rounded-xl bg-slate-50"
              >
                <option value="All">All Types</option>
                <option value="Full-time">Full-time</option>
                <option value="Internship">Internship</option>
              </select>
            </div>
          </div>
          <div className="flex items-center justify-between pt-2">
            <label className="flex items-center space-x-1.5 text-xs text-slate-700">
              <input
                type="checkbox"
                checked={fresherOnly}
                onChange={(e) => setFresherOnly(e.target.checked)}
                className="rounded text-brand-600"
              />
              <span>Freshers welcome only</span>
            </label>
            <button
              onClick={() => setMobileFilterOpen(false)}
              className="px-3 py-1 bg-brand-600 text-white text-xs font-semibold rounded-lg"
            >
              Apply
            </button>
          </div>
        </div>
      )}

      {/* Job Cards Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <JobCardSkeleton />
          <JobCardSkeleton />
          <JobCardSkeleton />
        </div>
      ) : jobs.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {jobs.map((job) => (
            <JobCard
              key={job.id}
              job={job}
              onToggleSave={(jobId, newState) => {
                setJobs((prev) =>
                  prev.map((j) => (j.id === jobId ? { ...j, is_saved: newState } : j))
                )
              }}
            />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-3xl border border-slate-200/80 p-12 text-center max-w-lg mx-auto">
          <Briefcase className="w-12 h-12 text-slate-300 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-800">No opportunities match these filters</h3>
          <p className="text-xs text-slate-500 mt-1">
            Try adjusting your search query, clearing domain constraints, or toggling work modes.
          </p>
          <button
            type="button"
            onClick={handleClearFilters}
            className="mt-4 px-4 py-2 text-xs font-semibold text-brand-600 bg-brand-50 hover:bg-brand-100 rounded-xl transition"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  )
}
