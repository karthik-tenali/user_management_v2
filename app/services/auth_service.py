from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import verify_password
from app.services.user_service import UserService
from sqlalchemy import select


def authentic_user(email: str, password: str, db: Session):
    # user = db.query(User).filter(User.email == email).first()
    result = db.execute(select(User).where(User.email == email))
    user = result.scalars().one_or_none()
    
    if user is None:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user
