from typing import Annotated
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import update
from sqlmodel import select

from api.deps import SessionDep
from api.models.app_submission import (
    AppSubmission,
    AppSubmissionCreateSchema,
    AppSubmissionDashboardSchema,
    AppSubmissionDetailSchema,
    AppSubmissionUpdateSchema,
)

router = APIRouter(prefix="/app-submission", tags=["AppSubmission"])


@router.get(
    "/",
    tags=["AppSubmission"],
    response_model=list[AppSubmissionDashboardSchema],
)
def get_all_app_submissions(
    session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100
):
    apps = session.exec(select(AppSubmission).offset(offset).limit(limit)).all()
    return apps


@router.get(
    "/{app_id}/",
    tags=["AppSubmission"],
    response_model=AppSubmissionDetailSchema,
)
def get_app_submission_by_id(
    app_id: int,
    session: SessionDep,
):
    app_def = session.exec(
        select(AppSubmission).where(AppSubmission.id == app_id)
    ).first()
    if not app_def:
        raise HTTPException(
            status_code=404, detail=f"App Submission with id {app_id} not found."
        )
    return app_def


@router.post(
    "/",
    tags=["AppSubmission"],
    response_model=AppSubmissionDetailSchema,
)
def create_app_submission(app_def: AppSubmissionCreateSchema, session: SessionDep):
    db_app_dev = AppSubmission.model_validate(app_def)
    session.add(db_app_dev)
    session.commit()
    session.refresh(db_app_dev)
    return db_app_dev


@router.put(
    "/{app_def_id}/",
    tags=["AppSubmission"],
    response_model=AppSubmissionDetailSchema,
)
def update_app_submission(
    app_def_id: int, app_def: AppSubmissionUpdateSchema, session: SessionDep
):
    existing_app_def = session.exec(
        select(AppSubmission).where(AppSubmission.id == app_def_id)
    ).first()
    if existing_app_def:
        update_stmt = (
            update(AppSubmission)
            .where(AppSubmission.id == app_def_id)
            .values(**app_def.model_dump(exclude_unset=True))
            .execution_options(synchronize_session="fetch")
        )
        session.exec(update_stmt)
        session.commit()
        session.refresh(existing_app_def)
        return existing_app_def
    else:
        raise HTTPException(
            status_code=404, detail=f"App Submission with id {app_def_id} not found."
        )


@router.delete("/{app_def_id}/", tags=["AppSubmission"])
def delete_app_submission(app_def_id: int, session: SessionDep):
    existing_app_def = session.exec(
        select(AppSubmission).where(AppSubmission.id == app_def_id)
    ).first()
    if existing_app_def:
        session.delete(existing_app_def)
        session.commit()
    else:
        raise HTTPException(
            status_code=404, detail=f"App Submission with id {app_def_id} not found."
        )
