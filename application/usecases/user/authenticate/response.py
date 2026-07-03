from pydantic import BaseModel


class Response(BaseModel):
    access_token: str
    token_type: str
