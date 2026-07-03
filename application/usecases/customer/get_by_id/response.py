import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class Response(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    phone: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
