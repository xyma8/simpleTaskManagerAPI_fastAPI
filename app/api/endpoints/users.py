from datetime import timedelta

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..schemas.user import UserResponse, UserCreate, UserLogin
from ...core.auth_services import hash_password, authenticate_user
from ...core.security import create_access_token, get_current_user
from ...db.dependencies import get_db
from ...db.models import User

router = APIRouter()

# Эндпойнты пользователя


@router.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login/")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(user.username, user.password, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/me/", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return current_user


@router.get("/protected/")
def protected_endpoint(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}! You are authenticated."}
