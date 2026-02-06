"""FastAPI application initialization."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

# Initialize FastAPI app
app = FastAPI(
    title="AI Chat Backend & Data Models API",
    description="Backend API for task management and chat persistence",
    version="1.0.0",
    openapi_url="/api/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "API is running"}


# Register routers
from src.api import tasks

app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
