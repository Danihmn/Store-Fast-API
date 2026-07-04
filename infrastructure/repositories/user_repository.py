import datetime
import uuid

from sqlalchemy import select

from domain.entities.user import Users
from infrastructure.security.password import hash_password


class UserRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_all_users(self, skip: int = 0, take: int = 100):
        """Get all users from the database."""
        async with self.session_factory() as session:
            result = await session.scalars(
                select(Users).offset(skip).limit(take)
            )
            return result.all()

    async def get_user_by_id(self, user_id: uuid.UUID):
        """Get a user by ID from the database."""
        async with self.session_factory() as session:
            return await session.get(Users, user_id)

    async def get_user_by_email(self, email: str):
        """Get a user by email from the database."""
        async with self.session_factory() as session:
            result = await session.scalars(
                select(Users).where(Users.email == email)
            )
            return result.first()

    async def create_user(self, user: Users):
        """Create a new user in the database."""
        async with self.session_factory() as session:
            session.add(user)
            await session.flush()
            await session.refresh(user)
        return user

    async def update_user(self, user_id: uuid.UUID, new_user: Users):
        """Update an existing user"""
        async with self.session_factory() as session:
            user = await session.get(Users, user_id)

            if not user:
                return None

            user.name = new_user.name
            user.email = new_user.email
            user.hashed_password = hash_password(new_user.hashed_password)
            user.role = new_user.role
            user.active = new_user.active
            user.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)

            await session.flush()
            await session.refresh(user)

        return user

    async def delete_user(self, user_id: uuid.UUID):
        """Delete a user from the database."""
        async with self.session_factory() as session:
            user = await session.get(Users, user_id)

            if not user:
                return None

            await session.delete(user)
            await session.flush()

        return True
