from fastapi import FastAPI

from api.endpoints.address_endpoints import router as address_routers

app = FastAPI(
    title='Store API',
    description='API for managing stores',
    version='1.0.0',
)

app.include_router(router=address_routers)
