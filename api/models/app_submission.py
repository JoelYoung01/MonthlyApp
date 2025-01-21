from sqlalchemy import Column, ForeignKey
from sqlmodel import Field, SQLModel


class AppSubmission(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    status: int = 10
    created_by: int | None
    created_on: int | None
    submitted_by: int | None
    submitted_on: int | None
    link: str | None

    app_definition_id: int = Field(sa_column=Column(ForeignKey("appdefinition.id")))


class AppSubmissionDetailSchema(SQLModel):
    id: int
    status: int
    created_by: int
    created_on: int
    submitted_by: int
    submitted_on: int
    link: str | None


class AppSubmissionCreateSchema(SQLModel):
    created_by: int
    created_on: int
    submitted_by: int
    submitted_on: int
    link: str | None
    app_definition_id: int


class AppSubmissionUpdateSchema(SQLModel):
    status: int | None = None
    created_by: int | None = None
    created_on: int | None = None
    submitted_by: int | None = None
    submitted_on: int | None = None
    link: str | None = None
