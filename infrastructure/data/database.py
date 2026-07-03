from sqlalchemy import create_engine

from settings import Settings

engine = create_engine(Settings().DATABASE_URL)  # type: ignore
