import React, { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { FullProfile } from '@/types'
import {
  User,
  MapPin,
  Briefcase,
  GraduationCap,
  Sparkles,
  Save,
  Plus,
  X,
  CheckCircle2,
  AlertCircle
} from 'lucide-react'

export const ProfilePage: React.FC = () => {
  const [profile, setProfile] = useState<FullProfile | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [successMsg, setSuccessMsg] = useState<string | null>(null)
  const [newSkill, setNewSkill] = useState('')
  const [newRole, setNewRole] = useState('')

  const fetchProfile = async () => {
    setIsLoading(true)
    try {
      const res = await api.get<FullProfile>('/users/profile')
      setProfile(res)
    } catch {
      // Ignore
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchProfile()
  }, [])

  const handleSaveBasic = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!profile) return
    setIsSaving(true)
    setSuccessMsg(null)
    try {
      await api.put('/users/profile', {
        first_name: profile.first_name,
        last_name: profile.last_name,
        headline: profile.headline,
        current_location: profile.current_location,
        phone: profile.phone
      })

      // Update preferences
      if (profile.career_preferences) {
        await api.put('/users/preferences', profile.career_preferences)
      }

      setSuccessMsg('Profile updated successfully!')
      setTimeout(() => setSuccessMsg(null), 3000)
    } catch {
      // Ignore
    } finally {
      setIsSaving(false)
    }
  }

  const handleAddSkill = (e: React.KeyboardEvent | React.MouseEvent) => {
    if ('key' in e && e.key !== 'Enter') return
    e.preventDefault()
    if (!profile || !newSkill.trim()) return

    const currentSkills = profile.candidate_profile?.skills || []
    if (!currentSkills.includes(newSkill.trim())) {
      const updatedSkills = [...currentSkills, newSkill.trim()]
      setProfile({
        ...profile,
        candidate_profile: {
          ...profile.candidate_profile!,
          skills: updatedSkills
        }
      })
      setNewSkill('')
    }
  }

  const handleRemoveSkill = (skill: string) => {
    if (!profile || !profile.candidate_profile) return
    setProfile({
      ...profile,
      candidate_profile: {
        ...profile.candidate_profile,
        skills: profile.candidate_profile.skills.filter((s) => s !== skill)
      }
    })
  }

  const handleAddRole = (e: React.KeyboardEvent | React.MouseEvent) => {
    if ('key' in e && e.key !== 'Enter') return
    e.preventDefault()
    if (!profile || !newRole.trim()) return

    const currentRoles = profile.career_preferences?.preferred_roles || []
    if (!currentRoles.includes(newRole.trim())) {
      const updatedRoles = [...currentRoles, newRole.trim()]
      setProfile({
        ...profile,
        career_preferences: {
          ...profile.career_preferences!,
          preferred_roles: updatedRoles
        }
      })
      setNewRole('')
    }
  }

  const handleRemoveRole = (role: string) => {
    if (!profile || !profile.career_preferences) return
    setProfile({
      ...profile,
      career_preferences: {
        ...profile.career_preferences,
        preferred_roles: profile.career_preferences.preferred_roles.filter((r) => r !== role)
      }
    })
  }

  if (isLoading || !profile) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center animate-pulse">
        <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <span className="text-xs text-slate-500">Loading career profile...</span>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 animate-fade-in">
      {/* Top Profile Card */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-card flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6">
        <div className="flex items-center space-x-4">
          <div className="w-16 h-16 rounded-2xl bg-indigo-600 text-white font-extrabold text-2xl flex items-center justify-center shadow-subtle">
            {profile.first_name.charAt(0)}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
              {profile.first_name} {profile.last_name}
            </h1>
            <p className="text-sm font-medium text-slate-600">{profile.headline || 'Aspiring Professional'}</p>
            <p className="text-xs text-slate-400 mt-0.5">{profile.email}</p>
          </div>
        </div>

        {/* Completeness Meter */}
        <div className="w-full sm:w-64 bg-slate-50 p-4 rounded-2xl border border-slate-100">
          <div className="flex justify-between text-xs font-semibold mb-1.5">
            <span className="text-slate-600">Profile Completeness</span>
            <span className="text-brand-600">{profile.completeness_percentage}%</span>
          </div>
          <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
            <div
              className="bg-brand-600 h-full rounded-full transition-all duration-500"
              style={{ width: `${profile.completeness_percentage}%` }}
            />
          </div>
          <span className="text-[11px] text-slate-400 mt-1.5 block">
            Complete your profile to improve job recommendations.
          </span>
        </div>
      </div>

      {successMsg && (
        <div className="p-3 bg-emerald-50 text-emerald-800 rounded-xl text-xs flex items-center gap-2 border border-emerald-200">
          <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {/* Main Settings Form */}
      <form onSubmit={handleSaveBasic} className="space-y-6">
        {/* Personal Details */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-subtle space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <User className="w-4 h-4 text-brand-600" />
            <span>Personal Information</span>
          </h2>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">First Name</label>
              <input
                type="text"
                value={profile.first_name}
                onChange={(e) => setProfile({ ...profile, first_name: e.target.value })}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Last Name</label>
              <input
                type="text"
                value={profile.last_name}
                onChange={(e) => setProfile({ ...profile, last_name: e.target.value })}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Professional Headline</label>
              <input
                type="text"
                value={profile.headline || ''}
                onChange={(e) => setProfile({ ...profile, headline: e.target.value })}
                placeholder="e.g. AI & Machine Learning Graduate"
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Current Location</label>
              <input
                type="text"
                value={profile.current_location || ''}
                onChange={(e) => setProfile({ ...profile, current_location: e.target.value })}
                placeholder="e.g. San Francisco, CA"
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200"
              />
            </div>
          </div>
        </div>

        {/* Skills Management */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-subtle space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-brand-600" />
            <span>Technical Skills & Tools</span>
          </h2>
          <p className="text-xs text-slate-500">
            These skills power your compatibility scoring across available opportunities.
          </p>

          <div className="flex gap-2">
            <input
              type="text"
              value={newSkill}
              onChange={(e) => setNewSkill(e.target.value)}
              onKeyDown={handleAddSkill}
              placeholder="Add skill (e.g. Docker, PyTorch) and press Enter"
              className="flex-1 text-xs p-2.5 rounded-xl border border-slate-200"
            />
            <button
              type="button"
              onClick={handleAddSkill}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-xs font-semibold rounded-xl text-slate-700"
            >
              Add
            </button>
          </div>

          <div className="flex flex-wrap gap-2 pt-2">
            {(profile.candidate_profile?.skills || []).map((skill) => (
              <span
                key={skill}
                className="inline-flex items-center px-3 py-1.5 rounded-xl bg-slate-100 text-slate-800 text-xs font-medium border border-slate-200/80"
              >
                <span>{skill}</span>
                <button
                  type="button"
                  onClick={() => handleRemoveSkill(skill)}
                  className="ml-2 text-slate-400 hover:text-rose-600"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Preferred Roles & Career Targets */}
        <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-subtle space-y-4">
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Briefcase className="w-4 h-4 text-brand-600" />
            <span>Target Roles</span>
          </h2>

          <div className="flex gap-2">
            <input
              type="text"
              value={newRole}
              onChange={(e) => setNewRole(e.target.value)}
              onKeyDown={handleAddRole}
              placeholder="Add target role title (e.g. ML Intern) and press Enter"
              className="flex-1 text-xs p-2.5 rounded-xl border border-slate-200"
            />
            <button
              type="button"
              onClick={handleAddRole}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-xs font-semibold rounded-xl text-slate-700"
            >
              Add
            </button>
          </div>

          <div className="flex flex-wrap gap-2 pt-2">
            {(profile.career_preferences?.preferred_roles || []).map((role) => (
              <span
                key={role}
                className="inline-flex items-center px-3 py-1.5 rounded-xl bg-brand-50 text-brand-700 text-xs font-semibold border border-brand-200/80"
              >
                <span>{role}</span>
                <button
                  type="button"
                  onClick={() => handleRemoveRole(role)}
                  className="ml-2 text-brand-400 hover:text-brand-600"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </span>
            ))}
          </div>
        </div>

        {/* Education Showcase */}
        {profile.candidate_profile?.education && profile.candidate_profile.education.length > 0 && (
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-subtle space-y-4">
            <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <GraduationCap className="w-4 h-4 text-brand-600" />
              <span>Education</span>
            </h2>
            <div className="space-y-3">
              {profile.candidate_profile.education.map((edu, idx) => (
                <div key={idx} className="p-3.5 rounded-xl bg-slate-50 border border-slate-100 text-xs">
                  <span className="font-bold text-slate-800 block text-sm">{edu.degree}</span>
                  <span className="text-slate-600">{edu.specialization} • {edu.college}</span>
                  {edu.graduation_year && (
                    <span className="text-slate-400 block mt-0.5">Class of {edu.graduation_year}</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Save CTA */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSaving}
            className="inline-flex items-center px-6 py-2.5 text-xs font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-subtle transition disabled:opacity-50"
          >
            <Save className="w-4 h-4 mr-1.5" />
            <span>{isSaving ? 'Saving...' : 'Save Profile Changes'}</span>
          </button>
        </div>
      </form>
    </div>
  )
}
