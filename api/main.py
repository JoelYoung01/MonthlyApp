from fastapi import FastAPI, APIRouter

from api.routes import app_definition_routes, requirement_routes
from api.deps import create_db_and_tables


app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


api_router = APIRouter()
api_router.include_router(app_definition_routes.router)
api_router.include_router(requirement_routes.router)


app.include_router(api_router, prefix="/api")
