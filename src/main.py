"""FastAPI application entrypoint."""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.config import settings
from backend.database import init_db
from backend.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events - startup and shutdown."""
    # Startup: Initialize database
    init_db()
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="A simple dictionary API for storing and retrieving word definitions",
    lifespan=lifespan
)

# Include routers
app.include_router(router)


@app.get("/", tags=["health"])
def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }


@app.get("/health", tags=["health"])
def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected"
    }