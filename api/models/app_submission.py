from datetime import datetime

from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel

from api.models.requirement import RequirementDetailSchema


class AppSubmission(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    status: int | None
    created_by: int | None
    created_on: int | None
    submitted_by: int | None
    submitted_on: int | None

    app_definition_id: int = Field(sa_column=Column(ForeignKey("appdefinition.id")))


class AppSubmissionDashboardSchema(SQLModel):
    id: int
    name: str
    start_date: datetime
    due_date: datetime
    description: str


class AppSubmissionDetailSchema(SQLModel):
    id: int
    name: str
    start_date: datetime
    due_date: datetime
    description: str
    requirements: list[RequirementDetailSchema]


class AppSubmissionCreateSchema(SQLModel):
    name: str
    start_date: datetime
    due_date: datetime
    description: str


class AppSubmissionUpdateSchema(SQLModel):
    name: str | None = None
    start_date: datetime | None = None
    due_date: datetime | None = None
    description: str | None = None
