import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { ApplicationItem } from '@/types'
import { getScoreColor } from '@/lib/utils'
import {
  Briefcase,
  ExternalLink,
  Plus,
  Trash2,
  FileEdit,
  Building,
  MapPin,
  LayoutGrid,
  List as ListIcon
} from 'lucide-react'

const STAGES = [
  { id: 'Applied', name: 'Applied', color: 'bg-blue-50 text-blue-700 border-blue-200' },
  { id: 'Assessment', name: 'Assessment', color: 'bg-amber-50 text-amber-700 border-amber-200' },
  { id: 'Interview', name: 'Interview', color: 'bg-indigo-50 text-indigo-700 border-indigo-200' },
  { id: 'Offer', name: 'Offer', color: 'bg-emerald-50 text-emerald-700 border-emerald-200' },
  { id: 'Rejected', name: 'Archived / Rejected', color: 'bg-slate-100 text-slate-600 border-slate-200' }
]

export const ApplicationsPage: React.FC = () => {
  const [applications, setApplications] = useState<ApplicationItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [viewMode, setViewMode] = useState<'kanban' | 'table'>('kanban')
  const [editingApp, setEditingApp] = useState<ApplicationItem | null>(null)
  const [notesInput, setNotesInput] = useState('')
  const [isUpdating, setIsUpdating] = useState(false)

  const fetchApplications = async () => {
    setIsLoading(true)
    try {
      const data = await api.get<ApplicationItem[]>('/applications')
      setApplications(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Failed to load applications:', err)
      setApplications([])
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchApplications()
  }, [])

  const handleStatusChange = async (appId: string, newStatus: string) => {
    try {
      await api.patch(`/applications/${appId}`, { status: newStatus })
      setApplications((prev) =>
        prev.map((app) => (app.id === appId ? { ...app, status: newStatus } : app))
      )
    } catch (err) {
      console.error('Failed to update status:', err)
    }
  }

  const handleDelete = async (appId: string) => {
    if (!window.confirm('Are you sure you want to remove this application from tracking?')) return
    try {
      await api.delete(`/applications/${appId}`)
      setApplications((prev) => prev.filter((app) => app.id !== appId))
    } catch (err) {
      console.error('Failed to delete application:', err)
    }
  }

  const handleSaveNotes = async () => {
    if (!editingApp) return
    setIsUpdating(true)
    try {
      await api.patch(`/applications/${editingApp.id}`, { notes: notesInput })
      setApplications((prev) =>
        prev.map((app) => (app.id === editingApp.id ? { ...app, notes: notesInput } : app))
      )
      setEditingApp(null)
    } catch (err) {
      console.error('Failed to save notes:', err)
    } finally {
      setIsUpdating(false)
    }
  }

  const totalCount = applications.length
  const inProgressCount = applications.filter((a) =>
    ['Assessment', 'Interview'].includes(a.status)
  ).length
  const offerCount = applications.filter((a) => a.status === 'Offer').length
  const responseRate = totalCount
    ? Math.round(((inProgressCount + offerCount) / totalCount) * 100)
    : 0

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-lg bg-brand-50 text-brand-600">
              <Briefcase className="w-5 h-5" />
            </span>
            <h1 className="text-2xl font-bold text-slate-900">Application Pipeline</h1>
          </div>
          <p className="mt-1 text-sm text-slate-500">
            Organize every opportunity you have applied to, track recruitment stages, and maintain follow-up notes.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {/* View Mode Toggle */}
          <div className="flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200">
            <button
              onClick={() => setViewMode('kanban')}
              className={`p-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                viewMode === 'kanban'
                  ? 'bg-white text-slate-800 shadow-xs'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <LayoutGrid className="w-4 h-4" />
              Board
            </button>
            <button
              onClick={() => setViewMode('table')}
              className={`p-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                viewMode === 'table'
                  ? 'bg-white text-slate-800 shadow-xs'
                  : 'text-slate-500 hover:text-slate-800'
              }`}
            >
              <ListIcon className="w-4 h-4" />
              List
            </button>
          </div>

          <Link
            to="/jobs"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold shadow-sm transition-colors"
          >
            <Plus className="w-4 h-4" />
            Find New Opportunities
          </Link>
        </div>
      </div>

      {/* KPI Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-500">Total Tracked</div>
          <div className="mt-1 text-2xl font-bold text-slate-900">{totalCount}</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-500">In Active Stages</div>
          <div className="mt-1 text-2xl font-bold text-indigo-600">{inProgressCount}</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-500">Offers Received</div>
          <div className="mt-1 text-2xl font-bold text-emerald-600">{offerCount}</div>
        </div>
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs">
          <div className="text-xs font-medium text-slate-500">Response / Progress Rate</div>
          <div className="mt-1 text-2xl font-bold text-brand-600">{responseRate}%</div>
        </div>
      </div>

      {/* Main Content */}
      {isLoading ? (
        <div className="flex items-center justify-center p-16">
          <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : applications.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-lg mx-auto space-y-4">
          <div className="w-14 h-14 bg-slate-100 rounded-full flex items-center justify-center mx-auto text-slate-400">
            <Briefcase className="w-7 h-7" />
          </div>
          <div className="space-y-1">
            <h3 className="text-base font-semibold text-slate-800">No applications tracked yet</h3>
            <p className="text-sm text-slate-500">
              When you click &ldquo;Apply&rdquo; on any role in the Career Feed, you can track it here to monitor your progress.
            </p>
          </div>
          <Link
            to="/jobs"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-semibold shadow-sm transition-colors"
          >
            Explore Matching Jobs
          </Link>
        </div>
      ) : viewMode === 'kanban' ? (
        /* Kanban Board View */
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 items-start">
          {STAGES.map((stage) => {
            const stageApps = applications.filter((a) => {
              if (stage.id === 'Rejected') {
                return a.status === 'Rejected' || a.status === 'Archived'
              }
              return a.status === stage.id
            })

            return (
              <div
                key={stage.id}
                className="bg-slate-50/80 rounded-xl border border-slate-200/80 p-3 space-y-3 min-h-[450px] flex flex-col"
              >
                {/* Column Header */}
                <div className="flex items-center justify-between pb-2 border-b border-slate-200">
                  <div className="flex items-center gap-2">
                    <span
                      className={`text-xs font-semibold px-2 py-0.5 rounded-full border ${stage.color}`}
                    >
                      {stage.name}
                    </span>
                  </div>
                  <span className="text-xs font-bold text-slate-400">{stageApps.length}</span>
                </div>

                {/* Cards Container */}
                <div className="space-y-3 flex-1 overflow-y-auto">
                  {stageApps.map((app) => (
                    <div
                      key={app.id}
                      className="bg-white rounded-lg p-3.5 border border-slate-200/90 shadow-2xs hover:shadow-xs transition-shadow space-y-2.5 group"
                    >
                      <div className="flex items-start justify-between gap-2">
                        <Link
                          to={`/jobs/${app.job_id}`}
                          className="font-semibold text-slate-900 text-sm hover:text-brand-600 transition-colors line-clamp-1"
                        >
                          {app.job_title}
                        </Link>
                        {app.match_score && (
                          <span
                            className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${getScoreColor(
                              app.match_score
                            )}`}
                          >
                            {app.match_score}%
                          </span>
                        )}
                      </div>

                      <div className="text-xs text-slate-600 font-medium flex items-center gap-1">
                        <Building className="w-3 h-3 text-slate-400 shrink-0" />
                        <span className="truncate">{app.company}</span>
                      </div>

                      <div className="text-[11px] text-slate-400 flex items-center gap-1">
                        <MapPin className="w-3 h-3 shrink-0" />
                        <span className="truncate">
                          {app.location || 'Remote'} &bull; {app.work_mode}
                        </span>
                      </div>

                      {app.notes && (
                        <div className="p-2 rounded bg-amber-50/60 border border-amber-100 text-[11px] text-amber-900 line-clamp-2">
                          {app.notes}
                        </div>
                      )}

                      {/* Card Action footer */}
                      <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                        {/* Stage Selector */}
                        <select
                          value={app.status}
                          onChange={(e) => handleStatusChange(app.id, e.target.value)}
                          className="text-[11px] font-medium text-slate-600 bg-slate-50 border border-slate-200 rounded px-1.5 py-0.5 focus:outline-none focus:ring-1 focus:ring-brand-500"
                        >
                          {STAGES.map((s) => (
                            <option key={s.id} value={s.id}>
                              {s.name}
                            </option>
                          ))}
                        </select>

                        <div className="flex items-center gap-1 opacity-70 group-hover:opacity-100 transition-opacity">
                          <button
                            title="Edit Notes"
                            onClick={() => {
                              setEditingApp(app)
                              setNotesInput(app.notes || '')
                            }}
                            className="p-1 text-slate-400 hover:text-slate-700 rounded"
                          >
                            <FileEdit className="w-3.5 h-3.5" />
                          </button>
                          <a
                            href={app.apply_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            title="Open Original Application"
                            className="p-1 text-slate-400 hover:text-brand-600 rounded"
                          >
                            <ExternalLink className="w-3.5 h-3.5" />
                          </a>
                          <button
                            title="Remove"
                            onClick={() => handleDelete(app.id)}
                            className="p-1 text-slate-400 hover:text-rose-600 rounded"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}

                  {stageApps.length === 0 && (
                    <div className="py-8 text-center text-xs text-slate-400 border border-dashed border-slate-200 rounded-lg">
                      No roles in {stage.name}
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      ) : (
        /* Table View */
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-xs">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
              <thead className="bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-700 uppercase tracking-wider">
                <tr>
                  <th className="py-3.5 px-4">Role & Company</th>
                  <th className="py-3.5 px-4">Match Score</th>
                  <th className="py-3.5 px-4">Stage</th>
                  <th className="py-3.5 px-4">Applied Date</th>
                  <th className="py-3.5 px-4">Notes</th>
                  <th className="py-3.5 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {applications.map((app) => (
                  <tr key={app.id} className="hover:bg-slate-50/70 transition-colors">
                    <td className="py-3.5 px-4">
                      <div className="font-semibold text-slate-900 hover:text-brand-600">
                        <Link to={`/jobs/${app.job_id}`}>{app.job_title}</Link>
                      </div>
                      <div className="text-xs text-slate-500">
                        {app.company} &bull; {app.location || 'Remote'}
                      </div>
                    </td>
                    <td className="py-3.5 px-4">
                      {app.match_score ? (
                        <span
                          className={`text-xs font-bold px-2 py-0.5 rounded ${getScoreColor(
                            app.match_score
                          )}`}
                        >
                          {app.match_score}%
                        </span>
                      ) : (
                        <span className="text-xs text-slate-400">--</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4">
                      <select
                        value={app.status}
                        onChange={(e) => handleStatusChange(app.id, e.target.value)}
                        className="text-xs font-medium text-slate-700 bg-white border border-slate-200 rounded-lg px-2 py-1 focus:ring-1 focus:ring-brand-500"
                      >
                        {STAGES.map((s) => (
                          <option key={s.id} value={s.id}>
                            {s.name}
                          </option>
                        ))}
                      </select>
                    </td>
                    <td className="py-3.5 px-4 text-xs text-slate-500">
                      {new Date(app.applied_at).toLocaleDateString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        year: 'numeric'
                      })}
                    </td>
                    <td className="py-3.5 px-4 text-xs text-slate-600 max-w-xs truncate">
                      {app.notes || <span className="text-slate-400 italic">No notes</span>}
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => {
                            setEditingApp(app)
                            setNotesInput(app.notes || '')
                          }}
                          className="p-1.5 text-slate-400 hover:text-slate-700 rounded-lg hover:bg-slate-100"
                          title="Edit Notes"
                        >
                          <FileEdit className="w-4 h-4" />
                        </button>
                        <a
                          href={app.apply_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-1.5 text-slate-400 hover:text-brand-600 rounded-lg hover:bg-slate-100"
                          title="Visit Job Listing"
                        >
                          <ExternalLink className="w-4 h-4" />
                        </a>
                        <button
                          onClick={() => handleDelete(app.id)}
                          className="p-1.5 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-slate-100"
                          title="Delete"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Notes Modal */}
      {editingApp && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-200 space-y-4 animate-in fade-in zoom-in-95 duration-150">
            <div>
              <h3 className="text-base font-bold text-slate-900">Application Notes</h3>
              <p className="text-xs text-slate-500">
                {editingApp.job_title} at {editingApp.company}
              </p>
            </div>

            <textarea
              rows={4}
              value={notesInput}
              onChange={(e) => setNotesInput(e.target.value)}
              placeholder="Record interviewer name, interview dates, follow-up deadlines, or preparation notes..."
              className="w-full p-3 text-sm border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
            />

            <div className="flex justify-end gap-3">
              <button
                type="button"
                onClick={() => setEditingApp(null)}
                className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleSaveNotes}
                disabled={isUpdating}
                className="px-4 py-2 text-xs font-semibold bg-brand-600 text-white rounded-lg hover:bg-brand-700 shadow-sm transition-colors disabled:opacity-50"
              >
                {isUpdating ? 'Saving...' : 'Save Notes'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
