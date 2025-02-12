from pydantic import BaseModel


class UserBase(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    class Config:
        from_attributes = True