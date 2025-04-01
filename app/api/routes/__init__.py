from fastapi import APIRouter

from .organization import router as organization_router
from .auth import router as auth_router
from .admin import router as admin_router

api_router = APIRouter()

api_router.include_router(organization_router, prefix="/org", tags=["organization"])
# api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
