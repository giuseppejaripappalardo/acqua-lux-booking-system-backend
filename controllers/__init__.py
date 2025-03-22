from fastapi import APIRouter
from controllers.user_controller import router as users
from controllers.auth_controller import router as auth
from controllers.role_controller import router as roles

router = APIRouter()
router.include_router(users, prefix="/users", tags=["Users"])
router.include_router(auth, prefix="/auth", tags=["Auth"])
router.include_router(roles, prefix="/roles", tags=["Roles"])