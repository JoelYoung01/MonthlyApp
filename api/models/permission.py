from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, Relationship, SQLModel


class Permission(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    name: str
