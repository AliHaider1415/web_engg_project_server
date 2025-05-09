import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_add_to_cart(auth_client, product):
    url = reverse("cart-items")
    data = {"product_id": product.id, "quantity": 2}
    response = auth_client.post(url, data)
    assert response.status_code == 201
    assert response.data["message"] == "Product added to cart."

@pytest.mark.django_db
def test_get_cart_items(auth_client):
    url = reverse("cart-items")
    response = auth_client.get(url)
    assert response.status_code == 200
    assert "items" in response.data

@pytest.mark.django_db
def test_update_cart_item(auth_client, product):
    url = reverse("cart-items")
    # Add item first
    auth_client.post(url, {"product_id": product.id, "quantity": 1})
    # Get cart item ID
    cart_items = auth_client.get(url).data["items"]
    cart_item_id = cart_items[0]["id"]
    # Update it
    response = auth_client.put(url, {"cart_item_id": cart_item_id, "quantity": 3})
    assert response.status_code == 200
    assert response.data["message"] == "Cart item updated."

@pytest.mark.django_db
def test_delete_cart_item(auth_client, product):
    url = reverse("cart-items")
    auth_client.post(url, {"product_id": product.id, "quantity": 1})
    cart_item_id = auth_client.get(url).data["items"][0]["id"]
    response = auth_client.delete(url, {"cart_item_id": cart_item_id}, format="json")
    assert response.status_code == 200
    assert response.data["message"] == "Cart item removed."


@pytest.mark.django_db
def test_add_to_cart_invalid_product(auth_client):
    url = reverse("cart-items")
    data = {"product_id": 9999, "quantity": 2}  # Assuming 9999 doesn't exist
    response = auth_client.post(url, data)
    assert response.status_code in [400, 404]


@pytest.mark.django_db
def test_add_to_cart_invalid_quantity(auth_client, product):
    url = reverse("cart-items")
    data = {"product_id": product.id, "quantity": 0}
    response = auth_client.post(url, data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_get_cart_items_unauthenticated(api_client):
    url = reverse("cart-items")
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_update_cart_item_invalid_id(auth_client):
    url = reverse("cart-items")
    response = auth_client.put(url, {"cart_item_id": 9999, "quantity": 2})
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_cart_item_invalid_quantity(auth_client, product):
    url = reverse("cart-items")
    auth_client.post(url, {"product_id": product.id, "quantity": 1})
    cart_items = auth_client.get(url).data["items"]
    cart_item_id = cart_items[0]["id"]
    response = auth_client.put(url, {"cart_item_id": cart_item_id, "quantity": 0})
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_cart_item_invalid_id(auth_client):
    url = reverse("cart-items")
    response = auth_client.delete(url, {"cart_item_id": 9999}, format="json")
    assert response.status_code == 404