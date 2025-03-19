from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True