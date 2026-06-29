from fastapi import FastAPI

from api.endpoints.address_endpoints import router as address_routers
from api.endpoints.customer_endpoints import router as customer_routers
from api.endpoints.user_endpoints import router as user_routers

app = FastAPI(
    title='Store API',
    description='API for managing stores',
    version='1.0.0',
)

app.include_router(router=address_routers)
app.include_router(router=customer_routers)
app.include_router(router=user_routers)
