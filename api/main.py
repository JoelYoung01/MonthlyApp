from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import os

from api.core.config import settings
from api.routes import (
    app_definition_routes,
    app_submission_routes,
    auth_routes,
    requirement_routes,
)
from api.core.database import create_db_and_tables


app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")

# Add CORS middleware for development environment
if os.getenv("ENVIRONMENT", "development") == "development":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.FRONTEND_HOST],  # Default Vite dev server port
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


api_router = APIRouter()
api_router.include_router(app_definition_routes.router)
api_router.include_router(requirement_routes.router)
api_router.include_router(app_submission_routes.router)
api_router.include_router(auth_routes.router)


app.include_router(api_router, prefix=settings.API_V1_STR)
