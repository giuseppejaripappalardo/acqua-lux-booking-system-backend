from fastapi import APIRouter
from .auth_routes import router as auth_routes
router = APIRouter(prefix="/auth", tags=["auth"])
router.include_router(auth_routes)