import React from 'react'
import { Link } from 'react-router-dom'
import {
  Sparkles,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  FileText,
  Layers,
  Compass,
  Zap,
  TrendingUp,
  Cpu
} from 'lucide-react'

export const LandingPage: React.FC = () => {
  return (
    <div className="bg-slate-50 overflow-hidden">
      {/* Hero Section */}
      <section className="relative pt-12 pb-20 sm:pt-16 sm:pb-24 lg:pt-20 lg:pb-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          {/* Badge */}
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-brand-50 border border-brand-200/80 text-brand-700 text-xs font-semibold mb-6 shadow-xs animate-fade-in">
            <Sparkles className="w-3.5 h-3.5 text-brand-600" />
            <span>Autonomous Career Intelligence Platform</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight max-w-4xl mx-auto leading-[1.12]">
            Find roles that fit you — <br className="hidden sm:inline" />
            <span className="text-brand-600">not the other way around.</span>
          </h1>

          {/* Subtitle */}
          <p className="mt-6 text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed font-normal">
            ZyncRole AI understands your resume, discovers verified opportunities across top employers, explains exactly why jobs match, and shows you the skills to unlock your next role.
          </p>

          {/* Action CTAs */}
          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4">
            <Link
              to="/register"
              className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3.5 rounded-xl text-sm font-semibold text-white bg-brand-600 hover:bg-brand-700 shadow-card transition-all duration-200 group"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
            <a
              href="#how-it-works"
              className="w-full sm:w-auto inline-flex items-center justify-center px-6 py-3.5 rounded-xl text-sm font-semibold text-slate-700 bg-white hover:bg-slate-100 border border-slate-200/90 shadow-subtle transition"
            >
              Explore How It Works
            </a>
          </div>

          {/* Product Preview Card */}
          <div className="mt-12 sm:mt-16 max-w-4xl mx-auto bg-white rounded-3xl shadow-float border border-slate-200/80 p-6 sm:p-8 text-left transition-all">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
              <div>
                <span className="text-xs font-semibold uppercase tracking-wider text-emerald-600 bg-emerald-50 px-2.5 py-1 rounded-md">
                  Live Feed Preview
                </span>
                <h3 className="text-xl font-bold text-slate-800 mt-2">
                  Machine Learning Engineer Intern
                </h3>
                <p className="text-sm text-slate-500">DeepPulse AI • Remote • Posted 3h ago</p>
              </div>

              <div className="flex items-center space-x-3 bg-emerald-50/80 border border-emerald-200/80 px-4 py-2 rounded-2xl">
                <div className="text-right">
                  <div className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">
                    Compatibility
                  </div>
                  <div className="text-xl font-extrabold text-emerald-700">92% Strong Match</div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6">
              <div>
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                  Why this matches you
                </h4>
                <div className="space-y-1.5 text-xs text-slate-600">
                  <div className="flex items-center text-slate-700 font-medium">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 mr-2 shrink-0" />
                    <span>Matches 4 core skills: Python, scikit-learn, SQL, Pandas</span>
                  </div>
                  <div className="flex items-center text-slate-700 font-medium">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 mr-2 shrink-0" />
                    <span>Entry-level & fresh graduates explicitly welcomed</span>
                  </div>
                  <div className="flex items-center text-slate-700 font-medium">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 mr-2 shrink-0" />
                    <span>Direct alignment with Machine Learning domain</span>
                  </div>
                </div>
              </div>

              <div>
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                  Skills to strengthen match
                </h4>
                <div className="flex flex-wrap gap-2 text-xs">
                  <span className="px-2.5 py-1 rounded-lg bg-amber-50 text-amber-800 border border-amber-200 font-medium">
                    Docker (Preferred)
                  </span>
                  <span className="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 font-medium">
                    PyTorch (Bonus)
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 mt-2">
                  Transparent reasoning generated strictly from verified resume data and requirements.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3-Step Simple Explanation */}
      <section id="how-it-works" className="py-16 sm:py-20 bg-white border-y border-slate-200/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto">
            <span className="text-xs font-bold uppercase tracking-wider text-brand-600">
              Effortless Intelligence
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 mt-2">
              Three steps to your personalized career feed
            </h2>
          </div>

          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-100 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-brand-100 text-brand-700 font-bold flex items-center justify-center">
                1
              </div>
              <h3 className="text-base font-bold text-slate-800">Upload your resume</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Drop your PDF, DOCX, or text resume. Our private parser extracts your skills, projects, and calculated ATS compatibility score.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-100 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-brand-100 text-brand-700 font-bold flex items-center justify-center">
                2
              </div>
              <h3 className="text-base font-bold text-slate-800">Understand your profile</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Profile Intelligence synthesizes your skills and preferences into an explainable candidate vector without overwriting your manual edits.
              </p>
            </div>

            <div className="p-6 rounded-2xl bg-slate-50 border border-slate-100 space-y-3">
              <div className="w-10 h-10 rounded-xl bg-brand-100 text-brand-700 font-bold flex items-center justify-center">
                3
              </div>
              <h3 className="text-base font-bold text-slate-800">Discover your opportunities</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                See top jobs ranked by mathematical compatibility, inspect skill gaps holding you back, and apply directly on the original employer portal.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Core Value Pillars */}
      <section className="py-16 sm:py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <span className="text-xs font-bold uppercase tracking-wider text-brand-600">
            Why ZyncRole AI
          </span>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 mt-2">
            Built for modern career navigation
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-subtle space-y-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <Compass className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-800">Personalized Job Matching</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              No generic chronological feeds. Your dashboard dynamically prioritizes the highest compatibility opportunities matching your experience and domain.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-subtle space-y-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <FileText className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-800">ATS Resume Intelligence</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Instant 7-dimension ATS readiness evaluation: keyword density, section completeness, quantified results, and free access to open-source ATS builders.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-subtle space-y-3">
            <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Cpu className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-800">Explainable Match Scores</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Every score comes with transparent reasoning. See matched skills, missing criteria, and clear steps to improve your compatibility.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-subtle space-y-3">
            <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center">
              <Layers className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-800">Skill Gap Intelligence</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Identify recurring skills required by your target jobs. Understand exactly which tools or frameworks will unlock the most matching roles.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-subtle space-y-3">
            <div className="w-10 h-10 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center">
              <Zap className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-800">Direct Source Transparency</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Every listing preserves its original source link (Greenhouse, Lever, Adzuna, etc.). One click redirects you straight to the authentic application page.
            </p>
          </div>

          <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-subtle space-y-3">
            <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <h3 className="text-base font-bold text-slate-800">Privacy & Zero-Cost</h3>
            <p className="text-sm text-slate-600 leading-relaxed">
              Your resume data remains private to your account. No paid subscriptions, no paywalls, and no unauthorized scraping.
            </p>
          </div>
        </div>
      </section>

      {/* Final Call to Action */}
      <section className="py-16 sm:py-20 bg-brand-600 text-white text-center">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
            Ready for an intelligent career feed?
          </h2>
          <p className="mt-4 text-brand-100 max-w-xl mx-auto text-sm sm:text-base">
            Upload your resume today and let autonomous career intelligence discover and explain your best opportunities.
          </p>
          <div className="mt-8">
            <Link
              to="/register"
              className="inline-flex items-center px-6 py-3.5 rounded-xl text-sm font-semibold text-brand-700 bg-white hover:bg-slate-50 shadow-float transition-all group"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
