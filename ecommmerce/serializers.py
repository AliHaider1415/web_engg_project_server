from rest_framework import serializers
from .models import Product, Category, Cart, CartItem
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    # Nested serializer for the seller (user) and category
    seller = serializers.SlugRelatedField(slug_field='username', queryset=get_user_model().objects.all())
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'seller', 'stock_quantity', 
            'category', 'created_at', 'updated_at', 'image'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value



class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', 
        read_only=True, 
        max_digits=10,  # Define the maximum number of digits
        decimal_places=2  # Define the number of decimal places
    )
    total_price = serializers.DecimalField(
        source='total_price', 
        read_only=True, 
        max_digits=10,  # Define the maximum number of digits
        decimal_places=2  # Define the number of decimal places
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity', 'product_price', 'total_price', 'added_at']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        source='total_price', 
        read_only=True, 
        max_digits=10,  # Define the maximum number of digits
        decimal_places=2  # Define the number of decimal places
    )
    item_count = serializers.IntegerField(source='item_count', read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'item_count', 'created_at', 'updated_at', 'is_active']
