import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from '@/contexts/AuthContext'
import { AppLayout, PublicLayout } from '@/layouts/AppLayout'

// Public Pages
import { LandingPage } from '@/pages/LandingPage'
import { LoginPage } from '@/pages/LoginPage'
import { RegisterPage } from '@/pages/RegisterPage'
import { ForgotPasswordPage } from '@/pages/ForgotPasswordPage'

// Protected & Core Pages
import { DashboardPage } from '@/pages/DashboardPage'
import { OnboardingPage } from '@/pages/OnboardingPage'
import { JobExplorerPage } from '@/pages/JobExplorerPage'
import { JobDetailPage } from '@/pages/JobDetailPage'
import { ResumePage } from '@/pages/ResumePage'
import { ResumeAnalysisPage } from '@/pages/ResumeAnalysisPage'
import { ProfilePage } from '@/pages/ProfilePage'
import { SkillGapsPage } from '@/pages/SkillGapsPage'
import { CareerPage } from '@/pages/CareerPage'
import { SavedJobsPage } from '@/pages/SavedJobsPage'
import { ApplicationsPage } from '@/pages/ApplicationsPage'
import { AlertsPage } from '@/pages/AlertsPage'
import { SettingsPage } from '@/pages/SettingsPage'
import { NotFoundPage } from '@/pages/NotFoundPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000
    }
  }
})

export const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public Layout */}
            <Route element={<PublicLayout />}>
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/forgot-password" element={<ForgotPasswordPage />} />
              <Route path="/jobs" element={<JobExplorerPage />} />
              <Route path="/jobs/:id" element={<JobDetailPage />} />
              <Route path="/career" element={<CareerPage />} />
            </Route>

            {/* Authenticated Protected Layout */}
            <Route element={<AppLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/onboarding" element={<OnboardingPage />} />
              <Route path="/resume" element={<ResumePage />} />
              <Route path="/resume/analysis" element={<ResumeAnalysisPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/skill-gaps" element={<SkillGapsPage />} />
              <Route path="/saved" element={<SavedJobsPage />} />
              <Route path="/applications" element={<ApplicationsPage />} />
              <Route path="/alerts" element={<AlertsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>

            {/* Fallback & 404 */}
            <Route element={<PublicLayout />}>
              <Route path="/404" element={<NotFoundPage />} />
              <Route path="*" element={<NotFoundPage />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
