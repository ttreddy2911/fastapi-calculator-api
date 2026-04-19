from app.models import User
from app.auth import verify_password


def test_register_user_success(client, db_session):
    payload = {
        "username": "student1",
        "email": "student1@example.com",
        "password": "supersecure123",
    }

    response = client.post("/users/register", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "password" not in data
    assert "hashed_password" not in data

    saved_user = db_session.query(User).filter(User.email == payload["email"]).first()
    assert saved_user is not None
    assert saved_user.username == payload["username"]
    assert saved_user.hashed_password != payload["password"]
    assert verify_password(payload["password"], saved_user.hashed_password) is True


def test_register_duplicate_email_fails(client):
    first_payload = {
        "username": "student2",
        "email": "duplicate@example.com",
        "password": "supersecure123",
    }

    second_payload = {
        "username": "anotheruser",
        "email": "duplicate@example.com",
        "password": "anothersecure123",
    }

    first_response = client.post("/users/register", json=first_payload)
    second_response = client.post("/users/register", json=second_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Email already registered"


def test_register_duplicate_username_fails(client):
    first_payload = {
        "username": "sameuser",
        "email": "sameuser1@example.com",
        "password": "supersecure123",
    }

    second_payload = {
        "username": "sameuser",
        "email": "sameuser2@example.com",
        "password": "anothersecure123",
    }

    first_response = client.post("/users/register", json=first_payload)
    second_response = client.post("/users/register", json=second_payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Username already taken"


def test_register_invalid_data_returns_422(client):
    payload = {
        "username": "ab",
        "email": "not-an-email",
        "password": "123",
    }

    response = client.post("/users/register", json=payload)

    assert response.status_code == 422


def test_login_success(client):
    register_payload = {
        "username": "student3",
        "email": "student3@example.com",
        "password": "supersecure123",
    }

    register_response = client.post("/users/register", json=register_payload)
    assert register_response.status_code == 201

    login_payload = {
        "email": "student3@example.com",
        "password": "supersecure123",
    }

    login_response = client.post("/users/login", json=login_payload)

    assert login_response.status_code == 200
    data = login_response.json()

    assert data["message"] == "Login successful"
    assert data["user"]["username"] == "student3"
    assert data["user"]["email"] == "student3@example.com"
    assert "id" in data["user"]
    assert "hashed_password" not in data["user"]


def test_login_wrong_password_fails(client):
    register_payload = {
        "username": "student4",
        "email": "student4@example.com",
        "password": "supersecure123",
    }

    register_response = client.post("/users/register", json=register_payload)
    assert register_response.status_code == 201

    response = client.post(
        "/users/login",
        json={
            "email": "student4@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_unknown_email_fails(client):
    response = client.post(
        "/users/login",
        json={
            "email": "unknown@example.com",
            "password": "supersecure123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_invalid_payload_returns_422(client):
    response = client.post(
        "/users/login",
        json={
            "email": "not-an-email",
            "password": "",
        },
    )

    assert response.status_code == 422