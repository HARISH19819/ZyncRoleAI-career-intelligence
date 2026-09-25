import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { Sparkles, ArrowLeft, CheckCircle2 } from 'lucide-react'

export const ForgotPasswordPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    try {
      await api.post('/auth/forgot-password', { email })
      setSubmitted(true)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-card border border-slate-200/80 p-6 sm:p-8">
        <div className="text-center mb-6">
          <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center mx-auto mb-3">
            <Sparkles className="w-5 h-5" />
          </div>
          <h1 className="text-xl font-bold text-slate-800">Reset your password</h1>
          <p className="text-xs text-slate-500 mt-1">
            Enter your email and we'll help you regain access to your career feed.
          </p>
        </div>

        {submitted ? (
          <div className="text-center space-y-4">
            <div className="p-3 bg-emerald-50 text-emerald-800 rounded-xl text-xs flex items-center gap-2 border border-emerald-200">
              <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600" />
              <span>If an account exists, reset instructions have been dispatched.</span>
            </div>
            <Link
              to="/login"
              className="inline-flex items-center text-xs font-semibold text-brand-600 hover:underline"
            >
              <ArrowLeft className="w-3.5 h-3.5 mr-1" />
              Back to login
            </Link>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5" htmlFor="email">
                Account Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600 transition"
              />
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className="w-full px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 transition"
            >
              {isLoading ? 'Sending...' : 'Send Reset Link'}
            </button>
            <div className="text-center pt-2">
              <Link to="/login" className="text-xs text-slate-500 hover:text-slate-700">
                Cancel and return to login
              </Link>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}
