from django.urls import path
from .views import UserBlogsListView, GuestBlogsView, BlogsDetailView, BlogsCountView, BlogCommentView

urlpatterns = [
    # URL for fetching all blogs or filtering user blogs
    path('user-blogs/', UserBlogsListView.as_view(), name='user-blogs-list'),  # GET and POST methods

    # URL for updating a specific user blog
    path('user-blogs/<int:pk>/', UserBlogsListView.as_view(), name='user-blogs-detail'),  # PUT and DELETE methods

    path('blogs-detail/<int:pk>/', BlogsDetailView.as_view(), name='blogs-detail'),

    # URL for all guest blogs
    path('guest-blogs/', GuestBlogsView.as_view(), name='guest-blogs-list'),  # GET and POST methods


    path('blogs-count/', BlogsCountView.as_view(), name='blogs-count'),

    path('blogs/<int:blog_id>/comments/', BlogCommentView.as_view(), name='blog-comments'),
]
