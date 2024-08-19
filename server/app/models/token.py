from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: Optional[int] = 0
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
