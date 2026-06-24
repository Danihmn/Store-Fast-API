import uuid

from sqlalchemy import (
    CheckConstraint,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    Uuid,
)
from sqlalchemy.orm import Mapped, mapped_column

from ..abstractions.base import Base


class OrderProducts(Base):
    order_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    product_id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    __tablename__ = 'order_products'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='chk_order_products_quantity'),
        ForeignKeyConstraint(
            ['order_id'],
            ['store.orders.id'],
            ondelete='CASCADE',
            name='fk_order_products_order',
        ),
        ForeignKeyConstraint(
            ['product_id'],
            ['catalog.products.id'],
            name='fk_order_products_product',
        ),
        PrimaryKeyConstraint(
            'order_id', 'product_id', name='pk_order_products'
        ),
        {'schema': 'store'},
    )
