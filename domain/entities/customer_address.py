from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    Table,
    Uuid,
)

from ..abstractions.base import Base

t_customer_addresses = Table(
    'customer_addresses',
    Base.metadata,
    Column('customer_id', Uuid, primary_key=True),
    Column('address_id', Uuid, primary_key=True),
    ForeignKeyConstraint(
        ['address_id'],
        ['store.addresses.id'],
        name='fk_customer_addresses_address',
    ),
    ForeignKeyConstraint(
        ['customer_id'],
        ['store.customers.id'],
        ondelete='CASCADE',
        name='fk_customer_addresses_customer',
    ),
    PrimaryKeyConstraint(
        'customer_id', 'address_id', name='pk_customer_addresses'
    ),
    schema='store',
)
