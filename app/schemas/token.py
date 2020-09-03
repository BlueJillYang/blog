from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    token: str
    expired: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
