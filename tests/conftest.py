from typing import Iterator
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_session
from sqlmodel import create_engine, StaticPool, SQLModel, Session

@pytest.fixture
def session() -> Iterator[Session]:
    engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool
        )
    SQLModel.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            yield session
    finally:
        engine.dispose()

@pytest.fixture
def client(session) -> Iterator[TestClient]:
    def override_get_session():
        yield session
    
    app.dependency_overrides[get_session] = override_get_session

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_session, None)
