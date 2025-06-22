from sqlmodel import select
from src.auth.models import User
from src.auth.schemas import UserSignupRequest
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import generate_password_hash, verify_password


class UserService:
    async def get_user_by_email(self, email, session):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        if not result:
            return None
        user = result.first()
        return user

    async def user_exists(self, email, session):
        user = await self.get_user_by_email(email, session)
        if user is None:
            return False
        return True

    async def create_user(self, data: UserSignupRequest, session: AsyncSession):
        user_exists = await self.user_exists(data.email, session)
        if user_exists:
            return

        user_data_dict = data.model_dump()

        new_user = User(**user_data_dict)
        new_user.password = generate_password_hash(new_user.password)
        new_user.role = "user"
        session.add(new_user)
        await session.commit()
        return new_user

    async def update_user(self, user: User, user_data: dict, session: AsyncSession):
        for key, value in user_data.items():
            setattr(user, key, value)

        await session.commit()
        return user
