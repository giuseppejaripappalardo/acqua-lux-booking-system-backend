from fastapi import APIRouter, Depends

from impl.user_service import UserService
from meta.user_service_meta import UserServiceMeta
from models.user import UserOut, UserCreate

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/create", response_model=UserOut)
def user_add(user: UserCreate, user_service: UserServiceMeta = Depends(UserService)):
    return user_service.create_user(user)


