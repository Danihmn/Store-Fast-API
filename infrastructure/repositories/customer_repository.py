import datetime
import uuid
from typing import Optional

from sqlalchemy import select

from domain.entities.customer import Customers


class CustomerRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_all_customers(self, skip: int = 0, take: int = 100):
        """Get all customers from the database."""
        async with self.session_factory() as session:
            result = await session.scalars(
                select(Customers).offset(skip).limit(take)
            )

            return result.all()

    async def get_customer_by_id(self, customer_id: uuid.UUID):
        """Get a customer by ID from the database."""
        async with self.session_factory() as session:
            return await session.get(Customers, customer_id)

    async def get_customer_by_email_or_phone(
        self, email: str, phone: Optional[str] = None
    ):
        """Get a customer matching the given email or phone."""
        async with self.session_factory() as session:
            return await session.scalar(
                select(Customers).where(
                    (Customers.email == email) | (Customers.phone == phone)
                )
            )

    async def create_customer(self, customer: Customers):
        """Create a new customer in the database."""
        async with self.session_factory() as session:
            session.add(customer)
            await session.flush()
            await session.refresh(customer)
        return customer

    async def update_customer(
        self, customer_id: uuid.UUID, new_customer: Customers
    ):
        """Update an existing customer"""
        async with self.session_factory() as session:
            customer = await session.get(Customers, customer_id)

            if not customer:
                return None

            customer.name = new_customer.name
            customer.email = new_customer.email
            customer.phone = new_customer.phone
            customer.updated_at = datetime.datetime.now(
                tz=datetime.timezone.utc
            ).replace(tzinfo=None)

            await session.flush()
            await session.refresh(customer)

        return customer

    async def delete_customer(self, customer_id: uuid.UUID):
        """Delete a customer from the database."""
        async with self.session_factory() as session:
            customer = await session.get(Customers, customer_id)

            if not customer:
                return False

            await session.delete(customer)
            await session.flush()

        return True
