from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import Column, ForeignKey, update
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select


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
    requirements: list["Requirement"]


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


class Requirement(SQLModel, table=True):
    id: int | None = Field(default=None, index=True, primary_key=True)
    name: str
    description: str
    related_app_id: int = Field(sa_column=Column(ForeignKey(AppDefinition.id)))


class RequirementDetailSchema(SQLModel):
    id: int
    name: str
    description: str
    related_app_id: int


class RequirementCreateSchema(SQLModel):
    name: str
    description: str
    related_app_id: int


class RequirementUpdateSchema(SQLModel):
    name: str | None = None
    description: str | None = None
    related_app_id: int | None = None


sqlite_file_name = "api/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get(
    "/app-definitions/",
    tags=["AppDefinition"],
    response_model=list[AppDefinitionDashboardSchema],
)
def get_all_apps(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    apps = session.exec(select(AppDefinition).offset(offset).limit(limit)).all()
    return apps


@app.get(
    "/app-definitions/{app_id}/",
    tags=["AppDefinition"],
    response_model=AppDefinitionDetailSchema,
)
def get_app_definition_by_id(
    app_id: int,
    session: SessionDep,
):
    app_def = session.exec(
        select(AppDefinition).where(AppDefinition.id == app_id)
    ).first()
    if not app_def:
        raise HTTPException(
            status_code=404, detail=f"App Definition with id {app_id} not found."
        )
    return app_def


@app.post(
    "/app-definitions/",
    tags=["AppDefinition"],
    response_model=AppDefinitionDetailSchema,
)
def create_app_definition(app_def: AppDefinitionCreateSchema, session: SessionDep):
    db_app_dev = AppDefinition.model_validate(app_def)
    session.add(db_app_dev)
    session.commit()
    session.refresh(db_app_dev)
    return db_app_dev


@app.put(
    "/app-definitions/{app_def_id}/",
    tags=["AppDefinition"],
    response_model=AppDefinitionDetailSchema,
)
def update_app_definition(
    app_def_id: int, app_def: AppDefinitionUpdateSchema, session: SessionDep
):
    existing_app_def = session.exec(
        select(AppDefinition).where(AppDefinition.id == app_def_id)
    ).first()
    if existing_app_def:
        update_stmt = (
            update(AppDefinition)
            .where(AppDefinition.id == app_def_id)
            .values(**app_def.model_dump(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        session.exec(update_stmt)
        session.commit()
        session.refresh(existing_app_def)
        return existing_app_def
    else:
        raise HTTPException(
            status_code=404, detail=f"App Definition with id {app_def_id} not found."
        )


@app.delete("/app-definition/{app_def_id}/", tags=["AppDefinition"])
def delete_app_definition(app_def_id: int, session: SessionDep):
    existing_app_def = session.exec(
        select(AppDefinition).where(AppDefinition.id == app_def_id)
    ).first()
    if existing_app_def:
        session.delete(existing_app_def)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"App Definition with id {app_def_id} not found."
        )


@app.get(
    "/requirements/{req_id}/",
    tags=["Requirement"],
    response_model=RequirementDetailSchema,
)
def get_requirement_by_id(req_id: int, session: SessionDep):
    req = session.exec(select(Requirement).where(Requirement.id == req_id)).first()
    if not req:
        raise HTTPException(
            status_code=404, detail=f"Requirement with id {req_id} not found."
        )
    return req


@app.post(
    "/requirements/",
    tags=["Requirement"],
    response_model=RequirementDetailSchema,
)
def create_requirement(
    requirement: RequirementCreateSchema,
    session: SessionDep,
):
    db_req = Requirement.model_validate(requirement)
    session.add(db_req)
    session.commit()
    session.refresh(db_req)
    return db_req


@app.put(
    "/requirements/{req_id}/",
    tags=["Requirement"],
    response_model=RequirementDetailSchema,
)
def update_requirement(
    req_id: int,
    requirement: RequirementUpdateSchema,
    session: SessionDep,
):
    existing_requirement = session.exec(
        select(Requirement).where(Requirement.id == req_id)
    ).first()
    if existing_requirement:
        update_stmt = (
            update(Requirement)
            .where(Requirement.id == req_id)
            .values(**requirement.model_dump(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        session.exec(update_stmt)
        session.commit()
        session.refresh(existing_requirement)
        return existing_requirement
    else:
        raise HTTPException(
            status_code=404, detail=f"Requirement with id {req_id} not found."
        )


@app.delete("/requirements/{req_id}/", tags=["Requirement"])
def delete_requirement(req_id: int, session: SessionDep):
    existing_requirement = session.exec(
        select(Requirement).where(Requirement.id == req_id)
    ).first()
    if existing_requirement:
        session.delete(existing_requirement)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"Requirement with id {req_id} not found."
        )
