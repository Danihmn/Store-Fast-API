from pydantic import BaseModel, EmailStr


class Command(BaseModel):
    email: EmailStr
    password: str
