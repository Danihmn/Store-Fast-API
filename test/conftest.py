import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

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
    return Session(engine)
