import datetime
import uuid
from typing import Optional

from sqlalchemy import (
    CHAR,
    Boolean,
    DateTime,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

from ..abstractions.base import Base
from . import Addresses

table_registry = registry()


@table_registry.mapped_as_dataclass
class Stores(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, server_default=text('gen_random_uuid()')
    )
    legal_name: Mapped[str] = mapped_column(String(200), nullable=False)
    cnpj: Mapped[str] = mapped_column(CHAR(14), nullable=False)
    active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text('true')
    )
    address_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime, server_default=text('now()')
    )
    trade_name: Mapped[Optional[str]] = mapped_column(String(200))

    address: Mapped['Addresses'] = relationship(
        'Addresses', back_populates='stores'
    )

    __tablename__ = 'stores'
    __table_args__ = (
        ForeignKeyConstraint(
            ['address_id'], ['store.addresses.id'], name='fk_stores_address'
        ),
        PrimaryKeyConstraint('id', name='pk_stores'),
        UniqueConstraint('cnpj', name='uq_stores_cnpj'),
        {'schema': 'store'},
    )
