from fastapi import APIRouter
from .users import router as users
from .auth import router as auth

router = APIRouter(prefix="/api", tags=["api"])
router.include_router(users)
router.include_router(auth)