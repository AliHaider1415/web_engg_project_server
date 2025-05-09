from rest_framework import serializers
from .models import Blog, Comment
from django.contrib.auth import get_user_model

class BlogSerializer(serializers.ModelSerializer):
    # Custom fields or relationships can be handled here
    author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    published_at = serializers.DateTimeField(required=False, allow_null=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'status', 'created_at', 'updated_at', 'published_at', 'category']
        read_only_fields = ['created_at', 'updated_at']

    def validate_title(self, value):
        """Custom validation for title."""
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long.")
        return value

    def validate_content(self, value):
        """Custom validation for content."""
        if len(value) < 20:
            raise serializers.ValidationError("Content must be at least 20 characters long.")
        return value
    
    def get_author(self, obj):
        # Return the username of the author
        return obj.author.username if obj.author else None
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
class UserBlogListSerializer(serializers.ModelSerializer):

    # Customizing the author field to return author.username
    author = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['id', 'title', 'author', 'status', 'category', 'published_at', 'created_at']
        read_only_fields = ['created_at']

    def get_author(self, obj):
        # Return the username of the author
        return obj.author.username if obj.author else None
    

# User serializer for author field
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']  # You can add more fields if necessary

# Blog serializer to include basic blog info in the comment serializer
class BlogSerializerForComment(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title']

# Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)  # Include the user data for the author
    blog = BlogSerializerForComment(read_only=True)  # Include the basic blog data

    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'blog', 'created_at', 'updated_at']

