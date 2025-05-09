import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_user_product_list(auth_client, product):
    url = reverse("user-products-list")
    response = auth_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_product_create(auth_client, category):
    url = reverse("user-products-list")
    data = {
        "name": "Phone",
        "description": "Smartphone",
        "price": 500,
        "category": category.id,
        "stock_quantity": 10
    }
    response = auth_client.post(url, data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_user_product_list_unauthenticated(api_client):
    url = reverse("user-products-list")
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_product_create_missing_fields(auth_client):
    url = reverse("user-products-list")
    data = {
        "name": "",
        "description": "Too short",
        # missing price, category, stock_quantity
    }
    response = auth_client.post(url, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_product_create_unauthenticated(api_client, category):
    url = reverse("user-products-list")
    data = {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 1500,
        "category": category.id,
        "stock_quantity": 5
    }
    response = api_client.post(url, data)
    assert response.status_code == 401