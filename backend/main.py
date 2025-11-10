from app.api.v1.endpoints import ai_assistant, knowledge_base
from app.core.config import settings
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# --- Middleware Configuration ---


# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    # Add other security headers here as needed
    return response


# CORS Middleware (should be one of the last middleware)
# The `allow_origins` is now controlled by the `BACKEND_CORS_ORIGINS` in `config.py`
# For local development, you might need to set it explicitly in your .env file,
# e.g., BACKEND_CORS_ORIGINS='["http://localhost:3000", "http://localhost:8000"]'
app.add_middleware(
    CORSMiddleware,
    allow_origins=(
        [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
        if settings.BACKEND_CORS_ORIGINS
        else []
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Routers ---
app.include_router(knowledge_base.router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Multi-Model Assistant Backend!"}
