import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { Job } from '@/types'
import { JobCard } from '@/components/JobCard'
import { JobCardSkeleton } from '@/components/SkeletonLoader'
import { Bookmark, Search, Compass, Sparkles, Filter, Briefcase } from 'lucide-react'

export const SavedJobsPage: React.FC = () => {
  const [jobs, setJobs] = useState<Job[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedDomain, setSelectedDomain] = useState<string>('All')

  const fetchSaved = async () => {
    setIsLoading(true)
    try {
      const data = await api.get<Job[]>('/saved')
      setJobs(data)
    } catch (err) {
      console.error('Failed to load saved jobs:', err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchSaved()
  }, [])

  const handleSaveToggle = (jobId: string, isSaved: boolean) => {
    if (!isSaved) {
      setJobs((prev) => prev.filter((j) => j.id !== jobId))
    }
  }

  // Filter saved jobs locally
  const filteredJobs = jobs.filter((job) => {
    const matchesSearch =
      searchQuery.trim() === '' ||
      job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
      job.location.toLowerCase().includes(searchQuery.toLowerCase())

    const matchesDomain =
      selectedDomain === 'All' || job.domain === selectedDomain

    return matchesSearch && matchesDomain
  })

  const domains = ['All', ...Array.from(new Set(jobs.map((j) => j.domain).filter(Boolean)))]
  const highMatchCount = jobs.filter((j) => (j.match_score || 0) >= 75).length
  const avgMatch = jobs.length
    ? Math.round(jobs.reduce((acc, j) => acc + (j.match_score || 0), 0) / jobs.length)
    : 0

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-lg bg-brand-50 text-brand-600">
              <Bookmark className="w-5 h-5 fill-brand-600" />
            </span>
            <h1 className="text-2xl font-bold text-slate-900">Saved Opportunities</h1>
          </div>
          <p className="mt-1 text-sm text-slate-500">
            Keep track of roles you are interested in. Compare match breakdowns and apply directly on the verified source platform.
          </p>
        </div>

        <Link
          to="/jobs"
          className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-sm font-semibold text-slate-700 shadow-sm transition-colors"
        >
          <Compass className="w-4 h-4 text-brand-600" />
          Explore More Roles
        </Link>
      </div>

      {/* Summary KPI Badges */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center font-bold text-lg">
            {jobs.length}
          </div>
          <div>
            <div className="text-xs font-medium text-slate-500">Total Bookmarked</div>
            <div className="text-sm font-semibold text-slate-900">Active Roles</div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold text-lg">
            {highMatchCount}
          </div>
          <div>
            <div className="text-xs font-medium text-slate-500">Strong Fits (&ge;75%)</div>
            <div className="text-sm font-semibold text-emerald-700">Prime Targets</div>
          </div>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-violet-50 text-violet-600 flex items-center justify-center font-bold text-lg">
            {avgMatch}%
          </div>
          <div>
            <div className="text-xs font-medium text-slate-500">Average Compatibility</div>
            <div className="text-sm font-semibold text-violet-700">Calculated by AI Engine</div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search saved roles by title, company, or location..."
            className="w-full pl-10 pr-4 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
          />
        </div>

        {domains.length > 2 && (
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <select
              value={selectedDomain}
              onChange={(e) => setSelectedDomain(e.target.value)}
              className="py-2 pl-3 pr-8 text-sm bg-white border border-slate-200 rounded-lg text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
            >
              {domains.map((dom) => (
                <option key={dom} value={dom}>
                  {dom === 'All' ? 'All Domains' : dom}
                </option>
              ))}
            </select>
          </div>
        )}
      </div>

      {/* Content Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((n) => (
            <JobCardSkeleton key={n} />
          ))}
        </div>
      ) : filteredJobs.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredJobs.map((job) => (
            <JobCard key={job.id} job={job} onToggleSave={handleSaveToggle} />
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-lg mx-auto space-y-4">
          <div className="w-14 h-14 bg-slate-100 rounded-full flex items-center justify-center mx-auto text-slate-400">
            <Bookmark className="w-7 h-7" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-semibold text-slate-800">
              {searchQuery || selectedDomain !== 'All' ? 'No matching saved roles' : 'No saved opportunities yet'}
            </h3>
            <p className="text-sm text-slate-500">
              {searchQuery || selectedDomain !== 'All'
                ? 'Try adjusting your search query or domain filter.'
                : 'Browse through intelligent career recommendations and bookmark roles with high compatibility.'}
            </p>
          </div>
          <div>
            <Link
              to="/jobs"
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold shadow-sm transition-colors"
            >
              <Compass className="w-4 h-4" />
              Explore Job Explorer
            </Link>
          </div>
        </div>
      )}
    </div>
  )
}
