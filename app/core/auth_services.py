from typing import Optional
from sqlalchemy.orm import Session
from ..db.models import User
import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    db_user = db.query(User).filter_by(username=username).first()
    if db_user and verify_password(password, db_user.password):
        return db_user
    return None
