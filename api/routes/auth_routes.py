from fastapi import APIRouter, HTTPException, status

from api.core.authentication import verify_session_token
from api.deps import SessionDep
from api.models.authentication import TokenResponse

router = APIRouter(prefix="/auth", tags=["/Auth"])


@router.post(
    "/login-google",
    tags=["Auth"],
)
def login_with_google(body, session: SessionDep):
    pass


@router.get("/verify-session/", tags=["Auth"], response_model=TokenResponse)
def verify_session(access_token: str, session: SessionDep):
    token = verify_session_token(access_token, session)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token
