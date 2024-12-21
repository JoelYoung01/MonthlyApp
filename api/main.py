from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, update
from sqlmodel import Field, Session, SQLModel, create_engine, select


class AppDefinition(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    start_date: datetime
    due_date: datetime
    description: str


class Requirement(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str
    related_app_id: int = Field(sa_column=Column(ForeignKey("app_definition.id")))


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


@app.get("/requirements/", tags=["Requirements"])
def get_all_requirements(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
) -> list[Requirement]:
    reqs = session.exec(select(Requirement).offset(offset).limit(limit)).all()
    return reqs


@app.get("/requirements/{req_id}/", tags=["Requirements"])
def get_requirement_by_id(
    req_id: int,
    session: SessionDep,
) -> Requirement:
    req = session.exec(select(Requirement).where(Requirement.id == req_id))
    if not req:
        raise HTTPException(
            status_code=404, detail=f"Requirement with id {req_id} not found."
        )
    return req


@app.post("/requirements/", tags=["Requirements"])
def create_requirement(requirement: Requirement, session: SessionDep) -> Requirement:
    session.add(requirement)
    session.commit()
    session.refresh(requirement)
    return requirement


@app.put("/requirements/{req_id}/", tags=["Requirements"])
def update_requirement(
    req_id: int, requirement: Requirement, session: SessionDep
) -> Requirement:
    existing_requirement = session.exec(
        select(Requirement).where(Requirement.id == req_id)
    ).first()
    if existing_requirement:
        update_stmt = (
            update(Requirement)
            .where(Requirement.id == req_id)
            .values(**requirement.dict())
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


@app.delete("/requirements/{req_id}/", tags=["Requirements"])
def delete_requirement(req_id: int, session: SessionDep) -> None:
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
