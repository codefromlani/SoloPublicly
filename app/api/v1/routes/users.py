from fastapi import APIRouter, Depends, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import EmailStr

from ..models.users import User
from ...db.database import get_db
from ..schemas.users import UserOut, UserCreate, LoginResponse
from ..services.users import create_user, login_user, resend_verification
from ...core.security import create_email_verification_token, verify_email_token, get_current_user
from ...core.email import send_verification_email


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(user, db)

    token = create_email_verification_token(new_user.email)
    await send_verification_email(new_user.email, token)

    return UserOut.model_validate(new_user)


@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user(form_data=form_data, db=db)


@router.get("/me", response_model=UserOut)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)


@router.get("/verify-email")
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    user = verify_email_token(token, db)
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}


@router.post("/resend-verification")
async def resend_verification_email(email: EmailStr, db: Session = Depends(get_db)):
    return await resend_verification(email, db)