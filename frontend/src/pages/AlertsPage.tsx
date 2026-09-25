import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '@/lib/api'
import { NotificationItem } from '@/types'
import {
  Bell,
  Sparkles,
  FileText,
  Briefcase,
  User,
  ArrowRight,
  CheckCheck
} from 'lucide-react'

export const AlertsPage: React.FC = () => {
  const [notifications, setNotifications] = useState<NotificationItem[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'unread'>('all')

  const fetchNotifications = async () => {
    setIsLoading(true)
    try {
      const data = await api.get<NotificationItem[]>('/notifications')
      setNotifications(Array.isArray(data) ? data : [])
    } catch (err) {
      console.error('Failed to load notifications:', err)
      setNotifications([])
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchNotifications()
  }, [])

  const handleMarkAsRead = async (id: string) => {
    try {
      await api.patch(`/notifications/${id}/read`, {})
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      )
    } catch (err) {
      console.error('Failed to mark notification as read:', err)
    }
  }

  const handleMarkAllRead = async () => {
    try {
      await api.post('/notifications/read-all', {})
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })))
    } catch (err) {
      console.error('Failed to mark all notifications as read:', err)
    }
  }

  const filteredNotifications = notifications.filter((n) => {
    if (filter === 'unread') return !n.is_read
    return true
  })

  const unreadCount = notifications.filter((n) => !n.is_read).length

  const getIconForType = (type: string) => {
    switch (type) {
      case 'opportunity':
      case 'match':
        return <Briefcase className="w-4 h-4 text-brand-600" />
      case 'resume':
        return <FileText className="w-4 h-4 text-emerald-600" />
      case 'profile':
        return <User className="w-4 h-4 text-indigo-600" />
      default:
        return <Sparkles className="w-4 h-4 text-amber-600" />
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 pb-6">
        <div>
          <div className="flex items-center gap-2">
            <span className="p-2 rounded-lg bg-brand-50 text-brand-600">
              <Bell className="w-5 h-5" />
            </span>
            <h1 className="text-2xl font-bold text-slate-900">Career Alerts & Notifications</h1>
          </div>
          <p className="mt-1 text-sm text-slate-500">
            Real-time updates on high-match opportunities, resume evaluations, and career intelligence.
          </p>
        </div>

        {unreadCount > 0 && (
          <button
            onClick={handleMarkAllRead}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-xs font-semibold text-slate-700 shadow-2xs transition-colors self-start sm:self-auto"
          >
            <CheckCheck className="w-4 h-4 text-slate-500" />
            Mark All as Read
          </button>
        )}
      </div>

      {/* Tabs / Filter bar */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors ${
            filter === 'all'
              ? 'bg-slate-900 text-white'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          All Updates ({notifications.length})
        </button>
        <button
          onClick={() => setFilter('unread')}
          className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5 ${
            filter === 'unread'
              ? 'bg-brand-600 text-white'
              : 'text-slate-600 hover:bg-slate-100'
          }`}
        >
          Unread
          {unreadCount > 0 && (
            <span className="w-4 h-4 rounded-full bg-brand-100 text-brand-700 text-[10px] flex items-center justify-center font-bold">
              {unreadCount}
            </span>
          )}
        </button>
      </div>

      {/* List */}
      {isLoading ? (
        <div className="flex items-center justify-center p-16">
          <div className="w-8 h-8 border-3 border-brand-600 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : filteredNotifications.length === 0 ? (
        <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center max-w-md mx-auto space-y-3">
          <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center mx-auto text-slate-400">
            <Bell className="w-6 h-6" />
          </div>
          <div className="text-sm font-semibold text-slate-800">
            {filter === 'unread' ? 'No unread notifications' : 'No notifications yet'}
          </div>
          <p className="text-xs text-slate-500">
            You will receive instant alerts when new opportunities match your career preferences.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {filteredNotifications.map((notif) => (
            <div
              key={notif.id}
              className={`p-4 rounded-xl border transition-all ${
                notif.is_read
                  ? 'bg-white border-slate-200 opacity-80 hover:opacity-100'
                  : 'bg-brand-50/30 border-brand-200 shadow-2xs'
              }`}
            >
              <div className="flex items-start gap-3">
                <div
                  className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 ${
                    notif.is_read ? 'bg-slate-100' : 'bg-white border border-brand-200 shadow-2xs'
                  }`}
                >
                  {getIconForType(notif.type)}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <h3
                      className={`text-sm ${
                        notif.is_read ? 'font-medium text-slate-800' : 'font-bold text-slate-900'
                      }`}
                    >
                      {notif.title}
                    </h3>
                    <span className="text-[11px] text-slate-400 shrink-0">
                      {new Date(notif.created_at).toLocaleDateString(undefined, {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                  </div>

                  <p className="mt-1 text-xs text-slate-600 leading-relaxed">
                    {notif.message}
                  </p>

                  <div className="mt-3 flex items-center gap-3">
                    {notif.link && (
                      <Link
                        to={notif.link}
                        onClick={() => !notif.is_read && handleMarkAsRead(notif.id)}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-brand-600 hover:text-brand-700"
                      >
                        View Details
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    )}

                    {!notif.is_read && (
                      <button
                        onClick={() => handleMarkAsRead(notif.id)}
                        className="text-xs font-medium text-slate-400 hover:text-slate-600"
                      >
                        Mark as read
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
