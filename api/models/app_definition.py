from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from api.models.requirement import Requirement, RequirementDetailSchema


class AppDefinition(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    name: str
    start_date: datetime
    due_date: datetime
    description: str

    requirements: list["Requirement"] = Relationship()


class AppDefinitionDashboardSchema(SQLModel):
    id: int
    name: str
    start_date: datetime
    due_date: datetime
    description: str


class AppDefinitionDetailSchema(SQLModel):
    id: int
    name: str
    start_date: datetime
    due_date: datetime
    description: str
    requirements: list[RequirementDetailSchema]


class AppDefinitionCreateSchema(SQLModel):
    name: str
    start_date: datetime
    due_date: datetime
    description: str


class AppDefinitionUpdateSchema(SQLModel):
    name: str | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None
    description: str | None = None
