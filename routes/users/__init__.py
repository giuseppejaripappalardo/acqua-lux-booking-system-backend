from fastapi import APIRouter
from .user_routes import router as user_routes

router = APIRouter()
router.include_router(user_routes)