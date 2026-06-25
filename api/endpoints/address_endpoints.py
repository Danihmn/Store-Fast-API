from fastapi import APIRouter, Depends
from sqlalchemy import select

from domain.entities.address import Addresses
from infrastructure.data.database import get_session

router = APIRouter(
    prefix='/address',
)


@router.get('/get_all')
def get_address(session=Depends(get_session)):
    address = session.scalars(select(Addresses)).all()

    return address
