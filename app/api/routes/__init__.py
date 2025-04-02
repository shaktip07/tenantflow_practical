from fastapi import APIRouter

from .organization import router as organization_router
from .admin import router as admin_router

api_router = APIRouter()

api_router.include_router(organization_router, prefix="/org", tags=["organization"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
