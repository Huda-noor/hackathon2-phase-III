"""Pytest fixtures for testing."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel.pool import StaticPool
from jose import jwt
from datetime import datetime, timedelta

from src.main import app
from src.api.deps import get_db
from src.core.config import settings


# Create in-memory SQLite engine for testing
@pytest.fixture(name="engine")
def engine_fixture():
    """Create in-memory SQLite engine for tests."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create database session for tests."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with overridden database dependency."""

    async def get_session_override():
        yield session

    app.dependency_overrides[get_db] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def mock_jwt_token():
    """Generate a mock JWT token for testing."""
    payload = {
        "sub": "test-user-123",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


@pytest.fixture
def auth_headers(mock_jwt_token):
    """Create authorization headers with mock JWT token."""
    return {"Authorization": f"Bearer {mock_jwt_token}"}


@pytest.fixture
def mock_jwt_token_user2():
    """Generate a mock JWT token for second test user."""
    payload = {
        "sub": "test-user-456",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return token


@pytest.fixture
def auth_headers_user2(mock_jwt_token_user2):
    """Create authorization headers for second test user."""
    return {"Authorization": f"Bearer {mock_jwt_token_user2}"}
