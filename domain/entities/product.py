import datetime
import decimal
import uuid
from typing import Optional

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from ..abstractions.base import Base
from . import OrderProducts

table_registry = registry()


@table_registry.mapped_as_dataclass
class Products(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text('gen_random_uuid()')
    )
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    unit_price: Mapped[decimal.Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    stock: Mapped[Optional[int]] = mapped_column(
        Integer, server_default=text('0')
    )

    order_products: Mapped[list['OrderProducts']] = relationship(
        'OrderProducts', back_populates='product'
    )

    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('stock >= 0', name='chk_products_stock'),
        PrimaryKeyConstraint('id', name='pk_products'),
        {'schema': 'catalog'},
    )
