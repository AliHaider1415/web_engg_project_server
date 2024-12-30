from rest_framework import serializers
from .models import Product, Category, Cart, CartItem
from django.contrib.auth import get_user_model

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field='username', queryset=get_user_model().objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

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


class ProductListSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(slug_field='username', queryset=get_user_model().objects.all())
    category = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'seller', 'stock_quantity', 
            'category', 'created_at', 'updated_at', 'image'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_category(self, obj):
        return obj.category.name  # Return the category name

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.FloatField(read_only=True)  # Removed source='total_price'
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'item_count', 'is_active']
