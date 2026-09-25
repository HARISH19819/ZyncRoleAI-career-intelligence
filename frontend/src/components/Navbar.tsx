import React, { useState, useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import {
  Compass,
  FileText,
  Briefcase,
  Bookmark,
  TrendingUp,
  Layers,
  Bell,
  User,
  LogOut,
  Menu,
  X,
  Sparkles,
  Settings
} from 'lucide-react'
import { useAuth } from '@/contexts/AuthContext'
import { api } from '@/lib/api'
import { NotificationItem } from '@/types'

export const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [notificationsOpen, setNotificationsOpen] = useState(false)
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false)
  const [notifications, setNotifications] = useState<NotificationItem[]>([])
  const [unreadCount, setUnreadCount] = useState(0)

  useEffect(() => {
    if (isAuthenticated) {
      const fetchNotifications = async () => {
        try {
          const notifs = await api.get<NotificationItem[]>('/notifications')
          setNotifications(notifs)
          setUnreadCount(notifs.filter((n) => !n.is_read).length)
        } catch {
          // Ignore
        }
      }
      fetchNotifications()
    }
  }, [isAuthenticated, location.pathname])

  const handleMarkAllRead = async () => {
    try {
      await api.post('/notifications/read-all')
      setNotifications((prev) => prev.map((n) => ({ ...n, is_read: true })))
      setUnreadCount(0)
    } catch {
      // Ignore
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navLinks = [
    { name: 'Dashboard', path: '/dashboard', icon: Compass },
    { name: 'Jobs', path: '/jobs', icon: Briefcase },
    { name: 'Resume', path: '/resume', icon: FileText },
    { name: 'Skill Gaps', path: '/skill-gaps', icon: Layers },
    { name: 'Career', path: '/career', icon: TrendingUp },
    { name: 'Saved', path: '/saved', icon: Bookmark },
    { name: 'Applications', path: '/applications', icon: Briefcase },
  ]

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Product Identity */}
          <div className="flex items-center space-x-3">
            <Link to={isAuthenticated ? '/dashboard' : '/'} className="flex items-center space-x-2.5 group">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center text-white shadow-subtle group-hover:scale-105 transition-transform">
                <Sparkles className="w-5 h-5" />
              </div>
              <div className="flex flex-col">
                <span className="font-bold text-lg text-slate-900 tracking-tight leading-none group-hover:text-brand-600 transition-colors">
                  ZyncRole<span className="text-brand-600 font-extrabold ml-0.5">AI</span>
                </span>
                <span className="text-[10px] text-slate-400 font-medium tracking-tight hidden sm:block">
                  Career Intelligence
                </span>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          {isAuthenticated && (
            <nav className="hidden md:flex items-center space-x-1 lg:space-x-2">
              {navLinks.map((link) => {
                const isActive = location.pathname === link.path
                const Icon = link.icon
                return (
                  <Link
                    key={link.name}
                    to={link.path}
                    className={`inline-flex items-center px-3 py-2 rounded-lg text-xs lg:text-sm font-medium transition-all ${
                      isActive
                        ? 'bg-brand-50 text-brand-700 font-semibold shadow-xs'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                    }`}
                  >
                    <Icon className="w-4 h-4 mr-1.5 opacity-70" />
                    <span>{link.name}</span>
                  </Link>
                )
              })}
            </nav>
          )}

          {/* Right Header: Alerts & Profile / Auth buttons */}
          <div className="flex items-center space-x-2">
            {isAuthenticated ? (
              <>
                {/* Notifications Bell */}
                <div className="relative">
                  <button
                    type="button"
                    onClick={() => {
                      setNotificationsOpen(!notificationsOpen)
                      setProfileDropdownOpen(false)
                    }}
                    className="p-2 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-xl relative transition"
                    aria-label="View notifications"
                  >
                    <Bell className="w-5 h-5" />
                    {unreadCount > 0 && (
                      <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-brand-600 rounded-full ring-2 ring-white" />
                    )}
                  </button>

                  {/* Notification Dropdown */}
                  {notificationsOpen && (
                    <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-2xl shadow-float border border-slate-100 py-3 z-50 animate-fade-in">
                      <div className="px-4 pb-2 border-b border-slate-100 flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                          Notifications ({unreadCount})
                        </span>
                        {unreadCount > 0 && (
                          <button
                            onClick={handleMarkAllRead}
                            className="text-xs text-brand-600 hover:underline"
                          >
                            Mark all read
                          </button>
                        )}
                      </div>

                      <div className="max-h-72 overflow-y-auto divide-y divide-slate-50">
                        {notifications.length > 0 ? (
                          notifications.slice(0, 6).map((notif) => (
                            <Link
                              key={notif.id}
                              to={notif.link || '/alerts'}
                              onClick={() => setNotificationsOpen(false)}
                              className={`p-3 block hover:bg-slate-50 transition ${
                                !notif.is_read ? 'bg-brand-50/30' : ''
                              }`}
                            >
                              <p className="text-xs font-semibold text-slate-800">{notif.title}</p>
                              <p className="text-xs text-slate-500 mt-0.5 line-clamp-2">{notif.message}</p>
                            </Link>
                          ))
                        ) : (
                          <div className="p-4 text-center text-xs text-slate-400">
                            No notifications right now.
                          </div>
                        )}
                      </div>

                      <div className="pt-2 px-4 border-t border-slate-100 text-center">
                        <Link
                          to="/alerts"
                          onClick={() => setNotificationsOpen(false)}
                          className="text-xs font-medium text-brand-600 hover:text-brand-700"
                        >
                          View all notifications
                        </Link>
                      </div>
                    </div>
                  )}
                </div>

                {/* Profile Avatar Dropdown */}
                <div className="relative">
                  <button
                    type="button"
                    onClick={() => {
                      setProfileDropdownOpen(!profileDropdownOpen)
                      setNotificationsOpen(false)
                    }}
                    className="flex items-center space-x-2 p-1.5 rounded-xl hover:bg-slate-100 transition"
                  >
                    <div className="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 font-bold text-xs flex items-center justify-center border border-indigo-200">
                      {user?.first_name?.charAt(0) || 'U'}
                    </div>
                    <span className="text-xs font-medium text-slate-700 hidden sm:block">
                      {user?.first_name}
                    </span>
                  </button>

                  {profileDropdownOpen && (
                    <div className="absolute right-0 mt-2 w-52 bg-white rounded-2xl shadow-float border border-slate-100 py-2 z-50 animate-fade-in">
                      <div className="px-4 py-2 border-b border-slate-100">
                        <p className="text-xs font-semibold text-slate-800">
                          {user?.first_name} {user?.last_name}
                        </p>
                        <p className="text-[11px] text-slate-500 truncate">{user?.email}</p>
                      </div>

                      <Link
                        to="/profile"
                        onClick={() => setProfileDropdownOpen(false)}
                        className="flex items-center px-4 py-2 text-xs text-slate-700 hover:bg-slate-50"
                      >
                        <User className="w-4 h-4 mr-2 text-slate-400" />
                        Career Profile
                      </Link>

                      <Link
                        to="/settings"
                        onClick={() => setProfileDropdownOpen(false)}
                        className="flex items-center px-4 py-2 text-xs text-slate-700 hover:bg-slate-50"
                      >
                        <Settings className="w-4 h-4 mr-2 text-slate-400" />
                        Settings & Privacy
                      </Link>

                      <div className="border-t border-slate-100 my-1" />

                      <button
                        type="button"
                        onClick={handleLogout}
                        className="w-full flex items-center px-4 py-2 text-xs text-rose-600 hover:bg-rose-50 transition"
                      >
                        <LogOut className="w-4 h-4 mr-2" />
                        Log out
                      </button>
                    </div>
                  )}
                </div>

                {/* Mobile Menu Toggle Button */}
                <button
                  type="button"
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  className="md:hidden p-2 text-slate-500 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition"
                >
                  {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
                </button>
              </>
            ) : (
              <div className="flex items-center space-x-2">
                <Link
                  to="/login"
                  className="px-3.5 py-1.5 text-xs sm:text-sm font-medium text-slate-700 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition"
                >
                  Log in
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-1.5 text-xs sm:text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-lg shadow-subtle transition"
                >
                  Get Started Free
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Mobile Navigation Drawer */}
      {isAuthenticated && mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200/80 bg-white px-4 pt-2 pb-4 space-y-1 animate-fade-in">
          {navLinks.map((link) => {
            const isActive = location.pathname === link.path
            const Icon = link.icon
            return (
              <Link
                key={link.name}
                to={link.path}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center px-3 py-2.5 rounded-xl text-sm font-medium transition ${
                  isActive ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                <Icon className="w-4 h-4 mr-3 opacity-70" />
                <span>{link.name}</span>
              </Link>
            )
          })}
          <div className="border-t border-slate-100 pt-2 mt-2">
            <button
              onClick={handleLogout}
              className="w-full flex items-center px-3 py-2.5 rounded-xl text-sm font-medium text-rose-600 hover:bg-rose-50"
            >
              <LogOut className="w-4 h-4 mr-3" />
              Log out
            </button>
          </div>
        </div>
      )}
    </header>
  )
}
