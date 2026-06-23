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
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from ..abstractions.base import Base
from . import Addresses, Customers, OrderProducts

table_registry = registry()


@table_registry.mapped_as_dataclass
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
        String(20), server_default=text("'pendente'::character varying")
    )

    address: Mapped['Addresses'] = relationship(
        'Addresses', back_populates='orders'
    )
    customer: Mapped['Customers'] = relationship(
        'Customers', back_populates='orders'
    )
    order_products: Mapped[list['OrderProducts']] = relationship(
        'OrderProducts', back_populates='order'
    )

    __tablename__ = 'orders'
    __table_args__ = (
        CheckConstraint(
            "status::text = ANY (ARRAY['pendente'::character varying, 'pago'::character varying, 'enviado'::character varying, 'entregue'::character varying, 'cancelado'::character varying]::text[])",  # noqa: E501
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
