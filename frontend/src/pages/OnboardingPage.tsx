import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '@/lib/api'
import { useAuth } from '@/contexts/AuthContext'
import {
  GraduationCap,
  Briefcase,
  MapPin,
  Sparkles,
  ArrowRight,
  ArrowLeft,
  Check,
  Plus,
  X
} from 'lucide-react'

export const OnboardingPage: React.FC = () => {
  const [step, setStep] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()
  const { user } = useAuth()

  // Form State
  // Step 1: Education
  const [degree, setDegree] = useState('B.Tech')
  const [specialization, setSpecialization] = useState('Artificial Intelligence & Data Science')
  const [college, setCollege] = useState('')
  const [graduationYear, setGraduationYear] = useState('2026')
  const [currentStatus, setCurrentStatus] = useState('Student / Final Year')

  // Step 2: Interests
  const [desiredRoles, setDesiredRoles] = useState<string[]>([
    'Machine Learning Engineer',
    'AI Engineer'
  ])
  const [roleInput, setRoleInput] = useState('')
  const [selectedDomains, setSelectedDomains] = useState<string[]>([
    'Machine Learning',
    'Artificial Intelligence'
  ])
  const [experienceLevel, setExperienceLevel] = useState('fresher')

  // Step 3: Preferences
  const [preferredLocations, setPreferredLocations] = useState<string[]>([
    'San Francisco, CA',
    'Remote'
  ])
  const [locationInput, setLocationInput] = useState('')
  const [workModes, setWorkModes] = useState<string[]>(['Remote', 'Hybrid'])
  const [employmentType, setEmploymentType] = useState('Full-time')
  const [salaryPreference, setSalaryPreference] = useState<number>(85000)

  // Step 4: Skills
  const [technicalSkills, setTechnicalSkills] = useState<string[]>([
    'Python',
    'SQL',
    'scikit-learn',
    'Pandas',
    'NumPy'
  ])
  const [skillInput, setSkillInput] = useState('')

  const availableDomains = [
    'Artificial Intelligence',
    'Machine Learning',
    'Data Science',
    'Data Analytics',
    'Software Development',
    'Full Stack Development',
    'Frontend Development',
    'Backend Development',
    'Mobile Development',
    'Cloud Computing',
    'DevOps',
    'Cybersecurity'
  ]

  const handleToggleDomain = (domain: string) => {
    setSelectedDomains((prev) =>
      prev.includes(domain) ? prev.filter((d) => d !== domain) : [...prev, domain]
    )
  }

  const handleToggleWorkMode = (mode: string) => {
    setWorkModes((prev) =>
      prev.includes(mode) ? prev.filter((m) => m !== mode) : [...prev, mode]
    )
  }

  const handleAddRole = (e: React.KeyboardEvent | React.MouseEvent) => {
    if ('key' in e && e.key !== 'Enter') return
    e.preventDefault()
    if (roleInput.trim() && !desiredRoles.includes(roleInput.trim())) {
      setDesiredRoles([...desiredRoles, roleInput.trim()])
      setRoleInput('')
    }
  }

  const handleRemoveRole = (role: string) => {
    setDesiredRoles(desiredRoles.filter((r) => r !== role))
  }

  const handleAddLocation = (e: React.KeyboardEvent | React.MouseEvent) => {
    if ('key' in e && e.key !== 'Enter') return
    e.preventDefault()
    if (locationInput.trim() && !preferredLocations.includes(locationInput.trim())) {
      setPreferredLocations([...preferredLocations, locationInput.trim()])
      setLocationInput('')
    }
  }

  const handleRemoveLocation = (loc: string) => {
    setPreferredLocations(preferredLocations.filter((l) => l !== loc))
  }

  const handleAddSkill = (e: React.KeyboardEvent | React.MouseEvent) => {
    if ('key' in e && e.key !== 'Enter') return
    e.preventDefault()
    if (skillInput.trim() && !technicalSkills.includes(skillInput.trim())) {
      setTechnicalSkills([...technicalSkills, skillInput.trim()])
      setSkillInput('')
    }
  }

  const handleRemoveSkill = (skill: string) => {
    setTechnicalSkills(technicalSkills.filter((s) => s !== skill))
  }

  const handleNext = () => {
    if (step < 4) {
      setStep(step + 1)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } else {
      handleSubmit()
    }
  }

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1)
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }

  const handleSkip = () => {
    navigate('/dashboard')
  }

  const handleSubmit = async () => {
    setIsLoading(true)
    try {
      await api.post('/users/onboarding', {
        education: {
          degree,
          specialization,
          college,
          graduation_year: parseInt(graduationYear) || 2026,
          current_status: currentStatus
        },
        interests: {
          desired_roles: desiredRoles,
          domains: selectedDomains,
          experience_level: experienceLevel,
          job_type: employmentType
        },
        preferences: {
          location: preferredLocations[0] || 'Remote',
          work_mode: workModes,
          preferred_cities: preferredLocations,
          salary_preference: salaryPreference,
          employment_preference: employmentType
        },
        skills: {
          technical_skills: technicalSkills,
          tools: ['Git'],
          frameworks: [],
          soft_skills: ['Problem Solving', 'Communication']
        }
      })
      navigate('/dashboard')
    } catch {
      navigate('/dashboard')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-[85vh] py-10 px-4 sm:px-6 max-w-3xl mx-auto">
      {/* Top Header & Step Progress Indicator */}
      <div className="mb-8">
        <div className="flex items-center justify-between text-xs font-semibold text-slate-500 mb-2">
          <span>Step {step} of 4</span>
          <button
            type="button"
            onClick={handleSkip}
            className="text-brand-600 hover:text-brand-700 font-medium"
          >
            Skip for now
          </button>
        </div>
        {/* Progress Bar */}
        <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
          <div
            className="bg-brand-600 h-full rounded-full transition-all duration-300"
            style={{ width: `${(step / 4) * 100}%` }}
          />
        </div>
      </div>

      <div className="bg-white rounded-3xl shadow-card border border-slate-200/80 p-6 sm:p-8">
        {/* Step 1: Education */}
        {step === 1 && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex items-center space-x-3 pb-4 border-b border-slate-100">
              <div className="w-10 h-10 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
                <GraduationCap className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-slate-800">Your Academic Foundation</h2>
                <p className="text-xs text-slate-500">
                  Help ZyncRole identify fresher-friendly roles aligned with your studies
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">Degree</label>
                <input
                  type="text"
                  value={degree}
                  onChange={(e) => setDegree(e.target.value)}
                  placeholder="e.g. B.Tech / B.S."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">Specialization / Major</label>
                <input
                  type="text"
                  value={specialization}
                  onChange={(e) => setSpecialization(e.target.value)}
                  placeholder="e.g. AI & Data Science, CS"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">University / College</label>
                <input
                  type="text"
                  value={college}
                  onChange={(e) => setCollege(e.target.value)}
                  placeholder="e.g. State University"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1.5">Graduation Year</label>
                <input
                  type="number"
                  value={graduationYear}
                  onChange={(e) => setGraduationYear(e.target.value)}
                  placeholder="2026"
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">Current Status</label>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                {['Student / Final Year', 'Recent Graduate / Fresher', 'Early Professional'].map((status) => (
                  <button
                    key={status}
                    type="button"
                    onClick={() => setCurrentStatus(status)}
                    className={`py-2 px-3 text-xs font-medium rounded-xl border transition ${
                      currentStatus === status
                        ? 'bg-brand-50 border-brand-300 text-brand-700 font-semibold'
                        : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    {status}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Step 2: Career Interests & Domains */}
        {step === 2 && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex items-center space-x-3 pb-4 border-b border-slate-100">
              <div className="w-10 h-10 rounded-2xl bg-brand-50 text-brand-600 flex items-center justify-center">
                <Briefcase className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-slate-800">Target Domains & Roles</h2>
                <p className="text-xs text-slate-500">
                  Select fields where you want your opportunities focused
                </p>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-2">
                Career Domains (select all that apply)
              </label>
              <div className="flex flex-wrap gap-2">
                {availableDomains.map((dom) => {
                  const selected = selectedDomains.includes(dom)
                  return (
                    <button
                      key={dom}
                      type="button"
                      onClick={() => handleToggleDomain(dom)}
                      className={`px-3 py-1.5 text-xs font-medium rounded-xl border transition flex items-center gap-1.5 ${
                        selected
                          ? 'bg-brand-600 text-white border-brand-600 shadow-xs'
                          : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
                      }`}
                    >
                      {selected && <Check className="w-3.5 h-3.5" />}
                      <span>{dom}</span>
                    </button>
                  )
                })}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Target Roles / Titles
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={roleInput}
                  onChange={(e) => setRoleInput(e.target.value)}
                  onKeyDown={handleAddRole}
                  placeholder="e.g. ML Engineer, AI Research Intern (press Enter)"
                  className="flex-1 px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600"
                />
                <button
                  type="button"
                  onClick={handleAddRole}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl"
                >
                  Add
                </button>
              </div>

              <div className="flex flex-wrap gap-1.5 mt-2.5">
                {desiredRoles.map((role) => (
                  <span
                    key={role}
                    className="inline-flex items-center px-3 py-1 rounded-lg bg-brand-50 text-brand-700 border border-brand-200 text-xs font-medium"
                  >
                    <span>{role}</span>
                    <button
                      type="button"
                      onClick={() => handleRemoveRole(role)}
                      className="ml-1.5 text-brand-400 hover:text-brand-600"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Step 3: Work Preferences */}
        {step === 3 && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex items-center space-x-3 pb-4 border-b border-slate-100">
              <div className="w-10 h-10 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
                <MapPin className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-slate-800">Work Preferences</h2>
                <p className="text-xs text-slate-500">
                  Where and how do you prefer to work?
                </p>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-2">Work Mode</label>
              <div className="grid grid-cols-3 gap-3">
                {['Remote', 'Hybrid', 'On-site'].map((mode) => {
                  const selected = workModes.includes(mode)
                  return (
                    <button
                      key={mode}
                      type="button"
                      onClick={() => handleToggleWorkMode(mode)}
                      className={`p-3 text-center rounded-xl border text-xs font-semibold transition ${
                        selected
                          ? 'bg-emerald-50 border-emerald-300 text-emerald-800'
                          : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                      }`}
                    >
                      {mode}
                    </button>
                  )
                })}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Preferred Cities / Regions
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={locationInput}
                  onChange={(e) => setLocationInput(e.target.value)}
                  onKeyDown={handleAddLocation}
                  placeholder="e.g. San Francisco, CA, New York, NY (press Enter)"
                  className="flex-1 px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600"
                />
                <button
                  type="button"
                  onClick={handleAddLocation}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl"
                >
                  Add
                </button>
              </div>

              <div className="flex flex-wrap gap-1.5 mt-2.5">
                {preferredLocations.map((loc) => (
                  <span
                    key={loc}
                    className="inline-flex items-center px-3 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 text-xs font-medium"
                  >
                    <span>{loc}</span>
                    <button
                      type="button"
                      onClick={() => handleRemoveLocation(loc)}
                      className="ml-1.5 text-emerald-500 hover:text-emerald-700"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Employment Preference
              </label>
              <div className="grid grid-cols-2 gap-3">
                {['Full-time', 'Internship'].map((t) => (
                  <button
                    key={t}
                    type="button"
                    onClick={() => setEmploymentType(t)}
                    className={`py-2.5 px-3 text-xs font-medium rounded-xl border transition ${
                      employmentType === t
                        ? 'bg-brand-50 border-brand-300 text-brand-700 font-semibold'
                        : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                    }`}
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Step 4: Technical Skills */}
        {step === 4 && (
          <div className="space-y-6 animate-fade-in">
            <div className="flex items-center space-x-3 pb-4 border-b border-slate-100">
              <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center">
                <Sparkles className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-slate-800">Your Technical Skills</h2>
                <p className="text-xs text-slate-500">
                  Languages, frameworks, and tools powering your match scores
                </p>
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1.5">
                Add Core Technical Skills
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyDown={handleAddSkill}
                  placeholder="e.g. Python, SQL, Docker, React (press Enter)"
                  className="flex-1 px-3.5 py-2 rounded-xl border border-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-600"
                />
                <button
                  type="button"
                  onClick={handleAddSkill}
                  className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-xl"
                >
                  Add
                </button>
              </div>

              <div className="flex flex-wrap gap-1.5 mt-3">
                {technicalSkills.map((skill) => (
                  <span
                    key={skill}
                    className="inline-flex items-center px-3 py-1 rounded-lg bg-slate-100 text-slate-800 border border-slate-200 text-xs font-medium"
                  >
                    <span>{skill}</span>
                    <button
                      type="button"
                      onClick={() => handleRemoveSkill(skill)}
                      className="ml-1.5 text-slate-400 hover:text-slate-600"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            </div>

            {/* Quick suggested chips */}
            <div>
              <span className="text-[11px] text-slate-400 font-medium block mb-2">
                Quick add popular skills:
              </span>
              <div className="flex flex-wrap gap-1.5">
                {['Python', 'SQL', 'scikit-learn', 'TensorFlow', 'Pandas', 'NumPy', 'Git', 'FastAPI', 'Docker', 'React'].map((s) => (
                  <button
                    key={s}
                    type="button"
                    onClick={() => {
                      if (!technicalSkills.includes(s)) {
                        setTechnicalSkills([...technicalSkills, s])
                      }
                    }}
                    disabled={technicalSkills.includes(s)}
                    className="px-2.5 py-1 text-xs rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-600 disabled:opacity-40"
                  >
                    + {s}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Wizard Navigation Footer */}
        <div className="mt-8 pt-5 border-t border-slate-100 flex items-center justify-between">
          {step > 1 ? (
            <button
              type="button"
              onClick={handleBack}
              className="inline-flex items-center px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl transition"
            >
              <ArrowLeft className="w-4 h-4 mr-1.5" />
              <span>Back</span>
            </button>
          ) : (
            <div />
          )}

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handleSkip}
              className="text-xs text-slate-400 hover:text-slate-600 transition"
            >
              Skip for now
            </button>
            <button
              type="button"
              onClick={handleNext}
              disabled={isLoading}
              className="inline-flex items-center px-5 py-2.5 rounded-xl text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 shadow-subtle transition"
            >
              <span>{step === 4 ? (isLoading ? 'Finalizing Profile...' : 'Complete & View Feed') : 'Next Step'}</span>
              <ArrowRight className="w-4 h-4 ml-1.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
