"""
app/main.py

Application entry point.
Configures the FastAPI instance, mounts all routers, and handles
startup events (table creation) and global exception handlers.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.database import engine, Base
from app.routes import transactions, analytics, users

# ---------------------------------------------------------------------------
# Create all tables on startup (idempotent — skips existing tables)
# In production you'd use Alembic migrations instead.
# ---------------------------------------------------------------------------
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# FastAPI application instance
# ---------------------------------------------------------------------------
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this for production deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Global exception handlers
# ---------------------------------------------------------------------------
@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Translate DB-level constraint violations into a clean 409 response."""
    return JSONResponse(
        status_code=409,
        content={"detail": "A resource with the provided data already exists."},
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all for unexpected errors — never expose raw stack traces."""
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred. Please try again later."},
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(analytics.router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"], summary="Service health check")
def health_check() -> dict:
    """Lightweight endpoint for uptime monitoring and load balancer probes."""
    return {"status": "ok", "version": settings.APP_VERSION}


@app.get("/", tags=["Health"], include_in_schema=False)
def root() -> dict:
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "redoc": "/redoc",
    }
