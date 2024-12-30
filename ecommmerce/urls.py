from django.urls import path
from .views import UserProductsListView, GuestProductsView, ProductDetailView, CartItemsView

urlpatterns = [
    # URL for fetching all blogs or filtering user blogs
    path('user-products/', UserProductsListView.as_view(), name='user-products-list'),  # GET and POST methods

    # URL for updating a specific user blog
    path('user-products/<int:pk>/', UserProductsListView.as_view(), name='user-products-detail'),  # PUT and DELETE methods

    path('product-detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    # URL for all guest blogs
    path('guest-products/', GuestProductsView.as_view(), name='guest-products-list'),  # GET and POST methods


    path('cart/', CartItemsView.as_view(), name='cart-items'),


    # path('blogs-count/', BlogsCountView.as_view(), name='blogs-count'),
]
