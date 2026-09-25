# Privacy Architecture & Data Sovereignty

> **User-first privacy, zero data monetization, and self-service right to erasure.**

---

## 1. Principles of Candidate Data Sovereignty

ZyncRole AI was built with a privacy-first foundation:

1. **Zero Data Monetization:**
   - Candidate resumes, contact details, notes, and activity histories are **never** sold, rented, or licensed to third-party data brokers or marketing networks.
2. **Deterministic Processing:**
   - Candidate data is processed solely to calculate personalized opportunity compatibility, identify career skill gaps, and provide actionable ATS resume feedback.
3. **No Hidden Tracking:**
   - Application tracking is strictly candidate-driven. We do not place hidden pixels or monitor candidate activity outside of the ZyncRole AI platform.

---

## 2. Right to Access & Self-Service Data Export

Every candidate maintains complete portability of their career intelligence portfolio:
- **Endpoint:** `GET /api/v1/users/export-data`
- **Settings Screen Action:** Click **"Export My Data (JSON)"** in Account Settings.
- **Export Package Includes:**
  - Full personal profile and contact information.
  - Selected career preferences (target roles, domains, salary thresholds, work modes).
  - Normalized candidate intelligence attributes (skills, education, projects, certifications).
  - Complete application pipeline records, status history, and personal notes.
  - Bookmarked / saved job references.

---

## 3. Right to Erasure & Account Purge

Candidates have an unconditional right to permanently delete their account and associated data at any time without administrative intervention:
- **Endpoint:** `DELETE /api/v1/users/account`
- **Settings Screen Action:** Click **"Delete Account & Purge Data"** and confirm by typing `"delete my account"`.
- **Purge Execution Workflow:**
  1. All uploaded resume files (`.pdf`, `.docx`, `.txt`) on disk storage are permanently removed.
  2. Cascade deletion executes across the database:
     - `profiles`
     - `career_preferences`
     - `candidate_profiles`
     - `resumes` and `resume_analyses`
     - `job_matches`
     - `saved_jobs`
     - `applications`
     - `notifications`
     - `user_activity`
  3. The user session is terminated and authentication tokens are invalidated.

---

## 4. External ATS Builder Privacy (OpenResume)

To maintain a lightweight, zero-cost, and private architecture:
- ZyncRole AI delegates resume document creation to **OpenResume**, an open-source, client-side ATS resume builder.
- When candidates click **"Build in ATS Format"**, OpenResume runs entirely in the candidate's browser without uploading their personal details to third-party database servers.
- Candidates remain in complete control of their PDF generation and local file downloads.
