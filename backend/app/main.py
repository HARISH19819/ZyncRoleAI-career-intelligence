import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.config import settings
from app.core.logging import logger, RequestLoggingMiddleware
from app.db.session import init_db, get_db
from app.models.all_models import Job, JobSource
from app.seed_demo import seed_database

# Import routers
from app.api.routes.auth import router as auth_router
from app.api.routes.profiles import router as profiles_router
from app.api.routes.resumes import router as resumes_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.skill_gaps import router as skill_gaps_router
from app.api.routes.career import router as career_router
from app.api.routes.saved import router as saved_router
from app.api.routes.applications import router as applications_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.internal import router as internal_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME} backend in {settings.ENVIRONMENT} mode...")
    await init_db()
    # Check if database has jobs; if not, automatically seed demo data
    try:
        from app.db.session import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            stmt = select(func.count(Job.id))
            res = await session.execute(stmt)
            count = res.scalar_one()
            if count == 0:
                logger.info("Empty database detected. Seeding initial demo opportunities...")
                await seed_database()
    except Exception as e:
        logger.warning(f"Initial seed check skipped: {e}")

    yield
    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME} backend...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Autonomous AI Career Intelligence and Personalized Job Matching Platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Robust CORS middleware for production and development
raw_origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [str(settings.CORS_ORIGINS)]
if "*" in raw_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"^https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=raw_origins,
        allow_origin_regex=r"^https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Global crash-resilient exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled exception on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred. Please try again later.",
            "error_type": exc.__class__.__name__
        }
    )

# Register API Routers
app.include_router(auth_router)
app.include_router(profiles_router)
app.include_router(resumes_router)
app.include_router(jobs_router)
app.include_router(skill_gaps_router)
app.include_router(career_router)
app.include_router(saved_router)
app.include_router(applications_router)
app.include_router(notifications_router)
app.include_router(dashboard_router)
app.include_router(internal_router)


@app.get("/")
async def root():
    return {
        "product": settings.PROJECT_NAME,
        "tagline": "One Resume. Every Opportunity. One Intelligent Career Feed.",
        "status": "operational",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Health check endpoint checking database, AI config, and storage."""
    db_status = "healthy"
    job_count = 0
    try:
        stmt = select(func.count(Job.id))
        res = await db.execute(stmt)
        job_count = res.scalar_one()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    ai_configured = bool(settings.GEMINI_API_KEY)

    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "database": {
            "status": db_status,
            "total_jobs": job_count
        },
        "ai": {
            "configured": ai_configured,
            "text_model": settings.GEMINI_TEXT_MODEL,
            "embedding_model": settings.GEMINI_EMBEDDING_MODEL,
            "fallback_available": True
        },
        "storage": {
            "status": "operational",
            "type": "local_with_supabase_storage_support"
        }
    }


# SPA Static Files support for single-service / Docker production deployments
dist_candidates = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")),
    os.path.abspath(os.path.join(os.getcwd(), "frontend", "dist")),
    os.path.abspath(os.path.join(os.getcwd(), "dist")),
]
dist_dir = next((d for d in dist_candidates if os.path.exists(os.path.join(d, "index.html"))), None)

if dist_dir:
    logger.info(f"Production static assets discovered at {dist_dir}. Serving SPA fallback.")
    assets_dir = os.path.join(dist_dir, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend_assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        if full_path.startswith("api/") or full_path in ("health", "docs", "redoc", "openapi.json"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="Not Found")
        target_file = os.path.join(dist_dir, full_path)
        if full_path and os.path.isfile(target_file):
            return FileResponse(target_file)
        return FileResponse(os.path.join(dist_dir, "index.html"))
