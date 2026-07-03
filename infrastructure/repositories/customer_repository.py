import datetime
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.customer import Customers


class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_customers(self, skip: int = 0, take: int = 100):
        """Get all customers from the database."""
        return self.session.scalars(
            select(Customers).offset(skip).limit(take)
        ).all()

    def get_customer_by_id(self, customer_id: uuid.UUID):
        """Get a customer by ID from the database."""
        return self.session.get(Customers, customer_id)

    def get_customer_by_email_or_phone(
        self, email: str, phone: Optional[str] = None
    ):
        """Get a customer matching the given email or phone."""
        return self.session.scalar(
            select(Customers).where(
                (Customers.email == email) | (Customers.phone == phone)
            )
        )

    def create_customer(self, customer: Customers):
        """Create a new customer in the database."""
        self.session.add(customer)
        self.session.flush()
        self.session.refresh(customer)
        return customer

    def update_customer(self, customer_id: uuid.UUID, new_customer: Customers):
        """Update an existing customer"""
        customer = self.session.get(Customers, customer_id)

        if not customer:
            return None

        customer.name = new_customer.name
        customer.email = new_customer.email
        customer.phone = new_customer.phone
        customer.updated_at = datetime.datetime.now(tz=datetime.timezone.utc)

        self.session.flush()
        self.session.refresh(customer)
        return customer

    def delete_customer(self, customer_id: uuid.UUID):
        """Delete a customer from the database."""
        customer = self.session.get(Customers, customer_id)

        if not customer:
            return None

        self.session.delete(customer)
        self.session.flush()
