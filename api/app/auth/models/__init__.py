from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class UserDetails(BaseModel):
    id:UUID
    name: str
    email: str


class Auth(BaseModel):
    user_id: Optional[str] = Field(default=None)
    token_type: str = "bearer"
    access_token: Optional[str] = Field(default="")
    refresh_token: Optional[str] = Field(default="")
