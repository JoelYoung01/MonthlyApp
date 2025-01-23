from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from sqlalchemy import update
from sqlmodel import select

from api.deps import SessionDep
from api.models.app_submission import (
    AppSubmission,
    AppSubmissionCreateSchema,
    AppSubmissionDetailSchema,
    AppSubmissionUpdateSchema,
)

router = APIRouter(prefix="/app-submission", tags=["AppSubmission"])


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
    new_def = app_def.model_dump()
    new_def["created_on"] = datetime.now(timezone.utc).isoformat()
    new_def["created_by"] = 1  # TODO: Add User from request

    db_app_def = AppSubmission.model_validate(new_def)

    session.add(db_app_def)
    session.commit()
    session.refresh(db_app_def)
    return db_app_def


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
