from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel

from api.models.permission import Permission


class User(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    username: str
    email: str
    display_name: str
    admin: bool = False
    disabled: bool = False

    permissions: list["Permission"] = Relationship()
