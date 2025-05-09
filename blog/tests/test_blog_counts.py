# tests/test_blog_counts.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_blog_count(auth_client, blog):
    url = reverse("blogs-count")
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "total_count" in response.data


@pytest.mark.django_db
def test_blog_count_unauthenticated(api_client):
    url = reverse("blogs-count")
    response = api_client.get(url)
    assert response.status_code == 401  # Unauthorized