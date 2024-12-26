from fastapi import APIRouter, HTTPException
from sqlalchemy import update
from sqlmodel import select

from api.deps import SessionDep
from api.models.Requirement import (
    Requirement,
    RequirementCreateSchema,
    RequirementDetailSchema,
    RequirementUpdateSchema,
)

router = APIRouter(prefix="/requirement", tags=["Requirement"])


@router.get(
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


@router.post(
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


@router.put(
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


@router.delete("/requirements/{req_id}/", tags=["Requirement"])
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
