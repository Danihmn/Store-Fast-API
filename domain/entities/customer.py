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
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from ..abstractions.base import Base
from . import Addresses, Orders

table_registry = registry()


@table_registry.mapped_as_dataclass
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

    address: Mapped[list['Addresses']] = relationship(
        'Addresses',
        secondary='store.customer_addresses',
        back_populates='customer',
    )
    orders: Mapped[list['Orders']] = relationship(
        'Orders', back_populates='customer'
    )

    __tablename__ = 'customers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_customers'),
        UniqueConstraint('email', name='uq_customers_email'),
        UniqueConstraint('phone', name='uq_customers_phone'),
        {'schema': 'store'},
    )
