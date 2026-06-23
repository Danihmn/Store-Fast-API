import datetime
import uuid
from typing import Optional

from sqlalchemy import CHAR, DateTime, PrimaryKeyConstraint, String, Uuid, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..abstractions.base import Base
from . import Customers, Orders, Stores


class Addresses(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text('gen_random_uuid()')
    )
    street: Mapped[str] = mapped_column(String(200), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(CHAR(2), nullable=False)
    zip_code: Mapped[str] = mapped_column(String(9), nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    customer: Mapped[list['Customers']] = relationship(
        'Customers',
        secondary='store.customer_addresses',
        back_populates='address',
    )
    orders: Mapped[list['Orders']] = relationship(
        'Orders', back_populates='address'
    )
    stores: Mapped[list['Stores']] = relationship(
        'Stores', back_populates='address'
    )

    __tablename__ = 'addresses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='pk_addresses'),
        {'schema': 'store'},
    )
