import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import api_router
from app.middleware.auth import (
    JWTAuthMiddleware
)
from app.admin import init_admin

import settings


async def startup_event():
    print("Starting application...")


async def shutdown_event():
    print("Shutting down application...")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    try:
        await startup_event()
        yield
    finally:
        await shutdown_event()


app = FastAPI(
    lifespan=app_lifespan,
    docs_url="/tenantflow/docs",
    redoc_url="/tenantflow/redoc",
    openapi_url="/tenantflow/openapi.json",
)

init_admin(app)
app.include_router(api_router, prefix="/api")

app.add_middleware(JWTAuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
add_pagination(app)

Instrumentator().instrument(app).expose(app, include_in_schema=False, should_gzip=True)

if __name__ == "__main__":
    try:
        import uvicorn

        uvicorn.run(app, host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
