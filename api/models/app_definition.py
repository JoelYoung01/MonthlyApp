from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from api.models.requirement import Requirement, RequirementDetailSchema
from api.models.app_submission import AppSubmission, AppSubmissionDetailSchema


class AppDefinition(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    name: str
    start_date: datetime
    due_date: datetime
    description: str

    requirements: list["Requirement"] = Relationship()
    submissions: list["AppSubmission"] = Relationship()


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
    submissions: list[AppSubmissionDetailSchema]


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
