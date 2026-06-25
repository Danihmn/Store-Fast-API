import datetime
import decimal
import uuid
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKeyConstraint,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..abstractions.base import Base


class Orders(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text('gen_random_uuid()')
    )
    customer_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    address_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    total: Mapped[decimal.Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    status: Mapped[Optional[str]] = mapped_column(
        String(20), server_default=text("'pending'::character varying")
    )

    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint(
            "status::text = ANY (ARRAY['pending'::character varying, 'paid'::character varying, 'shipped'::character varying, 'delivered'::character varying, 'canceled'::character varying]::text[])",  # noqa: E501
            name='chk_orders_status',
        ),
        ForeignKeyConstraint(
            ['address_id'], ['store.addresses.id'], name='fk_orders_address'
        ),
        ForeignKeyConstraint(
            ['customer_id'], ['store.customers.id'], name='fk_orders_customer'
        ),
        PrimaryKeyConstraint('id', name='pk_orders'),
        {'schema': 'store'},
    )
