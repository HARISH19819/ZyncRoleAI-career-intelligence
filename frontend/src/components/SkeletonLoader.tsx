import React from 'react'

export const JobCardSkeleton: React.FC = () => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-subtle animate-pulse space-y-4">
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-slate-200" />
          <div className="space-y-1.5">
            <div className="w-24 h-3 bg-slate-200 rounded" />
            <div className="w-40 h-4 bg-slate-200 rounded" />
          </div>
        </div>
        <div className="w-8 h-8 rounded-xl bg-slate-100" />
      </div>

      <div className="flex gap-2">
        <div className="w-20 h-4 bg-slate-100 rounded" />
        <div className="w-16 h-4 bg-slate-100 rounded" />
        <div className="w-24 h-4 bg-slate-100 rounded" />
      </div>

      <div className="w-full h-8 bg-slate-100 rounded-xl" />

      <div className="flex gap-1.5">
        <div className="w-16 h-5 bg-slate-100 rounded-md" />
        <div className="w-20 h-5 bg-slate-100 rounded-md" />
        <div className="w-14 h-5 bg-slate-100 rounded-md" />
      </div>

      <div className="pt-3 border-t border-slate-100 flex justify-between items-center">
        <div className="w-20 h-3 bg-slate-100 rounded" />
        <div className="w-24 h-7 bg-slate-200 rounded-lg" />
      </div>
    </div>
  )
}

export const DashboardSkeleton: React.FC = () => {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-pulse space-y-8">
      <div className="space-y-2">
        <div className="w-48 h-7 bg-slate-200 rounded-lg" />
        <div className="w-72 h-4 bg-slate-100 rounded" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="h-32 bg-white rounded-2xl border border-slate-200/80 p-5" />
        <div className="h-32 bg-white rounded-2xl border border-slate-200/80 p-5" />
        <div className="h-32 bg-white rounded-2xl border border-slate-200/80 p-5" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <JobCardSkeleton />
        <JobCardSkeleton />
        <JobCardSkeleton />
      </div>
    </div>
  )
}
