from fastapi import HTTPException, Header
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from main import app
from configs.db import Base, get_db
from controllers.authentication import get_user_from_token

DATABASE_URL = "postgresql://admin:admin123@localhost:5432/profile_test"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def mock_get_user_from_token(_token: str = None):
    return "mocked_email@example.com"

def mock_get_user_from_token_user_2(_token: str = None):
    return "mocked_email_2@example.com"

def mock_get_user_from_token_invalid(_token: str = None):
    raise HTTPException(status_code=401, detail="Invalid token")
   
app.dependency_overrides[get_user_from_token] = mock_get_user_from_token

client = TestClient(app)


def test_create_profile():
    data = {
        "name": "John",
        "surname": "Doe",
        "username": "johndoe",
        "location": "New York",
        "description": "Developer",
        "date_of_birth": "1990-01-01",
        "interests": ["coding", "reading"]
    }
    response = client.post(
        "/profiles/", 
        json=data,
        headers={"Authorization": "Bearer mocktoken"}
    )
    
    assert response.status_code == 200
    assert response.json() == {"message": "Profile created successfully"}



def test_create_profile_invalid_token():
    app.dependency_overrides[get_user_from_token] = mock_get_user_from_token_invalid
    data = {
        "name": "John",
        "surname": "Doe",
        "username": "johndoe",
        "location": "New York",
        "description": "Developer",
        "date_of_birth": "1990-01-01",
        "interests": ["coding", "reading"]
    }
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.post("/profiles/", json=data, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"




def test_get_profile():
    app.dependency_overrides[get_user_from_token] = mock_get_user_from_token
    headers = {"Authorization": "Bearer mocktoken"}
    response = client.get("/profiles/", headers=headers)
    assert response.status_code == 200
    profile = response.json()
    assert profile["email"] == "mocked_email@example.com"
    assert profile["name"] == "John"
    assert profile["surname"] == "Doe"
    assert profile["username"] == "johndoe"


def test_update_profile():
    data = {
        "name": "John Updated",
        "surname": "Doe Updated",
        "username": "johndoe",
        "location": "San Francisco",
        "description": "Senior Developer",
        "date_of_birth": "1990-01-01",
        "interests": ["coding", "gaming"]
    }
    headers = {"Authorization": "Bearer mocktoken"}
    response = client.put("/profiles/", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Profile updated successfully"}

def test_get_all_usernames():
    response = client.get("/profiles/all-usernames")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0] == "johndoe"

def test_get_profile_by_username():
    response = client.get("/profiles/by-username?username=johndoe")
    assert response.status_code == 200
    profile = response.json()
    assert profile["email"] == "mocked_email@example.com"
    assert profile["name"] == "John Updated"

def test_get_profile_by_username_not_found():
    response = client.get("/profiles/by-username?username=unknown")
    assert response.status_code == 404
    assert response.json()["detail"] == "Profile for username unknown not found."


def test_delete_profile():
    headers = {"Authorization": "Bearer mocktoken"}
    response = client.delete("/profiles/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Profile deleted successfully"}



def test_get_profile_invalid_token():
    app.dependency_overrides[get_user_from_token] = mock_get_user_from_token_invalid
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/profiles/", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"

def test_follow_user_success():
    app.dependency_overrides[get_user_from_token] = mock_get_user_from_token

    data = {
        "name": "John",
        "surname": "Doe",
        "username": "johndoe",
        "location": "New York",
        "description": "Developer",
        "date_of_birth": "1990-01-01",
        "interests": ["coding", "reading"]
    }
    client.post(
        "/profiles/", 
        json=data,
        headers={"Authorization": "Bearer mocktoken"}
    )

    app.dependency_overrides[get_user_from_token] = mock_get_user_from_token_user_2

    data = {
        "name": "Jane",
        "surname": "Doe",
        "username": "janedoe",
        "location": "New York",
        "description": "Developer",
        "date_of_birth": "1990-01-01",
        "interests": ["coding", "reading"]
    }
    client.post(
        "/profiles/", 
        json=data,
        headers={"Authorization": "Bearer mocktoken"}
    )

    response = client.post("/profiles/follow?username=johndoe", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 200
    assert response.json() == {"message": "User followed successfully"}

def test_get_followers_unauthorized():
    response = client.get("/profiles/followers?username=johndoe", headers={"Authorization":"Bearer invalid_token"})

    assert response.status_code == 400
    assert response.json() == {"detail": "User janedoe is not authorized to view followers of user johndoe"}

def test_get_followed_unauthorized():
    response = client.get("/profiles/followed?username=johndoe", headers={"Authorization":"Bearer invalid_token"})

    assert response.status_code == 400
    assert response.json() == {"detail": "User janedoe is not authorized to view followed of user johndoe"}

def test_get_followers():
    app.dependency_overrides[get_user_from_token] = mock_get_user_from_token

    client.post("/profiles/follow?username=janedoe", headers={"Authorization": "Bearer invalid_token"})

    response = client.get("/profiles/followers?username=johndoe", headers={"Authorization":"Bearer invalid_token"})

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0] == "janedoe"

def test_get_followed():
    response = client.get("/profiles/followed?username=janedoe", headers={"Authorization":"Bearer invalid_token"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0] == "johndoe"

def test_get_my_followers():
    response = client.get("/profiles/followers?username=johndoe", headers={"Authorization":"Bearer invalid_token"})
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0] == "janedoe"

def test_get_my_followed():
    response = client.get("/profiles/followed?username=johndoe", headers={"Authorization":"Bearer invalid_token"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0] == "janedoe"

def test_follow_inexistent_user():
    response = client.post("/profiles/follow?username=unexisting", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 400
    assert response.json() == {"detail": "User with username unexisting not found."}

def test_follow_already_followed_user():
    app.dependency_overrides[get_user_from_token] = mock_get_user_from_token_user_2

    response = client.post("/profiles/follow?username=johndoe", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 400
    assert response.json() == {"detail": "User with username johndoe is already followed by user with username janedoe"}

def test_unfollow_user_success():
    response = client.delete("/profiles/unfollow?username=johndoe", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 200
    assert response.json() == {"message": "User unfollowed successfully"}

def test_unfollow_inexistent_user():
    response = client.delete("/profiles/unfollow?username=unexisting", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 400
    assert response.json() == {"detail": "User with username unexisting not found."}

def test_unfollow_not_followed_user():
    response = client.delete("/profiles/unfollow?username=johndoe", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 400
    assert response.json() == {"detail": "User with username johndoe is not followed by user with username janedoe"}

def test_cannot_follow_self():
    response = client.post("/profiles/follow?username=janedoe", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot follow yourself."}
