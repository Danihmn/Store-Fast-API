import datetime
import uuid
from typing import Optional

from sqlalchemy import (
    DateTime,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..abstractions.base import Base


class Customers(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text('gen_random_uuid()')
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    phone: Mapped[Optional[str]] = mapped_column(String(20))

    __tablename__ = 'customers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_customers'),
        UniqueConstraint('email', name='uq_customers_email'),
        UniqueConstraint('phone', name='uq_customers_phone'),
        {'schema': 'store'},
    )
