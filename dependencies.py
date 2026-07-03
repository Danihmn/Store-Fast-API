from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from application.usecases.customer.create.handler import (
    Handler as CreateHandler,
)
from application.usecases.customer.delete.handler import (
    Handler as DeleteHandler,
)
from application.usecases.customer.get_all.handler import (
    Handler as GetAllHandler,
)
from application.usecases.customer.get_by_id.handler import (
    Handler as GetByIdHandler,
)
from application.usecases.customer.update.handler import (
    Handler as UpdateHandler,
)
from application.usecases.user.authenticate.handler import (
    Handler as AuthenticateHandler,
)
from infrastructure.data.database import engine
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.user_repository import UserRepository


# Database ====================================================================
def get_session():
    """Creates a new database session"""
    with Session(engine) as session:
        yield session
        session.commit()


# Repositories ================================================================
SessionDependency = Annotated[Session, Depends(get_session)]


def get_customer_repository(
    session: SessionDependency,
):
    """Get the customer repository."""
    return CustomerRepository(session)


def get_user_repository(
    session: SessionDependency,
):
    """Get the user repository."""
    return UserRepository(session)


# Use Cases - Customers =======================================================
def get_customer_get_all_handler(
    customer_repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    """Get the customer get all use case handler."""
    return GetAllHandler(repository=customer_repository)


def get_customer_by_id_handler(
    customer_repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    """Get the customer get by id use case handler."""
    return GetByIdHandler(repository=customer_repository)


def get_customer_create_handler(
    customer_repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    """Get the customer create use case handler."""
    return CreateHandler(repository=customer_repository)


def get_customer_update_handler(
    customer_repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    """Get the customer update use case handler."""
    return UpdateHandler(repository=customer_repository)


def get_customer_delete_handler(
    customer_repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
):
    """Get the customer delete use case handler."""
    return DeleteHandler(repository=customer_repository)


# Use Cases - Users ===========================================================
def get_user_authenticate_handler(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
):
    """Get the user authenticate use case handler."""
    return AuthenticateHandler(repository=user_repository)
