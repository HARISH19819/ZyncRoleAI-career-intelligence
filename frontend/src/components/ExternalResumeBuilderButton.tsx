import React, { useState } from 'react'
import { ExternalLink, Sparkles, X } from 'lucide-react'

interface Props {
  url?: string
  label?: string
  description?: string
  variant?: 'primary' | 'secondary' | 'outline'
  className?: string
}

export const ExternalResumeBuilderButton: React.FC<Props> = ({
  url,
  label = 'Create ATS-Friendly Resume',
  description,
  variant = 'secondary',
  className = ''
}) => {
  const [showNotice, setShowNotice] = useState(false)
  const targetUrl = url || import.meta.env.VITE_ATS_RESUME_BUILDER_URL || 'https://www.open-resume.com'

  const handleOpen = () => {
    setShowNotice(true)
  }

  const handleProceed = () => {
    window.open(targetUrl, '_blank', 'noopener,noreferrer')
    setShowNotice(false)
  }

  const baseStyle =
    'inline-flex items-center justify-center font-medium transition-all duration-200 rounded-lg text-sm px-4 py-2.5 focus:outline-none focus:ring-2 focus:ring-offset-2'

  const variants = {
    primary: 'bg-brand-600 hover:bg-brand-700 text-white shadow-subtle focus:ring-brand-500',
    secondary: 'bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 shadow-subtle focus:ring-slate-400',
    outline: 'border border-brand-200 hover:bg-brand-50 text-brand-700 focus:ring-brand-500'
  }

  return (
    <>
      <button
        type="button"
        onClick={handleOpen}
        className={`${baseStyle} ${variants[variant]} ${className}`}
        title={description || label}
      >
        <Sparkles className="w-4 h-4 mr-2 text-brand-600" />
        <span>{label}</span>
        <ExternalLink className="w-3.5 h-3.5 ml-2 opacity-60" />
      </button>

      {/* Calm Confirmation Dialog */}
      {showNotice && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/30 backdrop-blur-xs animate-fade-in">
          <div className="w-full max-w-md p-6 bg-white rounded-2xl shadow-float border border-slate-100">
            <div className="flex items-start justify-between">
              <div className="flex items-center space-x-2">
                <div className="p-2 rounded-xl bg-brand-50 text-brand-600">
                  <Sparkles className="w-5 h-5" />
                </div>
                <h3 className="text-lg font-semibold text-slate-800">Free ATS Resume Builder</h3>
              </div>
              <button
                onClick={() => setShowNotice(false)}
                className="p-1 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="mt-3 text-sm text-slate-600 leading-relaxed">
              Your resume analysis is complete. You will be redirected to a free, privacy-first ATS resume builder (<strong>OpenResume</strong>) where you can build an optimized ATS-formatted template without any cost or subscription.
            </p>

            <div className="flex justify-end gap-3 mt-6">
              <button
                type="button"
                onClick={() => setShowNotice(false)}
                className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg transition"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleProceed}
                className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-brand-600 hover:bg-brand-700 rounded-lg shadow-subtle transition"
              >
                <span>Continue to Builder</span>
                <ExternalLink className="w-4 h-4 ml-1.5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
