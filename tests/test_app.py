import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    base_data = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }

    activities.clear()
    activities.update(base_data)
    yield
    activities.clear()
    activities.update(base_data)


def test_get_activities():
    # Arrange (initial data in fixture)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_and_duplicate_blocked():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act: first signup
    first_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert first signup works
    assert first_response.status_code == 200
    assert email in activities[activity_name]["participants"]

    # Act: duplicate signup
    duplicate_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert duplicate is blocked
    assert duplicate_response.status_code == 400
    assert activities[activity_name]["participants"].count(email) == 1


def test_unregister_participant():
    # Arrange
    activity_name = "Programming Class"
    participant_email = "emma@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": participant_email}
    )

    # Assert
    assert response.status_code == 200
    assert participant_email not in activities[activity_name]["participants"]
