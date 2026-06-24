import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    load_dotenv('.env')
    engine = create_engine(
        URL.create(
            drivername='postgresql+psycopg2',
            username=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD'),
            database=os.getenv('DATABASE_NAME'),
            host='localhost',
        )
    )
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
