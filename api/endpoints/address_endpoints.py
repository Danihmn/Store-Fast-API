from fastapi import APIRouter
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from domain.entities.address import Addresses
from settings import Settings

router = APIRouter(
    prefix='/address',
)


@router.get('/get_all')
async def get_address():
    engine = create_engine(Settings().DATABASE_URL)  # type: ignore
    session = Session(engine)

    addresses = session.scalars(select(Addresses)).all()
    session.close()

    return addresses
