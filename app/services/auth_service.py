from sqlalchemy.orm import Session
from app.models.user_model import User
from app.core.security import verify_password


def authentic_user(email: str, password: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        return False
    
    if not verify_password(password, user.hashed_password):
        return False
    
    return user
