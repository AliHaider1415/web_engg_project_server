import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_product_detail_view(auth_client, product):
    url = reverse("product-detail", args = [product.id])
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == product.name

@pytest.mark.django_db
def test_product_detail_invalid_id(auth_client):
    url = reverse("product-detail", args=[9999])  # Assuming ID 9999 does not exist
    response = auth_client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_product_detail_unauthenticated(api_client, product):
    url = reverse("product-detail", args=[product.id])
    response = api_client.get(url)
    assert response.status_code == 401