import React, { Component, ErrorInfo, ReactNode } from 'react'
import { AlertCircle, RefreshCw } from 'lucide-react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  }

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught:', error, errorInfo)
  }

  private handleRetry = () => {
    this.setState({ hasError: false })
    window.location.reload()
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-[50vh] flex items-center justify-center p-6">
          <div className="max-w-md w-full p-8 bg-white rounded-3xl shadow-card border border-slate-200/80 text-center">
            <div className="w-12 h-12 rounded-2xl bg-rose-50 text-rose-600 flex items-center justify-center mx-auto mb-4">
              <AlertCircle className="w-6 h-6" />
            </div>
            <h2 className="text-lg font-bold text-slate-800">Something went wrong</h2>
            <p className="mt-2 text-sm text-slate-600 leading-relaxed">
              Something went wrong. Your data is safe. Please refresh and try again.
            </p>
            <div className="mt-6">
              <button
                onClick={this.handleRetry}
                className="inline-flex items-center px-4 py-2.5 text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 rounded-xl shadow-subtle transition"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                <span>Retry</span>
              </button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
