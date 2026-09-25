import React from 'react'
import { Link } from 'react-router-dom'
import { Compass, Home, ArrowLeft } from 'lucide-react'

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-[70vh] flex items-center justify-center px-4 py-16">
      <div className="text-center max-w-md mx-auto space-y-6">
        <div className="w-16 h-16 bg-brand-50 text-brand-600 rounded-2xl flex items-center justify-center mx-auto shadow-xs">
          <Compass className="w-8 h-8" />
        </div>

        <div className="space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-600">404 Error</span>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Page Not Found</h1>
          <p className="text-sm text-slate-500 leading-relaxed">
            The page you are looking for doesn&rsquo;t exist, was moved, or the link may be outdated.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
          <Link
            to="/dashboard"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold shadow-sm transition-colors"
          >
            <Home className="w-4 h-4" />
            Go to Dashboard
          </Link>
          <Link
            to="/jobs"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-sm font-semibold shadow-2xs transition-colors"
          >
            <Compass className="w-4 h-4 text-brand-600" />
            Explore Career Feed
          </Link>
        </div>
      </div>
    </div>
  )
}
