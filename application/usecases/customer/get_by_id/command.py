import uuid

from pydantic import BaseModel


class Command(BaseModel):
    customer_id: uuid.UUID
