from enum import Enum
from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel

from api.models.user import User


class TokenType(Enum):
    Access = 10


class Token(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    access_token: str
    token_type: TokenType
    user_id: int = Field(sa_column=Column(ForeignKey("user.id")))


class TokenResponse(SQLModel):
    access_token: str
    user: User
