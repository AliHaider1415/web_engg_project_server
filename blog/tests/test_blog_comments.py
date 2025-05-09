# tests/test_blog_comments.py
import pytest
from django.urls import reverse
from blog.models import Comment

@pytest.mark.django_db
def test_get_blog_comments(auth_client, blog):
    url = reverse("blog-comments", args=[blog.id])
    response = auth_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_blog_comment(auth_client, blog):
    url = reverse("blog-comments", args=[blog.id])
    data = {"content": "Nice post!"}
    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert response.data["content"] == "Nice post!"

# tests/test_blog_comments.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_get_blog_comments(auth_client, blog):
    url = reverse("blog-comments", args=[blog.id])
    response = auth_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_create_blog_comment(auth_client, blog):
    url = reverse("blog-comments", args=[blog.id])
    data = {"content": "Nice post!"}
    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert response.data["content"] == "Nice post!"

# Negative test cases

@pytest.mark.django_db
def test_create_blog_comment_invalid_data(auth_client, blog):
    url = reverse("blog-comments", args=[blog.id])
    data = {"content": ""}  # Invalid: empty comment
    response = auth_client.post(url, data)
    assert response.status_code == 400
    assert "content" in response.data

@pytest.mark.django_db
def test_create_blog_comment_unauthenticated_user(api_client, blog):
    url = reverse("blog-comments", args=[blog.id])
    data = {"content": "Trying without login"}
    response = api_client.post(url, data)
    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_get_blog_comments_invalid_blog_id(auth_client):
    invalid_blog_id = 9999
    url = reverse("blog-comments", args=[invalid_blog_id])
    response = auth_client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_create_comment_invalid_blog_id(auth_client):
    url = reverse("blog-comments", args=[9999])
    data = {"content": "Doesn't matter"}
    response = auth_client.post(url, data)
    assert response.status_code == 404
