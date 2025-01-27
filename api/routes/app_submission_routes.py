from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select

from api.core.authentication import CurrentUserDep, verify_access_token
from api.core.database import SessionDep
from api.models.app_submission import (
    AppSubmission,
    AppSubmissionCreateSchema,
    AppSubmissionDetailSchema,
)

router = APIRouter(
    prefix="/app-submission",
    dependencies=[Depends(verify_access_token)],
    tags=["AppSubmission"],
)


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
def create_app_submission(
    app_def: AppSubmissionCreateSchema,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    new_def = app_def.model_dump()
    new_def["created_on"] = datetime.now(timezone.utc).isoformat()
    new_def["created_by"] = current_user.id

    db_app_def = AppSubmission.model_validate(new_def)

    session.add(db_app_def)
    session.commit()
    session.refresh(db_app_def)
    return db_app_def


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
