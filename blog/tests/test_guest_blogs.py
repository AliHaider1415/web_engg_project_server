# tests/test_guest_blogs.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_guest_blogs(auth_client_as_guest, blog):
    url = reverse("guest-blogs-list")
    response = auth_client_as_guest.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1

@pytest.mark.django_db
def test_guest_blogs_unauthenticated(api_client, blog):
    url = reverse("guest-blogs-list")
    response = api_client.get(url)
    assert response.status_code == 401  