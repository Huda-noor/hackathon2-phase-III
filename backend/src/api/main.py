from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat, auth
from ..core.config import settings
from ..middleware.auth import jwt_auth_middleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Add authentication middleware
    app.middleware("http")(jwt_auth_middleware)

    # Set up CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(chat.router, prefix=settings.API_V1_STR)
    app.include_router(auth.router, prefix=settings.API_V1_STR)

    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}

    return app


app = create_app()