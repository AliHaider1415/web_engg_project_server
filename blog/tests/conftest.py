# conftest.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from blog.models import Blog, Comment

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password123', email='test@example.com', role = "user")

@pytest.fixture
def guest_user(db):
    user = User.objects.create_user(username='guestuser', password='password123', email='guest@example.com')
    user.role = "guest"  # Assign the "guest" role
    user.save()
    return user

@pytest.fixture
def auth_client_as_guest(api_client, guest_user):
    api_client.force_authenticate(user=guest_user)
    return api_client

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def blog(user):
    return Blog.objects.create(title="Test Blog", content="Test content", status="draft", author=user)
