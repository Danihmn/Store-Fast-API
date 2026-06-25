from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from settings import Settings

engine = create_engine(Settings().DATABASE_URL)  # type: ignore


def get_session():
    """creates a new database session"""
    with Session(engine) as session:
        return session
