import React, { createContext, useContext, useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { User } from '@/types'

interface AuthContextType {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<{ onboarding_completed: boolean }>
  register: (firstName: string, lastName: string, email: string, password: string) => Promise<void>
  logout: () => void
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem('zyncrole_user')
    return saved ? JSON.parse(saved) : null
  })
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('zyncrole_token')
  })
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const verifyAuth = async () => {
      const storedToken = localStorage.getItem('zyncrole_token')
      if (storedToken) {
        try {
          const profile = await api.get<User>('/users/profile')
          setUser(profile)
          localStorage.setItem('zyncrole_user', JSON.stringify(profile))
        } catch {
          // Token invalid
          localStorage.removeItem('zyncrole_token')
          localStorage.removeItem('zyncrole_user')
          setUser(null)
          setToken(null)
        }
      }
      setIsLoading(false)
    }

    verifyAuth()

    const handleUnauthorized = () => {
      setUser(null)
      setToken(null)
    }

    window.addEventListener('auth-unauthorized', handleUnauthorized)
    return () => window.removeEventListener('auth-unauthorized', handleUnauthorized)
  }, [])

  const login = async (email: string, password: string) => {
    const res = await api.post<{
      access_token: string
      user: User
      onboarding_completed: boolean
    }>('/auth/login', { email, password })

    localStorage.setItem('zyncrole_token', res.access_token)
    localStorage.setItem('zyncrole_user', JSON.stringify(res.user))
    setToken(res.access_token)
    setUser(res.user)
    return { onboarding_completed: res.onboarding_completed }
  }

  const register = async (firstName: string, lastName: string, email: string, password: string) => {
    const res = await api.post<{
      access_token: string
      user: User
      onboarding_completed: boolean
    }>('/auth/register', {
      first_name: firstName,
      last_name: lastName,
      email,
      password
    })

    localStorage.setItem('zyncrole_token', res.access_token)
    localStorage.setItem('zyncrole_user', JSON.stringify(res.user))
    setToken(res.access_token)
    setUser(res.user)
  }

  const logout = () => {
    localStorage.removeItem('zyncrole_token')
    localStorage.removeItem('zyncrole_user')
    setToken(null)
    setUser(null)
  }

  const refreshUser = async () => {
    try {
      const profile = await api.get<User>('/users/profile')
      setUser(profile)
      localStorage.setItem('zyncrole_user', JSON.stringify(profile))
    } catch {
      // Ignore
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token && !!user,
        isLoading,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
