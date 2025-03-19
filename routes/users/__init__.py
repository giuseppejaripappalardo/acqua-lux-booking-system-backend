from fastapi import APIRouter
from .user_add import router as user_add_router
from .users_list import router as users_list_router

router = APIRouter()
router.include_router(user_add_router)
router.include_router(users_list_router)