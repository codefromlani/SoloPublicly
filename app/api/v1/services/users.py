from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any
from pydantic import EmailStr

from ..schemas.users import UserCreate, UserOut
from ..models.users import User
from ...core.security import hash_password, create_access_token, create_email_verification_token
from ...core.email import send_verification_email


def create_user(user: UserCreate, db: Session) -> UserOut:
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with provided credentials already exists"
        )

    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with provided credentials already exists"
        )
    
    hashed_password = hash_password(user.password)
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        is_verified=False,
        role=user.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserOut.model_validate(new_user)

def login_user(form_data: OAuth2PasswordRequestForm, db: Session) -> dict[str, Any]:
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not db_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify your email before logging in"
        )
    
    access_token = create_access_token(data={"sub": db_user.email}, expires_delta=timedelta(minutes=30))

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.model_validate(db_user)
    }

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

async def resend_verification(email: EmailStr, db: Session):
    user = get_user_by_email(email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    token = create_email_verification_token(user.email)
    await send_verification_email(user.email, token)

    return {"message": "Verification email sent successfully"}