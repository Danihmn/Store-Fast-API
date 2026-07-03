from pydantic import BaseModel


class Command(BaseModel):
    skip: int = 0
    take: int = 100
