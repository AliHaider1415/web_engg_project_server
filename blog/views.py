from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog, Comment
from django.db.models import Count
from .serializers import BlogSerializer, UserBlogListSerializer, CommentSerializer
from accounts.permissions import isUserAuthenticated, isGuestAuthenticated, isGuestOrUserAuthenticated
from django.shortcuts import get_object_or_404



class UserBlogsListView(APIView):
    """
    View for fetching all blogs of the authenticated user.
    If query parameters are provided, the blogs will be filtered based on those parameters.
    """
    permission_classes = [IsAuthenticated, isUserAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Fetching all blogs related to the current authenticated user
            blogs = Blog.objects.filter(author=request.user)

            # Check if query parameters are passed
            if request.query_params:
                # Loop through all query params and apply them as filters to the queryset
                for param, value in request.query_params.items():
                    # Handle filters for known fields like status, category, title, etc.
                    if param in ['status', 'category']:
                        # Apply filters directly
                        if param == 'status':
                            blogs = blogs.filter(status=value)
                        elif param == 'category':
                            blogs = blogs.filter(category__icontains=value)

            # If no blogs are found after applying all filters, return a message
            if not blogs.exists():
                return Response(
                    {"message": "No blogs found for this user with the given filters."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serializing the filtered blogs
            serializer = UserBlogListSerializer(blogs, many=True)

            # Return the serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:

            # Serializing the incoming data
            serializer = BlogSerializer(data=request.data, context={"request": request})
            
            if serializer.is_valid():
                # Save the blog if the data is valid
                blog = serializer.save()

                # Return the serialized data of the created blog
                return Response(BlogSerializer(blog).data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except Exception as e:
            print("Error: ", str(e))
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        try:
            # Fetching the blog to update
            blog = Blog.objects.get(id=pk)

            # If the blog is not found, return a 404 error
            if not blog:
                return Response(
                    {"error": "Blog not found or you do not have permission to edit this blog."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Serializing the request data to update the blog
            serializer = BlogSerializer(blog, data=request.data, partial=True)  # partial=True allows partial updates

            if serializer.is_valid():
                # Save the updated blog
                serializer.save()

                # Return the updated serialized data
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        try:
            # Fetching the blog to delete
            blog = Blog.objects.get(id=pk)

            # If the blog is not found, return a 404 error
            if not blog:
                return Response(
                    {"error": "Blog not found or you do not have permission to delete this blog."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Deleting the blog
            blog.delete()

            # Return a success response
            return Response(
                {"message": "Blog deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class BlogsDetailView(APIView):
    """
    View for fetching all blogs of the authenticated user.
    If query parameters are provided, the blogs will be filtered based on those parameters.
    """
    permission_classes = [IsAuthenticated, isGuestOrUserAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            # Fetching all blogs related to the current authenticated user
            blogs = Blog.objects.filter(id = pk)

            # Check if query parameters are passed
            if request.query_params:
                # Loop through all query params and apply them as filters to the queryset
                for param, value in request.query_params.items():
                    # Handle filters for known fields like status, category, title, etc.
                    if param in ['status', 'category']:
                        # Apply filters directly
                        if param == 'status':
                            blogs = blogs.filter(status=value)
                        elif param == 'category':
                            blogs = blogs.filter(category__icontains=value)

            # If no blogs are found after applying all filters, return a message
            if not blogs.exists():
                return Response(
                    {"message": "No blogs found for this user with the given filters."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serializing the filtered blogs
            serializer = BlogSerializer(blogs, many=True)

            # Return the serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class GuestBlogsView(APIView):
    """
    
    """
    permission_classes = [IsAuthenticated, isGuestAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Fetching all blogs related to the current authenticated user
            blogs = Blog.objects.all()

            # Check if query parameters are passed
            if request.query_params:
                # Loop through all query params and apply them as filters to the queryset
                for param, value in request.query_params.items():
                    # Handle filters for known fields like status, category, title, etc.
                    if param in ['status', 'category']:
                        # Apply filters directly
                        if param == 'status':
                            blogs = blogs.filter(status=value)
                        elif param == 'category':
                            blogs = blogs.filter(category__icontains=value)

            # If no blogs are found after applying all filters, return a message
            if not blogs.exists():
                return Response(
                    {"message": "No blogs found with the given filters."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serializing the filtered blogs
            serializer = UserBlogListSerializer(blogs, many=True)

            # Return the serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BlogsCountView(APIView):
    """
    View for fetching all blogs of the authenticated user.
    If query parameters are provided, the blogs will be filtered based on those parameters.
    """
    permission_classes = [IsAuthenticated, isGuestOrUserAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Base queryset for all blogs
            blogs = Blog.objects.all()

            # Filter blogs based on query parameters (if provided)
            if request.query_params:
                for param, value in request.query_params.items():
                    if param == 'status':
                        blogs = blogs.filter(status=value)
                    elif param == 'category':
                        blogs = blogs.filter(category__icontains=value)

            # Count total blogs
            total_count = blogs.count()

            # Count blogs by category
            category_counts = blogs.values('category').annotate(count=Count('id')).order_by('category')

            # Prepare response data
            response_data = {
                "total_count": total_count,
                "categories": {item['category']: item['count'] for item in category_counts}
            }

            # Return the counts
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BlogCommentView(APIView):
    """
    View to handle comments for a specific blog post.
    Allows fetching all comments and creating a new comment.
    """
    permission_classes = [IsAuthenticated, isGuestOrUserAuthenticated]

    def get(self, request, blog_id):
        """
        Get all comments for a specific blog post.
        """

        blog = get_object_or_404(Blog, id=blog_id)
        comments = Comment.objects.filter(blog=blog).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, blog_id):
        """
        Create a new comment for a specific blog post.
        """
        blog = get_object_or_404(Blog, id=blog_id)

        data = request.data.copy()
        data["author"] = request.user.id 
        # Deserialize the incoming data
        serializer = CommentSerializer(data=data)

        # Validate and save the comment
        if serializer.is_valid():
            serializer.save(blog=blog, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)