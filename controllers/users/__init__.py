from fastapi import APIRouter
from .user_controller import router as user_routes

router = APIRouter(prefix="/user", tags=["user"])
router.include_router(user_routes)