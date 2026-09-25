import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { api } from '@/lib/api'
import { Sparkles, ArrowRight, AlertCircle } from 'lucide-react'

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)

    try {
      const res = await login(email, password)
      if (res.onboarding_completed) {
        navigate('/dashboard')
      } else {
        navigate('/onboarding')
      }
    } catch (err: any) {
      setError(err.message || 'Invalid email or password.')
    } finally {
      setIsLoading(false)
    }
  }

  // Quick Demo Account for Hackathon Jury Evaluation
  const handleQuickDemo = async () => {
    setError(null)
    setIsLoading(true)
    try {
      // First try login demo
      try {
        await login('demo.candidate@zyncrole.ai', 'Password123!')
        navigate('/dashboard')
        return
      } catch {
        // Register demo candidate if doesn't exist yet
        await api.post('/auth/register', {
          first_name: 'Alex',
          last_name: 'Chen',
          email: 'demo.candidate@zyncrole.ai',
          password: 'Password123!'
        })
        await login('demo.candidate@zyncrole.ai', 'Password123!')
        // Populate onboarding
        await api.post('/users/onboarding', {
          education: {
            degree: 'B.Tech',
            specialization: 'Artificial Intelligence & Data Science',
            college: 'Institute of Technology',
            graduation_year: 2026,
            current_status: 'Final-year student'
          },
          interests: {
            desired_roles: ['Machine Learning Engineer', 'AI Engineer', 'Data Scientist'],
            domains: ['Machine Learning', 'Artificial Intelligence', 'Data Science'],
            experience_level: 'fresher',
            job_type: 'Full-time'
          },
          preferences: {
            location: 'San Francisco, CA',
            work_mode: ['Remote', 'Hybrid'],
            salary_preference: 95000,
            employment_preference: 'Full-time'
          },
          skills: {
            technical_skills: ['Python', 'SQL', 'scikit-learn', 'TensorFlow', 'Git'],
            tools: ['Git', 'VS Code'],
            frameworks: ['Pandas', 'NumPy'],
            soft_skills: ['Problem Solving', 'Team Collaboration']
          }
        })
        navigate('/dashboard')
      }
    } catch (err: any) {
      setError(err.message || 'Unable to load demo account.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-[85vh] flex items-center justify-center p-4 sm:p-6">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-card border border-slate-200/80 p-6 sm:p-8">
        <div className="text-center mb-6">
          <div className="w-10 h-10 rounded-xl bg-brand-50 text-brand-600 flex items-center justify-center mx-auto mb-3">
            <Sparkles className="w-5 h-5" />
          </div>
          <h1 className="text-2xl font-bold text-slate-800 tracking-tight">Welcome back</h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Log in to access your personalized career feed
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200/80 text-rose-700 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1.5" htmlFor="email">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600 transition"
            />
          </div>

          <div>
            <div className="flex items-center justify-between mb-1.5">
              <label className="block text-xs font-semibold text-slate-700" htmlFor="password">
                Password
              </label>
              <Link
                to="/forgot-password"
                className="text-xs text-brand-600 hover:text-brand-700 font-medium"
              >
                Forgot password?
              </Link>
            </div>
            <input
              id="password"
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600 transition"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full inline-flex items-center justify-center px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 shadow-subtle transition disabled:opacity-50"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
            <ArrowRight className="w-4 h-4 ml-1.5" />
          </button>
        </form>

        {/* Demo Fast Track Button */}
        <div className="mt-5 pt-5 border-t border-slate-100">
          <button
            type="button"
            onClick={handleQuickDemo}
            disabled={isLoading}
            className="w-full inline-flex items-center justify-center px-4 py-2 text-xs font-medium text-slate-700 bg-slate-50 hover:bg-slate-100 border border-slate-200/80 rounded-xl transition"
          >
            <Sparkles className="w-3.5 h-3.5 text-brand-600 mr-1.5" />
            <span>Launch Instant Demo Profile (Alex Chen • AI Fresher)</span>
          </button>
        </div>

        <div className="mt-6 text-center text-xs text-slate-500">
          Don't have an account?{' '}
          <Link to="/register" className="text-brand-600 hover:underline font-semibold">
            Create account free
          </Link>
        </div>
      </div>
    </div>
  )
}
