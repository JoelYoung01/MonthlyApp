from fastapi import APIRouter

from api.deps import SessionDep

router = APIRouter(prefix="/auth", tags=["/Auth"])


@router.post(
    "/google-auth-receiver",
    tags=["AppSubmission"],
)
def google_login(credential, session: SessionDep):
    pass
