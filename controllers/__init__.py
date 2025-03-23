from fastapi import APIRouter
from controllers.user_controller import router as users
from controllers.auth_controller import router as auth
from controllers.role_controller import router as roles
from controllers.boat_controller import router as boats
from controllers.booking_controller import router as bookings

router = APIRouter()
router.include_router(users, prefix="/users", tags=["Users"])
router.include_router(auth, prefix="/auth", tags=["Auth"])
router.include_router(roles, prefix="/roles", tags=["Roles"])
router.include_router(boats, prefix="/boats", tags=["Boats"])
router.include_router(bookings, prefix="/bookings", tags=["Bookings"])