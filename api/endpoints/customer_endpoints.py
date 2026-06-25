from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select

from application.schemas.customer_schema import (
    CustomerCreate,
    CustomerResponse,
)
from domain.entities.customer import Customers
from infrastructure.data.database import get_session

router = APIRouter(
    prefix='/customer',
)


@router.get(
    '/', response_model=list[CustomerResponse], response_class=JSONResponse
)
def get_customers(
    session=Depends(get_session), skip: int = 0, take: int = 100
):
    customers = session.scalars(select(Customers).offset(skip).limit(take))
    return customers


@router.post(
    '/create', response_model=CustomerResponse, response_class=JSONResponse
)
def create_customer(customer: CustomerCreate, session=Depends(get_session)):
    existing = session.scalar(
        select(Customers).where(
            (Customers.email == customer.email)
            | (Customers.phone == customer.phone)
        )
    )

    if existing:
        if existing.email == customer.email:
            raise HTTPException(
                status_code=400,
                detail='Customer with this email already exists',
            )
        elif existing.phone == customer.phone:
            raise HTTPException(
                status_code=400,
                detail='Customer with this phone already exists',
            )

    db_customer = Customers(
        name=customer.name, email=customer.email, phone=customer.phone
    )

    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)

    return db_customer
