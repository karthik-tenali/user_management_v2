from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models.auth_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.auth_schema import UserRequest
from app.core.security import hash_password, verify_password
from app.core.exceptions import EmailAlreadyExistsError, UsernameALreadyExistsError


class UserService:
    
    async def get_user_by_email(self, email: str, db: AsyncSession):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().one_or_none()
        return user
        
    async def get_user_by_username(self, username: str, db: AsyncSession):
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().one_or_none()
        return user
        
    async def create_new_user(self, form_data: UserRequest, db: AsyncSession):
        
        exist_by_email = await self.get_user_by_email(form_data.email, db)
        exist_by_username = await self.get_user_by_username(form_data.username, db)
        
        if exist_by_email:
            raise EmailAlreadyExistsError()
        
        if exist_by_username:
            raise UsernameALreadyExistsError()
        
        new_user = User(
            first_name = form_data.first_name,
            last_name = form_data.last_name,
            username = form_data.username,
            email = form_data.email,
            hashed_password = hash_password(form_data.password),

        )
        
        db.add(new_user)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise EmailAlreadyExistsError()

        await db.refresh(new_user)
        return new_user
    
    async def authenticate_user(self, email: str, password: str, db: AsyncSession):
        
        user = await self.get_user_by_email(email, db)
        
        if not user:
            return False
        
        if not verify_password(password, user.hashed_password):
            return False
        
        return user
    