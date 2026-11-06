import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from tasks.models import Task

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="ephantus", email="ephantus@example.com", password="StrongPassword123"
    )


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


# test task creation


def test_user_can_create_task(authenticated_client, user):
    response = authenticated_client.post(
        "/api/tasks/",
        {
            "title": "Learn CI/CD",
            "description": "Build my first CI pipeline",
            "completed": False,
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["title"] == "Learn CI/CD"

    assert Task.objects.filter(title="Learn CI/CD", user=user).exists()


# test task ownership


def test_user_cannot_see_other_users_tasks(authenticated_client, user):
    another_user = User.objects.create_user(
        username="anotheruser", password="AnotherPassword123"
    )

    Task.objects.create(title="Private task", user=another_user)

    response = authenticated_client.get("/api/tasks/")

    assert response.status_code == 200
    assert len(response.data) == 0


# Test anauthorized access


def test_unauthenticatd_user_cannot_create_task():
    client = APIClient()

    response = client.post(
        "/api/tasks/",
        {"title": "Unauthorized task", "description": "This should not work"},
        format="json",
    )

    assert response.status_code == 401


# test invalid data


def test_user_cannot_create_task_without_title(authenticated_client):
    response = authenticated_client.post(
        "/api/tasks/", {"description": "This task has no title"}, format="json"
    )

    assert response.status_code == 400

    assert "title" in response.data


def test_user_can_filter_completed_tasks(authenticated_client, user):
    Task.objects.create(title="Completed task", user=user, completed=True)

    Task.objects.create(title="Incomplete task", user=user, completed=False)

    response = authenticated_client.get("/api/tasks/?completed=true")

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Completed task"
    assert response.data[0]["completed"] is True
