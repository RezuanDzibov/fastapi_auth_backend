from pydantic import BaseModel, UUID4


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: UUID4


class Message(BaseModel):
    message: str