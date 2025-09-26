import pytest
from httpx import (AsyncClient,
                   ASGITransport)  # allows testing directly against FastAPI apps (without starting a real server).
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.session import get_db
from app.models.user import Base, UserRole
from app.core.config import settings

# --- Test Database Setup ---
# Use a separate database for testing
TEST_DATABASE_URL = f"{settings.DATABASE_URL}"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Fixtures for Test Isolation ---

@pytest.fixture(scope="session", autouse=True)  # runs once per test session automatically.
def setup_test_db():
    """
    Fixture to create and tear down the test database tables for the entire test session.
    'autouse=True' ensures it runs automatically for the session.
    """
    Base.metadata.create_all(bind=engine)
    yield  # pauses here while tests run.
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """
    Dependency override to use the test database session.
    """
    try:
        db = TestingSessionLocal()
        yield db  # returns a session to FastAPI routes.
    finally:
        db.close()  # ensures session is closed after use.


# Apply the dependency override to our app
app.dependency_overrides[get_db] = override_get_db


# Fixture to provide an async test client for making API requests
@pytest.fixture(scope="module")
async def client() -> AsyncClient:
    """
    Provides an async client to interact with the FastAPI application.
    """
    # httpx.AsyncClient doesn't directly accept a FastAPI app object (no server needed)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# --- Test Cases ---

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    """
    Test successful user registration.
    """
    # Arrange
    user_data = {
        "email": "testuser@example.com",
        "password": "strongpassword123",
        "password_repeat": "strongpassword123",
        "role": UserRole.CUSTOMER.value
    }

    # Act
    response = await client.post("/api/v1/register", json=user_data)
    print('response', response)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["role"] == user_data["role"]
    assert data["is_active"] is True
    assert "password" not in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient):
    """
    Test registration failure when an email is already taken.
    """
    # Arrange: A user with this email already exists from the previous test.
    user_data = {
        "email": "testuser@example.com",
        "password": "anotherpassword",
        "password_repeat": "anotherpassword",
        "role": UserRole.CUSTOMER.value
    }

    # Act
    response = await client.post("/api/v1/register", json=user_data)

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """
    Test successful login and token generation.
    """
    # Arrange: The user 'testuser@example.com' exists.
    login_data = {
        "username": "testuser@example.com",
        "password": "strongpassword123"
    }

    # Act
    response = await client.post("/api/v1/token", data=login_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_incorrect_password(client: AsyncClient):
    """
    Test login failure with an incorrect password.
    """
    # Arrange
    login_data = {
        "username": "testuser@example.com",
        "password": "wrongpassword"
    }

    # Act
    response = await client.post("/api/v1/token", data=login_data)

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_read_users_me_success(client: AsyncClient):
    """
    Test accessing a protected route with a valid token.
    """
    # Arrange: First, log in to get a token
    login_data = {"username": "testuser@example.com", "password": "strongpassword123"}
    login_response = await client.post("/api/v1/token", data=login_data)
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    # Act
    response = await client.get("/api/v1/users/me", headers=headers)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["role"] == "customer"


@pytest.mark.asyncio
async def test_read_users_me_no_token(client: AsyncClient):
    """
    Test accessing a protected route without providing a token.
    """
    # Act
    response = await client.get("/api/v1/users/me")

    # Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
