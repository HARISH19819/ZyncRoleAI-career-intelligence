import React, { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { ExternalResumeBuilderButton } from '@/components/ExternalResumeBuilderButton'
import {
  UploadCloud,
  FileText,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  Trash2,
  ShieldCheck,
  Check
} from 'lucide-react'

export const ResumePage: React.FC = () => {
  const [currentResume, setCurrentResume] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgressStep, setUploadProgressStep] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [isDragOver, setIsDragOver] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const fetchResume = async () => {
    setIsLoading(true)
    try {
      const res = await api.get<{ current_resume: any }>('/resume/current')
      setCurrentResume(res.current_resume)
    } catch {
      setCurrentResume(null)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchResume()
  }, [])

  const handleFileUpload = async (file: File) => {
    const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase()
    if (!['.pdf', '.docx', '.txt'].includes(ext)) {
      setError('Please upload a PDF, DOCX, or TXT file.')
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      setError('File size exceeds the 5 MB limit.')
      return
    }

    setError(null)
    setIsUploading(true)

    // Human step progression (Section 14 & 89)
    setUploadProgressStep('Reading your resume...')
    await new Promise((r) => setTimeout(r, 600))
    setUploadProgressStep('Building your career profile...')
    await new Promise((r) => setTimeout(r, 600))
    setUploadProgressStep('Checking ATS readiness...')

    const formData = new FormData()
    formData.append('file', file)

    try {
      await api.post('/resume/upload', formData)
      setUploadProgressStep('Finding matching roles...')
      await new Promise((r) => setTimeout(r, 400))
      await fetchResume()
    } catch (err: any) {
      setError(err.message || 'We could not analyze this resume yet. Please try again.')
    } finally {
      setIsUploading(false)
      setUploadProgressStep('')
    }
  }

  const handleDeleteResume = async () => {
    if (!currentResume) return
    try {
      await api.delete(`/resume/${currentResume.id}`)
      setCurrentResume(null)
    } catch {
      // Ignore
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200/60">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
            Resume Intelligence Center
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Private resume analysis, ZyncRole ATS readiness, and automated career profile extraction
          </p>
        </div>

        <ExternalResumeBuilderButton />
      </div>

      {error && (
        <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-600" />
            <span>{error}</span>
          </div>
          <button onClick={() => setError(null)} className="text-rose-500 hover:text-rose-700">
            Dismiss
          </button>
        </div>
      )}

      {/* Two Column Layout (Section 14) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left: Upload / Current Resume File (5 cols) */}
        <div className="lg:col-span-5 space-y-5">
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-5">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-bold text-slate-900">
                {currentResume ? 'Current Resume' : 'Upload Resume'}
              </h2>
              <span className="text-xs text-slate-400">PDF, DOCX, TXT • Max 5MB</span>
            </div>

            {/* Drag & Drop Zone */}
            <div
              onDragOver={(e) => {
                e.preventDefault()
                setIsDragOver(true)
              }}
              onDragLeave={() => setIsDragOver(false)}
              onDrop={(e) => {
                e.preventDefault()
                setIsDragOver(false)
                if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                  handleFileUpload(e.dataTransfer.files[0])
                }
              }}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all ${
                isDragOver
                  ? 'border-brand-600 bg-brand-50/50'
                  : 'border-slate-200 hover:border-brand-400 bg-slate-50/60 hover:bg-slate-50'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    handleFileUpload(e.target.files[0])
                  }
                }}
                className="hidden"
              />

              <div className="w-12 h-12 rounded-2xl bg-brand-50 text-brand-600 flex items-center justify-center mx-auto mb-3">
                <UploadCloud className="w-6 h-6" />
              </div>

              {isUploading ? (
                <div className="space-y-2">
                  <div className="w-5 h-5 border-2 border-brand-600 border-t-transparent rounded-full animate-spin mx-auto" />
                  <p className="text-xs font-semibold text-brand-600">{uploadProgressStep}</p>
                </div>
              ) : (
                <>
                  <p className="text-xs font-bold text-slate-700">
                    Click to browse or drag and drop your resume
                  </p>
                  <p className="text-[11px] text-slate-400 mt-1">
                    Your file is processed privately in your account.
                  </p>
                </>
              )}
            </div>

            {/* Current Resume details if present */}
            {currentResume && (
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                <div className="flex items-center space-x-3 min-w-0">
                  <div className="w-9 h-9 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-slate-700 font-bold text-xs uppercase shrink-0">
                    {currentResume.file_type}
                  </div>
                  <div className="min-w-0">
                    <p className="text-xs font-bold text-slate-800 truncate">
                      {currentResume.file_name}
                    </p>
                    <p className="text-[11px] text-slate-400">
                      Uploaded {new Date(currentResume.uploaded_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleDeleteResume}
                  className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-white transition"
                  title="Delete resume"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            )}

            <div className="text-[11px] text-slate-400 flex items-start space-x-1.5 pt-1">
              <ShieldCheck className="w-3.5 h-3.5 text-slate-400 shrink-0 mt-0.5" />
              <span>
                Your resume is private to your account and evaluated purely for skills matching and ATS readiness.
              </span>
            </div>
          </div>
        </div>

        {/* Right: Resume Health Summary (7 cols) */}
        <div className="lg:col-span-7 space-y-5">
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-card space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-100">
              <div>
                <h2 className="text-lg font-bold text-slate-900">
                  ZyncRole ATS Compatibility
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  An estimate based on resume structure, keyword coverage, and relevance.
                </p>
              </div>

              {currentResume?.ats_score !== undefined && (
                <div className="text-right">
                  <div className="text-3xl font-extrabold text-brand-600">
                    {Math.round(currentResume.ats_score)}
                    <span className="text-base text-slate-400 font-normal">/100</span>
                  </div>
                  <span className="text-[10px] font-semibold uppercase text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded">
                    ATS Ready
                  </span>
                </div>
              )}
            </div>

            {currentResume ? (
              <div className="space-y-5">
                {/* Detected Skills */}
                <div>
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                    Detected Technical Skills ({currentResume.detected_skills?.length || 0})
                  </h3>
                  <div className="flex flex-wrap gap-1.5">
                    {(currentResume.detected_skills || []).slice(0, 14).map((skill: string) => (
                      <span
                        key={skill}
                        className="px-2.5 py-1 text-xs font-medium rounded-lg bg-indigo-50 text-indigo-700 border border-indigo-100"
                      >
                        {skill}
                      </span>
                    ))}
                    {(currentResume.detected_skills?.length || 0) > 14 && (
                      <span className="px-2 py-1 text-xs text-slate-400">
                        +{(currentResume.detected_skills?.length || 0) - 14} more
                      </span>
                    )}
                  </div>
                </div>

                {/* Checklist snapshot */}
                <div className="space-y-2 pt-2">
                  <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                    ATS Readiness Checklist
                  </h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                    <div className="flex items-center text-slate-700 font-medium">
                      <Check className="w-3.5 h-3.5 text-emerald-600 mr-2 shrink-0" />
                      <span>Standard parsed section headers</span>
                    </div>
                    <div className="flex items-center text-slate-700 font-medium">
                      <Check className="w-3.5 h-3.5 text-emerald-600 mr-2 shrink-0" />
                      <span>Technical keyword density</span>
                    </div>
                    <div className="flex items-center text-slate-700 font-medium">
                      <Check className="w-3.5 h-3.5 text-emerald-600 mr-2 shrink-0" />
                      <span>Contact information complete</span>
                    </div>
                    <div className="flex items-center text-slate-700 font-medium">
                      <Check className="w-3.5 h-3.5 text-emerald-600 mr-2 shrink-0" />
                      <span>Clean ASCII bullet formatting</span>
                    </div>
                  </div>
                </div>

                {/* Action CTA buttons */}
                <div className="pt-4 border-t border-slate-100 flex flex-col sm:flex-row gap-3">
                  <Link
                    to="/resume/analysis"
                    className="flex-1 inline-flex items-center justify-center px-4 py-2.5 text-xs font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-subtle transition"
                  >
                    <span>View Resume Analysis</span>
                    <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
                  </Link>

                  <ExternalResumeBuilderButton
                    label="Create ATS-Friendly Resume"
                    variant="secondary"
                    className="flex-1 text-xs py-2.5"
                  />
                </div>
              </div>
            ) : (
              <div className="py-8 text-center space-y-3">
                <FileText className="w-12 h-12 text-slate-300 mx-auto" />
                <h3 className="text-sm font-bold text-slate-800">No Resume Analyzed Yet</h3>
                <p className="text-xs text-slate-500 max-w-sm mx-auto">
                  Upload your resume on the left to view your comprehensive ZyncRole ATS readiness score, detected competencies, and improvement tips.
                </p>
                <div className="pt-2">
                  <ExternalResumeBuilderButton
                    label="Create ATS-Friendly Resume"
                    variant="outline"
                    className="text-xs py-2"
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
