# tests/test_user_blogs.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_user_blogs_list(auth_client, blog):
    url = reverse("user-blogs-list")  # make sure this matches your urls.py
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data[0]["title"] == "Test Blog"

@pytest.mark.django_db
def test_user_blogs_create(auth_client):
    url = reverse("user-blogs-list")
    data = {
        "title": "New Blog",
        "content": "This is a new blog post",
        "status": "published"
    }
    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert response.data["title"] == "New Blog"


@pytest.mark.django_db
def test_user_blogs_create_missing_title(auth_client):
    url = reverse("user-blogs-list")
    data = {
        "content": "Missing title here",
        "status": "draft"
    }
    response = auth_client.post(url, data)
    assert response.status_code == 400
    assert "title" in response.data["error"]

@pytest.mark.django_db
def test_user_blogs_create_invalid_status(auth_client):
    url = reverse("user-blogs-list")
    data = {
        "title": "Invalid status blog",
        "content": "Test content",
        "status": "invalid_status"
    }
    response = auth_client.post(url, data)
    assert response.status_code == 400
    assert "status" in response.data["error"]

@pytest.mark.django_db
def test_user_blogs_create_unauthenticated(api_client):
    url = reverse("user-blogs-list")
    data = {
        "title": "Should not work",
        "content": "No user",
        "status": "published"
    }
    response = api_client.post(url, data)
    assert response.status_code == 401  # Unauthorized
