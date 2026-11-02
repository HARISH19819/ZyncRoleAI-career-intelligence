import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_presentation(output_path="ZyncRole_AI_Presentation.pptx"):
    prs = Presentation()
    # 16:9 Widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette - Professional Deep Tech Theme
    BG_DARK = RGBColor(11, 15, 25)        # #0B0F19 - Main Dark Background
    CARD_BG = RGBColor(24, 34, 53)        # #182235 - Card Background
    CARD_BORDER = RGBColor(40, 56, 85)    # #283855 - Card Border
    ACCENT_BLUE = RGBColor(59, 130, 246)  # #3B82F6 - Primary Brand Blue
    ACCENT_CYAN = RGBColor(6, 182, 212)   # #06B6D4 - Secondary Accent Cyan
    ACCENT_GREEN = RGBColor(16, 185, 129) # #10B981 - Success / Highlight Green
    ACCENT_AMBER = RGBColor(245, 158, 11) # #F59E0B - Accent Amber
    TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC - Primary White Text
    TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8 - Secondary Gray Text
    TEXT_DIM = RGBColor(100, 116, 139)    # #64748B - Muted Slate

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, category_text, title_text, subtitle_text=None):
        # Category Badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.name = "Arial"
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.5), Inches(0.65))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

        # Subtitle
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.5), Inches(0.4))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.name = "Arial"
            p_sub.font.size = Pt(13)
            p_sub.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 1: COVER SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative background card
    bg_accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    bg_accent.fill.solid()
    bg_accent.fill.fore_color.rgb = CARD_BG
    bg_accent.line.color.rgb = CARD_BORDER
    bg_accent.line.width = Pt(1.5)

    # Pill badge
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.3), Inches(3.6), Inches(0.42))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(17, 24, 39)
    pill.line.color.rgb = ACCENT_BLUE
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = "NEXT-GEN CAREER INTELLIGENCE"
    p_pill.font.name = "Arial"
    p_pill.font.size = Pt(10)
    p_pill.font.bold = True
    p_pill.font.color.rgb = ACCENT_CYAN
    p_pill.alignment = PP_ALIGN.CENTER

    # Title & Tagline
    title_box = s1.shapes.add_textbox(Inches(1.3), Inches(1.9), Inches(10.7), Inches(2.2))
    tf = title_box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "ZyncRole AI"
    p1.font.name = "Arial"
    p1.font.size = Pt(50)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf.add_paragraph()
    p2.text = "One Resume. Every Opportunity. One Intelligent Career Feed."
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.color.rgb = ACCENT_BLUE
    p2.font.bold = True
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Autonomous AI job matching, 7-dimension ATS diagnostics, deterministic compatibility scoring, and real-time market intelligence."
    p3.font.name = "Arial"
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(10)

    # Feature Highlights Badges (3 columns)
    badges = [
        ("8-Dimension Match Engine", "100% deterministic mathematical compatibility calculation"),
        ("7-Dimension ATS Diagnostic", "Deep resume keyword, structure, and impact evaluation"),
        ("Zero-Cost Production", "Engineered for 100% free-tier cloud deployment")
    ]
    for i, (b_title, b_desc) in enumerate(badges):
        x = Inches(1.3 + i * 3.7)
        card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(4.5), Inches(3.45), Inches(1.6))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(15, 23, 42)
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.2)
        ctf.margin_top = Inches(0.2)
        cp1 = ctf.paragraphs[0]
        cp1.text = b_title
        cp1.font.name = "Arial"
        cp1.font.size = Pt(13)
        cp1.font.bold = True
        cp1.font.color.rgb = ACCENT_GREEN

        cp2 = ctf.add_paragraph()
        cp2.text = b_desc
        cp2.font.name = "Arial"
        cp2.font.size = Pt(11)
        cp2.font.color.rgb = TEXT_MUTED
        cp2.space_before = Pt(4)

    # ==========================================
    # SLIDE 2: PROBLEM STATEMENT
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Core Challenge", "The Broken Hiring Pipeline & Job Search Friction",
               "Candidates and recruiters struggle in a fragmented, opaque, and algorithmic black-box ecosystem.")

    problems = [
        ("01", "Fragmented Opportunities",
         "Job listings are scattered across dozens of disconnected platforms, proprietary ATS boards (Greenhouse, Lever, Ashby), and generic job portals, forcing repetitive manual searches.",
         ACCENT_CYAN),
        ("02", "The ATS 'Black Hole'",
         "Over 75% of resumes are filtered out by automated Applicant Tracking Systems without candidates ever receiving actionable feedback, scoring breakdowns, or missing-skill insights.",
         ACCENT_AMBER),
        ("03", "Hallucinated & Unreliable Matches",
         "Standard generative AI job tools invent non-existent connections or rely on generic keyword matching, giving unpredictable scores and zero auditable mathematical explanation.",
         RGBColor(239, 68, 68)), # Red
        ("04", "Skill Ambiguity & Career Guesswork",
         "Job seekers lack factual market intelligence showing exactly which recurring skills are missing across target roles, leading to misdirected upskilling and rejected applications.",
         ACCENT_BLUE)
    ]

    for i, (num, p_title, p_desc, color) in enumerate(problems):
        row = i // 2
        col = i % 2
        x = Inches(0.8 + col * 5.95)
        y = Inches(2.0 + row * 2.5)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.75), Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.25)

        # Number & Title
        p_num = tf.paragraphs[0]
        p_num.text = f"{num}  •  {p_title}"
        p_num.font.name = "Arial"
        p_num.font.size = Pt(15)
        p_num.font.bold = True
        p_num.font.color.rgb = color

        p_body = tf.add_paragraph()
        p_body.text = p_desc
        p_body.font.name = "Arial"
        p_body.font.size = Pt(12)
        p_body.font.color.rgb = TEXT_MUTED
        p_body.space_before = Pt(8)

    # ==========================================
    # SLIDE 3: PROPOSED SOLUTION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "The Innovation", "The ZyncRole AI Solution Architecture",
               "An autonomous, deterministic career intelligence engine delivering radical transparency and zero scraping.")

    solutions = [
        ("Ethical Ingestion & Unified Feed",
         "Aggregates job postings from authorized developer APIs (Adzuna, Arbeitnow, Remotive, The Muse) and public ATS boards (Greenhouse, Lever, Ashby) with zero unauthorized web scraping.",
         ["Compliant ATS APIs", "Automatic Normalization", "Fast SHA-256 Deduplication"]),
        ("Deterministic 8-Dimension Matching",
         "Replaces black-box hallucinations with a mathematically auditable compatibility formula (0–100%) evaluating skills, roles, domains, experience, education, locations, and semantic vectors.",
         ["Auditable 0–100% Score", "No Random LLM Hallucinations", "Balanced Multi-Vector Scoring"]),
        ("7-Dimension ATS Resume Diagnostic",
         "Evaluates resumes across keywords, role alignment, structure, project depth, formatting, and impact metrics with direct 1-click export to OpenResume for instant correction.",
         ["Keyword & Section Audit", "Actionable Improvement Steps", "Direct OpenResume Builder"]),
        ("Market Skill Gap Intelligence",
         "Automatically aggregates recurring missing skills across target opportunities, classifying upskilling priorities into High, Medium, and Low market impact ratings.",
         ["Recurring Gap Aggregation", "Market Demand Analytics", "Personalized Learning Focus"])
    ]

    for i, (sol_title, sol_desc, bullets) in enumerate(solutions):
        row = i // 2
        col = i % 2
        x = Inches(0.8 + col * 5.95)
        y = Inches(2.0 + row * 2.5)

        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.75), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.3)
        tf.margin_top = Inches(0.2)

        p_t = tf.paragraphs[0]
        p_t.text = sol_title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_GREEN

        p_d = tf.add_paragraph()
        p_d.text = sol_desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(4)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = f"✓  {b}"
            p_b.font.name = "Arial"
            p_b.font.size = Pt(10.5)
            p_b.font.bold = True
            p_b.font.color.rgb = ACCENT_CYAN
            p_b.space_before = Pt(3)

    # ==========================================
    # SLIDE 4: TECHNICAL WORKFLOW
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "End-To-End Architecture", "Technical Workflow & Data Processing Pipeline",
               "How data flows autonomously from raw ingestion and resume parsing to deterministic matching.")

    pipeline_steps = [
        ("Step 1", "Multi-Source Job Ingestion",
         "Ingests listings via HTTPX async coroutines from ATS APIs (Greenhouse, Lever, Ashby) and public job feeds (Adzuna, Remotive, Arbeitnow).",
         ACCENT_BLUE),
        ("Step 2", "Normalization & Deduplication",
         "Cleans job titles, extracts canonical skills, clusters domains, and removes duplicates using SHA-256 content hashes and RapidFuzz token matching.",
         ACCENT_CYAN),
        ("Step 3", "Resume Parsing & ATS Diagnostic",
         "PyMuPDF and python-docx extract plain text, sections, and contact metadata. ATSEngine scores readiness across 7 weighted dimensions.",
         ACCENT_GREEN),
        ("Step 4", "Dual Semantic Vectorization",
         "Generates 768-dimensional vector embeddings via Google Gemini Embedding 2 with automatic fallback to Scikit-Learn TF-IDF for zero-cost runtime.",
         ACCENT_AMBER),
        ("Step 5", "Deterministic Matching & Explanations",
         "8-dimension engine calculates exact 0-100% compatibility. ExplanationAgent generates human-readable strengths, gaps, and recommendations.",
         RGBColor(168, 85, 247)) # Purple
    ]

    card_width = Inches(2.26)
    gap = Inches(0.12)
    start_x = Inches(0.8)

    for i, (step_num, step_name, step_desc, color) in enumerate(pipeline_steps):
        x = start_x + i * (card_width + gap)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), card_width, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.25)

        p_num = tf.paragraphs[0]
        p_num.text = step_num
        p_num.font.name = "Arial"
        p_num.font.size = Pt(11)
        p_num.font.bold = True
        p_num.font.color.rgb = color

        p_name = tf.add_paragraph()
        p_name.text = step_name
        p_name.font.name = "Arial"
        p_name.font.size = Pt(14)
        p_name.font.bold = True
        p_name.font.color.rgb = TEXT_WHITE
        p_name.space_before = Pt(6)

        p_desc = tf.add_paragraph()
        p_desc.text = step_desc
        p_desc.font.name = "Arial"
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = TEXT_MUTED
        p_desc.space_before = Pt(10)

    # ==========================================
    # SLIDE 5: 8-DIMENSION MATCHING ENGINE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Auditable Evaluation", "The 8-Dimension Compatibility Formula",
               "Deterministic, mathematically grounded scoring that completely eliminates LLM hallucinations.")

    # Left Column: The Formula Card
    calc_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(4.3), Inches(4.8))
    calc_card.fill.solid()
    calc_card.fill.fore_color.rgb = CARD_BG
    calc_card.line.color.rgb = ACCENT_BLUE
    calc_card.line.width = Pt(1.5)

    tf_calc = calc_card.text_frame
    tf_calc.word_wrap = True
    tf_calc.margin_left = tf_calc.margin_right = Inches(0.25)
    tf_calc.margin_top = Inches(0.3)

    p_f1 = tf_calc.paragraphs[0]
    p_f1.text = "Mathematical Integrity"
    p_f1.font.name = "Arial"
    p_f1.font.size = Pt(16)
    p_f1.font.bold = True
    p_f1.font.color.rgb = ACCENT_CYAN

    p_f2 = tf_calc.add_paragraph()
    p_f2.text = "S_total = 100 × ∑ (w_i × s_i)"
    p_f2.font.name = "Courier New"
    p_f2.font.size = Pt(16)
    p_f2.font.bold = True
    p_f2.font.color.rgb = TEXT_WHITE
    p_f2.space_before = Pt(12)

    formula_points = [
        "Strict Weight Validation: Sum of all weights strictly equals 1.00 dynamically on startup.",
        "Zero Hallucination: Explanations are generated exclusively from computed mathematical facts.",
        "Candidate Transparency: Candidates see the exact contribution of each factor and how to boost their score.",
        "Adaptive Penalties: Missing required skills incur 3x higher impact than missing preferred bonus skills."
    ]
    for pt in formula_points:
        p_pt = tf_calc.add_paragraph()
        p_pt.text = f"•  {pt}"
        p_pt.font.name = "Arial"
        p_pt.font.size = Pt(11)
        p_pt.font.color.rgb = TEXT_MUTED
        p_pt.space_before = Pt(10)

    # Right Column: The 8 Dimensions Table/Cards (2 columns of 4)
    dimensions = [
        ("1. Skills Match", "25% - 30%", "Canonical taxonomy Jaccard overlap (75% req / 25% pref)"),
        ("2. Role Alignment", "15%", "RapidFuzz token set ratio between target roles & job title"),
        ("3. Domain Alignment", "10% - 15%", "Clustering across 20+ specialized engineering tracks"),
        ("4. Experience Fit", "10% - 15%", "Candidate level vs requirements with fresher-friendly rules"),
        ("5. Education Fit", "5% - 10%", "Degree level and technical specialization alignment"),
        ("6. Location & Mobility", "5% - 10%", "Geographic matching and remote-work tolerance scoring"),
        ("7. Preferences Fit", "5%", "Employment type and work mode compliance check"),
        ("8. Semantic Similarity", "10% - 15%", "Gemini Embedding 2 cosine distance (or TF-IDF fallback)")
    ]

    for idx, (d_name, d_wt, d_desc) in enumerate(dimensions):
        col = idx // 4
        row = idx % 4
        x = Inches(5.3 + col * 3.6)
        y = Inches(2.0 + row * 1.2)

        d_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.45), Inches(1.08))
        d_card.fill.solid()
        d_card.fill.fore_color.rgb = CARD_BG
        d_card.line.color.rgb = CARD_BORDER
        d_card.line.width = Pt(1)

        dtf = d_card.text_frame
        dtf.word_wrap = True
        dtf.margin_left = dtf.margin_right = Inches(0.15)
        dtf.margin_top = Inches(0.12)

        p_h = dtf.paragraphs[0]
        p_h.text = f"{d_name}  ({d_wt})"
        p_h.font.name = "Arial"
        p_h.font.size = Pt(12)
        p_h.font.bold = True
        p_h.font.color.rgb = ACCENT_GREEN

        p_b = dtf.add_paragraph()
        p_b.text = d_desc
        p_b.font.name = "Arial"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = TEXT_MUTED
        p_b.space_before = Pt(2)

    # ==========================================
    # SLIDE 6: COMPLETE TECH STACK
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Technologies & Libraries", "Complete Modern Full-Stack Architecture",
               "Built with high-performance, asynchronous, and cloud-native open source technologies.")

    tech_categories = [
        ("Frontend Application", ACCENT_BLUE, [
            ("React 19 & TypeScript", "Component SPA architecture with strict typing"),
            ("Vite 8.3", "Ultra-fast bundling and development server"),
            ("Tailwind CSS 3.4", "Modern responsive utility styling"),
            ("TanStack React Query", "Async caching, prefetching, and state sync"),
            ("Recharts", "Interactive radar charts & analytics visualizations"),
            ("Lucide React & Zod", "Streamlined iconography and runtime validation")
        ]),
        ("Backend & Ingestion", ACCENT_CYAN, [
            ("FastAPI 0.115", "High-throughput asynchronous ASGI Python framework"),
            ("Uvicorn 0.32", "High-performance production ASGI server"),
            ("Pydantic v2", "Strict request/response schema data validation"),
            ("PyMuPDF & python-docx", "Deep text & metadata extraction from resumes"),
            ("HTTPX", "Async HTTP client for parallel job API ingestion"),
            ("PyJWT & Bcrypt", "Secure authentication tokens & hashed credentials")
        ]),
        ("Database & Storage", ACCENT_GREEN, [
            ("Supabase PostgreSQL 15", "Cloud-native relational data persistence"),
            ("pgvector (768-dim)", "Vector extension for similarity embeddings"),
            ("SQLite Fallback", "Zero-cost local database file (zyncrole.db)"),
            ("SQLAlchemy 2.0 (Async)", "Async ORM with asyncpg and aiosqlite"),
            ("Multi-Tenant Isolation", "User-scoped queries and cascading relations"),
            ("Local Disk / Storage", "Dedicated /uploads repository for resume files")
        ]),
        ("AI, ML & Deployment", ACCENT_AMBER, [
            ("Google Gemini Embeddings", "gemini-embedding-2 for 768-dim vector embeddings"),
            ("Gemini Generative AI", "gemini-3.8-flash for synthesis & deep intelligence"),
            ("RapidFuzz 3.10", "C-optimized token matching for job deduplication"),
            ("Scikit-Learn & NumPy", "TF-IDF fallback & deterministic vector similarity"),
            ("Docker & Compose", "Containerized local and production orchestration"),
            ("Render & Vercel", "100% free-tier cloud deployment configuration")
        ])
    ]

    card_w = Inches(2.83)
    card_gap = Inches(0.12)
    start_x = Inches(0.8)

    for i, (cat_title, color, items) in enumerate(tech_categories):
        x = start_x + i * (card_w + card_gap)
        card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), card_w, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = color
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.2)

        p_t = tf.paragraphs[0]
        p_t.text = cat_title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = color

        for heading, desc in items:
            p_h = tf.add_paragraph()
            p_h.text = heading
            p_h.font.name = "Arial"
            p_h.font.size = Pt(11)
            p_h.font.bold = True
            p_h.font.color.rgb = TEXT_WHITE
            p_h.space_before = Pt(8)

            p_d = tf.add_paragraph()
            p_d.text = desc
            p_d.font.name = "Arial"
            p_d.font.size = Pt(9.5)
            p_d.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 7: CORE FEATURES
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Feature Showcase", "Core Platform Capabilities & User Experience",
               "Comprehensive suite of intelligent tools designed for modern tech job seekers.")

    features = [
        ("1-Click Instant Demo Evaluation",
         "Pre-configured Alex Chen (AI/ML Engineer) profile for rapid jury & hackathon review without manual form filling.",
         ACCENT_CYAN),
        ("Personalized Career Feed",
         "Real-time opportunities filtered by compatibility, freshness, domain, work mode (Remote/Hybrid), and salary.",
         ACCENT_BLUE),
        ("Transparent 'Why This Match?'",
         "Actionable explanation breakdown revealing top matched skills, missing criteria, and how to improve compatibility.",
         ACCENT_GREEN),
        ("7-Dimension ATS Diagnostic",
         "Comprehensive evaluation of resume structure, keywords, achievements, and formatting + 1-click OpenResume CTA.",
         ACCENT_AMBER),
        ("Market Skill Gap Intelligence",
         "Aggregated missing skill frequencies ranked by High, Medium, and Low impact to target user upskilling.",
         RGBColor(168, 85, 247)),
        ("Kanban Application Pipeline",
         "Integrated recruitment tracker across Applied, Assessment, Interview, Offer, and Rejected with notes and dates.",
         RGBColor(244, 63, 94))
    ]

    for i, (f_title, f_desc, color) in enumerate(features):
        col = i % 3
        row = i // 3
        x = Inches(0.8 + col * 3.95)
        y = Inches(2.0 + row * 2.5)

        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.8), Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.25)

        p_t = tf.paragraphs[0]
        p_t.text = f_title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = color

        p_d = tf.add_paragraph()
        p_d.text = f_desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(8)

    # ==========================================
    # SLIDE 8: SUMMARY & COMPETITIVE ADVANTAGE
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Value Proposition & Impact", "Why ZyncRole AI Stands Out",
               "Designed for ethical compliance, auditability, candidate privacy, and zero operational cost.")

    advantages = [
        ("Deterministic vs Hallucinated AI",
         "Unlike black-box LLMs that invent qualification claims, ZyncRole uses an auditable mathematical equation backed by vector math and canonical skill taxonomies.",
         ACCENT_BLUE),
        ("100% Free-Tier Cloud Operations",
         "Architected with Supabase (Free Tier PostgreSQL + pgvector), Render / Fly.io backend, and Vercel frontend for $0 operational expenditure.",
         ACCENT_GREEN),
        ("Complete Data Sovereignty & Privacy",
         "Self-service 1-click JSON export and complete right-to-erasure compliance. Autonomous platform with zero administrative backdoor interfaces.",
         ACCENT_CYAN),
        ("Ethical Ingestion Standards",
         "100% compliant with API terms and public ATS feeds. Zero unauthorized web scraping, respecting platform terms and robots.txt.",
         ACCENT_AMBER)
    ]

    for i, (a_title, a_desc, color) in enumerate(advantages):
        row = i // 2
        col = i % 2
        x = Inches(0.8 + col * 5.95)
        y = Inches(2.0 + row * 2.4)

        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.75), Inches(2.15))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)

        p_t = tf.paragraphs[0]
        p_t.text = a_title
        p_t.font.name = "Arial"
        p_t.font.size = Pt(15)
        p_t.font.bold = True
        p_t.font.color.rgb = color

        p_d = tf.add_paragraph()
        p_d.text = a_desc
        p_d.font.name = "Arial"
        p_d.font.size = Pt(11.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(6)

    # Save presentation
    prs.save(output_path)
    print(f"Presentation generated successfully at: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    create_presentation()

