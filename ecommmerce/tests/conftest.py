import pytest
from rest_framework.test import APIClient
from ecommmerce.models import Category, Product, Cart
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password", email='test@example.com', role = "user")

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def category():
    return Category.objects.create(name="Electronics")

@pytest.fixture
def product(user, category):
    return Product.objects.create(name="Laptop", description="Powerful", price=1000, seller=user, category=category, stock_quantity = 10)

@pytest.fixture
def cart(user):
    return Cart.objects.create(user=user, is_active=True)
