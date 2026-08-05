from fastapi import APIRouter, HTTPException, status, Depends

from app.auth.dependencies import get_current_user

from app.auth.schemas import (
    SignupRequest,
    SignupResponse,
    LoginRequest,
    TokenResponse,
)

from app.auth.service import auth_service


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/signup",
    response_model=SignupResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    request: SignupRequest,
) -> SignupResponse:

    try:
        response = auth_service.signup(
            request.email,
            request.password,
        )

        return SignupResponse(
            message="User created successfully",
            email=response.user.email,
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create account.",
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
) -> TokenResponse:

    try:
        response = auth_service.login(
            request.email,
            request.password,
        )

        session = response.session

        return TokenResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )




@router.get("/me")
def get_profile(
    user=Depends(get_current_user),
):
    return {
        "id": user.id,
        "email": user.email,
    }