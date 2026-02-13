from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import EmailAlreadyExistsError, UserNotFoundError
from app.models.user_model import User
from app.core.security import hash_password
from app.schemas.user_schema import UserUpdateRequest


def get_users(db: Session):
    
    return db.query(User).order_by(User.id).all()

def get_user_by_id(db: Session, user_id: int):
    
    user = db.query(User).filter(User.id == user_id).first()
    return user

def get_user_by_mail(db: Session, email: str):
    
    user_by_email = db.query(User).filter(User.email == email).first()
    return user_by_email
    
def create_new_user(db: Session, input):
    new_user = User(
        name = input.name,
        email = input.email,
        hashed_password = hash_password(input.password),
        role = input.role,
        is_active = input.is_active
        
    )
    
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise EmailAlreadyExistsError()

    db.refresh(new_user)
    return new_user


def update_existing_user(db: Session, input: UserUpdateRequest, user_id: int):
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError()

    if input.email and input.email != user.email:
        conflict = get_user_by_mail(db, input.email)
        if conflict:
            raise EmailAlreadyExistsError()

    if input.name is not None:
        user.name = input.name

    if input.email is not None:
        user.email = input.email

    if input.role is not None:
        user.role = input.role

    if input.is_active is not None:
        user.is_active = input.is_active

    db.commit()
    db.refresh(user)
    return user

    
def delete_existing_user(db: Session, user_id: int):
    existing  = get_user_by_id(db, user_id)
    if not existing:
        return False
    db.delete(existing)
    db.commit()
    return True
    