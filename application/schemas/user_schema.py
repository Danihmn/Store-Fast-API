from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    hashed_password: str
    active: Optional[bool] = True
    role: str


class UserOut(BaseModel):
    name: str
    email: EmailStr
    active: Optional[bool] = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
