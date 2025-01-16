from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import update
from sqlmodel import select

from api.deps import SessionDep
from api.models.app_definition import (
    AppDefinition,
    AppDefinitionCreateSchema,
    AppDefinitionDashboardSchema,
    AppDefinitionDetailSchema,
    AppDefinitionUpdateSchema,
)

router = APIRouter(prefix="/app-definition", tags=["AppDefinition"])


@router.get(
    "/",
    tags=["AppDefinition"],
    response_model=list[AppDefinitionDashboardSchema],
)
def get_all_apps(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    apps = session.exec(select(AppDefinition).offset(offset).limit(limit)).all()
    return apps


@router.get(
    "/{app_id}/",
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


@router.post(
    "/",
    tags=["AppDefinition"],
    response_model=AppDefinitionDetailSchema,
)
def create_app_definition(app_def: AppDefinitionCreateSchema, session: SessionDep):
    db_app_dev = AppDefinition.model_validate(app_def)
    session.add(db_app_dev)
    session.commit()
    session.refresh(db_app_dev)
    return db_app_dev


@router.put(
    "/{app_def_id}/",
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


@router.delete("/{app_def_id}/", tags=["AppDefinition"])
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
