import datetime
import uuid
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    PrimaryKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..abstractions.base import Base


class Users(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, server_default=text('gen_random_uuid()')
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    active: Mapped[bool] = mapped_column(
        nullable=False, server_default=text('TRUE')
    )
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )

    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_users'),
        UniqueConstraint('email', name='uq_users_email'),
        CheckConstraint(
            "role IN ('admin', 'seller', 'purchaser', 'stock_clerk')",
            name='chk_users_role',
        ),
        {'schema': 'store'},
    )
