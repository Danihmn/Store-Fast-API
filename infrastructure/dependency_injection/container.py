from dependency_injector import containers, providers

from application.usecases.customer import (
    CreateHandler,
    DeleteHandler,
    GetAllHandler,
    GetByIdHandler,
    UpdateHandler,
)
from application.usecases.user import AuthenticateHandler
from infrastructure.data.database import session_scope
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.user_repository import UserRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            'api.endpoints.customer_endpoints',
            'api.endpoints.user_endpoints',
        ]
    )

    # repositories ============================================================
    customer_repository = providers.Factory(
        CustomerRepository, session_factory=session_scope
    )
    user_repository = providers.Factory(
        UserRepository, session_factory=session_scope
    )

    # use cases - customers ===================================================
    customer_get_all_handler = providers.Factory(
        GetAllHandler, repository=customer_repository
    )
    customer_get_by_id_handler = providers.Factory(
        GetByIdHandler, repository=customer_repository
    )
    customer_create_handler = providers.Factory(
        CreateHandler, repository=customer_repository
    )
    customer_update_handler = providers.Factory(
        UpdateHandler, repository=customer_repository
    )
    customer_delete_handler = providers.Factory(
        DeleteHandler, repository=customer_repository
    )

    # use cases - users =======================================================
    user_authenticate_handler = providers.Factory(
        AuthenticateHandler, repository=user_repository
    )
