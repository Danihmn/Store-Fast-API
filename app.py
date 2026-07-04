from fastapi import FastAPI

from api.endpoints.customer_endpoints import router as customer_routers
from api.endpoints.user_endpoints import router as user_routers
from infrastructure.dependency_injection.container import Container

container = Container()
container.wire(
    modules=[
        'api.endpoints.customer_endpoints',
        'api.endpoints.user_endpoints',
    ]
)

app = FastAPI(
    title='Store API',
    description='API for managing stores',
    version='1.0.0',
)

app.container = container  # type: ignore

app.include_router(router=customer_routers)
app.include_router(router=user_routers)
