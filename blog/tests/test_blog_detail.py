# tests/test_blog_detail.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_blog_detail(auth_client, blog):
    url = reverse("blogs-detail", args=[blog.id])
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data[0]["title"] == "Test Blog"

@pytest.mark.django_db
def test_blog_detail_unauthenticated(api_client, blog):
    url = reverse("blogs-detail", args=[blog.id])
    response = api_client.get(url)
    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_blog_detail_nonexistent(auth_client):
    url = reverse("blogs-detail", args=[9999])  # Assuming this ID doesn't exist
    response = auth_client.get(url)
    assert response.status_code in [404, 200]  # Adjust based on your view logic
    if response.status_code == 200:
        assert response.data == []  # Your view might return an empty list