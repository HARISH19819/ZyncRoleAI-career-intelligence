import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'
import { FullProfile, CareerPreferences } from '@/types'
import {
  Settings,
  User as UserIcon,
  Shield,
  Download,
  Trash2,
  Save,
  CheckCircle2,
  AlertTriangle,
  Briefcase,
  Lock,
  ExternalLink
} from 'lucide-react'

export const SettingsPage: React.FC = () => {
  const { user, logout, refreshUser } = useAuth()
  const navigate = useNavigate()

  const [fullProfile, setFullProfile] = useState<FullProfile | null>(null)

  // Profile fields
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [headline, setHeadline] = useState('')
  const [currentLocation, setCurrentLocation] = useState('')
  const [phone, setPhone] = useState('')

  // Preference fields
  const [workModes, setWorkModes] = useState<string[]>([])
  const [salaryMin, setSalaryMin] = useState<number>(0)
  const [salaryCurrency, setSalaryCurrency] = useState('USD')

  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState(false)
  const [deleteModalOpen, setDeleteModalOpen] = useState(false)
  const [deleteConfirmText, setDeleteConfirmText] = useState('')
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    const fetchUserData = async () => {
      setIsLoading(true)
      try {
        const profile = await api.get<FullProfile>('/users/profile')
        setFullProfile(profile)
        setFirstName(profile.first_name || '')
        setLastName(profile.last_name || '')
        setHeadline(profile.headline || '')
        setCurrentLocation(profile.current_location || '')
        setPhone(profile.phone || '')

        if (profile.career_preferences) {
          setWorkModes(profile.career_preferences.work_modes || ['Remote', 'Hybrid'])
          setSalaryMin(profile.career_preferences.salary_min || 0)
          setSalaryCurrency(profile.career_preferences.salary_currency || 'USD')
        }
      } catch (err) {
        console.error('Failed to load profile settings:', err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchUserData()
  }, [])

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSaving(true)
    setSaveSuccess(false)
    try {
      await api.put('/users/profile', {
        first_name: firstName,
        last_name: lastName,
        headline,
        current_location: currentLocation,
        phone
      })

      await api.put('/users/preferences', {
        preferred_roles: fullProfile?.career_preferences?.preferred_roles || [],
        preferred_domains: fullProfile?.career_preferences?.preferred_domains || [],
        preferred_locations: fullProfile?.career_preferences?.preferred_locations || [],
        work_modes: workModes,
        employment_types: fullProfile?.career_preferences?.employment_types || ['Full-time'],
        salary_min: salaryMin,
        salary_currency: salaryCurrency,
        preferred_company_types: fullProfile?.career_preferences?.preferred_company_types || []
      })

      await refreshUser()
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    } catch (err) {
      console.error('Failed to save settings:', err)
    } finally {
      setIsSaving(false)
    }
  }

  const handleExportData = async () => {
    try {
      const data = await api.get('/users/export-data')
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `zyncrole_data_export_${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } catch (err) {
      console.error('Failed to export data:', err)
      alert('Unable to export data at this time.')
    }
  }

  const handleDeleteAccount = async () => {
    if (deleteConfirmText.trim().toLowerCase() !== 'delete my account') {
      alert('Please type "delete my account" to confirm.')
      return
    }

    setIsDeleting(true)
    try {
      await api.delete('/users/account')
      logout()
      navigate('/', { replace: true })
    } catch (err) {
      console.error('Failed to delete account:', err)
      alert('Error deleting account. Please contact support or try again.')
      setIsDeleting(false)
    }
  }

  const toggleWorkMode = (mode: string) => {
    if (workModes.includes(mode)) {
      setWorkModes(workModes.filter((m) => m !== mode))
    } else {
      setWorkModes([...workModes, mode])
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-24">
        <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="border-b border-slate-200 pb-6">
        <div className="flex items-center gap-2">
          <span className="p-2 rounded-lg bg-brand-50 text-brand-600">
            <Settings className="w-5 h-5" />
          </span>
          <h1 className="text-2xl font-bold text-slate-900">Account & Privacy Settings</h1>
        </div>
        <p className="mt-1 text-sm text-slate-500">
          Manage your personal details, career search preferences, and data privacy controls.
        </p>
      </div>

      {saveSuccess && (
        <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center gap-3 text-emerald-800 text-sm animate-in fade-in duration-200">
          <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
          <span>Your settings and preferences have been successfully updated.</span>
        </div>
      )}

      {/* Main Settings Form */}
      <form onSubmit={handleSaveProfile} className="space-y-6">
        {/* Profile Card */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-5">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
            <UserIcon className="w-4 h-4 text-brand-600" />
            <h2 className="text-base font-bold text-slate-900">Personal Information</h2>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">First Name</label>
              <input
                type="text"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
                className="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Last Name</label>
              <input
                type="text"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                className="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
            <input
              type="email"
              value={user?.email || ''}
              disabled
              className="w-full px-3.5 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg text-slate-500 cursor-not-allowed"
            />
            <span className="text-[11px] text-slate-400 mt-1 block">
              Email is associated with your primary authentication identity.
            </span>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Professional Headline</label>
            <input
              type="text"
              value={headline}
              onChange={(e) => setHeadline(e.target.value)}
              placeholder="e.g. Aspiring Full Stack Engineer | Python & React"
              className="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Current Location</label>
              <input
                type="text"
                value={currentLocation}
                onChange={(e) => setCurrentLocation(e.target.value)}
                placeholder="City, State / Country"
                className="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Contact Phone</label>
              <input
                type="text"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="+1 (555) 000-0000"
                className="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
              />
            </div>
          </div>
        </div>

        {/* Career Preferences Quick Config */}
        <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-5">
          <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
            <Briefcase className="w-4 h-4 text-brand-600" />
            <h2 className="text-base font-bold text-slate-900">Career Preferences</h2>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-2">Work Modes</label>
            <div className="flex flex-wrap gap-2">
              {['Remote', 'Hybrid', 'On-site'].map((mode) => (
                <button
                  type="button"
                  key={mode}
                  onClick={() => toggleWorkMode(mode)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
                    workModes.includes(mode)
                      ? 'bg-brand-50 border-brand-500 text-brand-700'
                      : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  {mode}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Minimum Annual Expected Salary
              </label>
              <input
                type="number"
                min="0"
                step="5000"
                value={salaryMin}
                onChange={(e) => setSalaryMin(parseFloat(e.target.value) || 0)}
                className="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Currency</label>
              <select
                value={salaryCurrency}
                onChange={(e) => setSalaryCurrency(e.target.value)}
                className="w-full px-3.5 py-2 text-sm bg-white border border-slate-200 rounded-lg text-slate-700 focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
              >
                <option value="USD">USD ($)</option>
                <option value="INR">INR (₹)</option>
                <option value="EUR">EUR (€)</option>
                <option value="GBP">GBP (£)</option>
              </select>
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSaving}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold shadow-sm transition-colors disabled:opacity-50"
          >
            <Save className="w-4 h-4" />
            {isSaving ? 'Saving...' : 'Save Settings'}
          </button>
        </div>
      </form>

      {/* Data Sovereignty & Privacy Section */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs space-y-6">
        <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
          <Shield className="w-4 h-4 text-emerald-600" />
          <h2 className="text-base font-bold text-slate-900">Data Sovereignty & Privacy</h2>
        </div>

        <div className="space-y-2 text-xs text-slate-600 leading-relaxed">
          <p>
            At <strong>ZyncRole AI</strong>, you own your career data. We do not sell your personal information,
            we do not engage in unauthorized scraping, and your resume is evaluated strictly for your personal job
            matching and ATS recommendations.
          </p>
          <p>
            You can export your complete candidate data at any time or permanently purge your account and resumes.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row gap-3 pt-2">
          <button
            type="button"
            onClick={handleExportData}
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-xs font-semibold text-slate-700 shadow-2xs transition-colors"
          >
            <Download className="w-4 h-4 text-slate-500" />
            Export My Data (JSON)
          </button>

          <button
            type="button"
            onClick={() => setDeleteModalOpen(true)}
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg border border-rose-200 bg-rose-50 hover:bg-rose-100 text-xs font-semibold text-rose-700 transition-colors"
          >
            <Trash2 className="w-4 h-4 text-rose-600" />
            Delete Account & Purge Data
          </button>
        </div>
      </div>

      {/* Account Deletion Confirmation Modal */}
      {deleteModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl border border-slate-200 space-y-4 animate-in fade-in zoom-in-95 duration-150">
            <div className="flex items-center gap-2 text-rose-600 font-bold text-base">
              <AlertTriangle className="w-5 h-5 shrink-0" />
              Delete Account Permanently
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              This action cannot be undone. All your saved jobs, application pipelines, uploaded resumes,
              and candidate profiles will be permanently erased from the platform.
            </p>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Type <span className="font-mono text-rose-600 font-bold">delete my account</span> to confirm:
              </label>
              <input
                type="text"
                value={deleteConfirmText}
                onChange={(e) => setDeleteConfirmText(e.target.value)}
                placeholder="delete my account"
                className="w-full px-3 py-2 text-xs border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500"
              />
            </div>

            <div className="flex justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => {
                  setDeleteModalOpen(false)
                  setDeleteConfirmText('')
                }}
                className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDeleteAccount}
                disabled={isDeleting || deleteConfirmText.trim().toLowerCase() !== 'delete my account'}
                className="px-4 py-2 text-xs font-semibold bg-rose-600 text-white rounded-lg hover:bg-rose-700 shadow-sm transition-colors disabled:opacity-50"
              >
                {isDeleting ? 'Deleting...' : 'Permanently Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
