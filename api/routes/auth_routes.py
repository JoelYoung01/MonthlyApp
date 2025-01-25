from fastapi import APIRouter, HTTPException, status

from api.core.authentication import (
    create_access_token,
    verify_google_token,
    verify_session_token,
)
from api.deps import SessionDep
from api.schemas.authentication import GoogleLoginPayload, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login-google/", response_model=TokenResponse)
def login_with_google(payload: GoogleLoginPayload, session: SessionDep):
    try:
        google_token = verify_google_token(payload.credential)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(google_token, session)
    return access_token


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
