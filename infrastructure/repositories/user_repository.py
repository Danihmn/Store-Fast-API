import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.user import Users
from infrastructure.security.password import hash_password


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_users(self, skip: int = 0, take: int = 100):
        """Get all users from the database."""
        return self.session.scalars(
            select(Users).offset(skip).limit(take)
        ).all()

    def get_user_by_id(self, user_id: uuid.UUID):
        """Get a user by ID from the database."""
        return self.session.get(Users, user_id)

    def get_user_by_email(self, email: str):
        """Get a user by email from the database."""
        return self.session.scalars(
            select(Users).where(Users.email == email)
        ).first()

    def create_user(self, user: Users):
        """Create a new user in the database."""
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user

    def update_user(self, user_id: uuid.UUID, new_user: Users):
        """Update an existing user"""
        user = self.session.get(Users, user_id)

        if not user:
            return None

        user.name = new_user.name
        user.email = new_user.email
        user.hashed_password = hash_password(new_user.hashed_password)
        user.role = new_user.role
        user.active = new_user.active
        user.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)

        self.session.flush()
        self.session.refresh(user)
        return user

    def delete_user(self, user_id: uuid.UUID):
        """Delete a user from the database."""
        user = self.session.get(Users, user_id)

        if not user:
            return None

        self.session.delete(user)
        self.session.flush()
