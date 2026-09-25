import React from 'react'
import { Sparkles, Shield, Heart } from 'lucide-react'
import { Link } from 'react-router-dom'

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200/80 py-8 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <div className="w-6 h-6 rounded-lg bg-brand-600 flex items-center justify-center text-white text-xs">
              <Sparkles className="w-3.5 h-3.5" />
            </div>
            <span className="text-sm font-semibold text-slate-800">
              ZyncRole AI
            </span>
            <span className="text-xs text-slate-400">
              — One Resume. Every Opportunity. One Intelligent Career Feed.
            </span>
          </div>

          <div className="flex items-center space-x-6 text-xs text-slate-500">
            <Link to="/jobs" className="hover:text-slate-800 transition">Explore Jobs</Link>
            <Link to="/career" className="hover:text-slate-800 transition">Market Trends</Link>
            <Link to="/settings" className="hover:text-slate-800 transition">Privacy & Controls</Link>
            <span className="flex items-center text-slate-400">
              <Shield className="w-3.5 h-3.5 mr-1" />
              Privacy First
            </span>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-400 gap-2">
          <p>© {new Date().getFullYear()} ZyncRole AI. Built for next-generation career discovery.</p>
          <p className="text-center sm:text-right">
            All original job sources and application portals are preserved. No unauthorized scraping.
          </p>
        </div>
      </div>
    </footer>
  )
}
