from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.user_model import User
from sqlalchemy.orm import Session
from app.schema.user_schema import UserRequest
from app.core.security import hash_password, verify_password
from app.core.exceptions import EmailAlreadyExistsError, UsernameALreadyExistsError

class UserService:

    def get_user_by_email(self, email: str, db: Session):
        email = email.lower().strip()
        return db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

    def get_user_by_username(self, username: str, db: Session):
        return db.execute(
            select(User).where(User.username == username)
        ).scalar_one_or_none()

    def create_new_user(self, form_data: UserRequest, db: Session):

        email = form_data.email.lower().strip()

        if self.get_user_by_email(email, db):
            raise EmailAlreadyExistsError()

        if self.get_user_by_username(form_data.username, db):
            raise UsernameALreadyExistsError()

        new_user = User(
            first_name=form_data.first_name,
            last_name=form_data.last_name,
            username=form_data.username,
            email=email,
            hashed_password=hash_password(form_data.password),
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user

        except IntegrityError:
            db.rollback()
            raise EmailAlreadyExistsError()

    def authenticate_user(self, email: str, password: str, db: Session):
        email = email.lower().strip()
        user = self.get_user_by_email(email, db)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
