from typing import Optional

from pydantic import BaseModel, EmailStr


class Command(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
