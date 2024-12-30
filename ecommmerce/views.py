from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product, Category, Cart
from .serializers import ProductSerializer, CartSerializer
from accounts.permissions import isUserAuthenticated, isGuestAuthenticated, isGuestOrUserAuthenticated


class UserProductsListView(APIView):
    """
    View for fetching all products of the authenticated user.
    If query parameters are provided, the products will be filtered based on those parameters.
    """
    permission_classes = [IsAuthenticated, isUserAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Fetching all products related to the current authenticated user
            products = Product.objects.filter(seller=request.user)

            # Check if query parameters are passed and apply filters
            if request.query_params:
                # Loop through all query params and apply them as filters to the queryset
                for param, value in request.query_params.items():
                    # Handle filters for known fields like category, price, min_price, max_price
                    if param == 'category':
                        products = products.filter(category__name__icontains=value)
                    elif param == 'price':
                        try:
                            price = float(value)
                            products = products.filter(price=price)
                        except ValueError:
                            return Response(
                                {"error": "Invalid price value."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    elif param == 'min_price':
                        try:
                            min_price = float(value)
                            products = products.filter(price__gte=min_price)
                        except ValueError:
                            return Response(
                                {"error": "Invalid min_price value."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    elif param == 'max_price':
                        try:
                            max_price = float(value)
                            products = products.filter(price__lte=max_price)
                        except ValueError:
                            return Response(
                                {"error": "Invalid max_price value."},
                                status=status.HTTP_400_BAD_REQUEST
                            )

            # If no products are found after applying all filters, return a message
            if not products.exists():
                return Response(
                    {"message": "No products found for this user with the given filters."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serializing the filtered products
            serializer = ProductSerializer(products, many=True)

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
            # Set the seller to the currently authenticated user
            data = request.data.copy()
            data['seller'] = request.user.id

            # Serializing the incoming data
            serializer = ProductSerializer(data=data)
            
            if serializer.is_valid():
                # Save the product if the data is valid
                product = serializer.save()

                # Return the serialized data of the created product
                return Response(ProductSerializer(product).data, status=status.HTTP_201_CREATED)
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

    def put(self, request, pk):
        try:
            # Fetching the product to update
            product = Product.objects.get(id=pk, seller=request.user)

            # If the product is not found, return a 404 error
            if not product:
                return Response(
                    {"error": "Product not found or you do not have permission to edit this product."},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Serializing the request data to update the product
            serializer = ProductSerializer(product, data=request.data, partial=True)  # partial=True allows partial updates

            if serializer.is_valid():
                # Save the updated product
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
            # Fetching the product to delete
            product = Product.objects.get(id=pk, seller=request.user)

            # If the product is not found, return a 404 error
            if not product:
                return Response(
                    {"error": "Product not found or you do not have permission to delete this product."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Deleting the product
            product.delete()

            # Return a success response
            return Response(
                {"message": "Product deleted successfully."},
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class ProductDetailView(APIView):
    """
    View for fetching the details of a single product by its ID.
    """
    permission_classes = [IsAuthenticated, isGuestOrUserAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        try:
            # Fetching the product with the given ID
            product = Product.objects.filter(id=pk, seller=request.user).first()

            # If the product does not exist or is not associated with the current user, return a 404 error
            if not product:
                return Response(
                    {"message": "Product not found or you do not have permission to view this product."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serializing the product data
            serializer = ProductSerializer(product)

            # Return the serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class GuestProductsView(APIView):
    """
    View for fetching all products with optional filters for guests or authenticated users.
    """
    permission_classes = [IsAuthenticated, isGuestAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Fetching all products
            products = Product.objects.all()

            # Check if query parameters are passed
            if request.query_params:
                # Loop through all query params and apply them as filters to the queryset
                for param, value in request.query_params.items():
                    # Handle filters for known fields like category, price, min_price, max_price, etc.
                    if param in ['category', 'price', 'min_price', 'max_price']:
                        # Apply filters based on the parameter
                        if param == 'category':
                            products = products.filter(category__name__icontains=value)
                        elif param == 'price':
                            products = products.filter(price=value)
                        elif param == 'min_price':
                            products = products.filter(price__gte=value)
                        elif param == 'max_price':
                            products = products.filter(price__lte=value)

            # If no products are found after applying all filters, return a message
            if not products.exists():
                return Response(
                    {"message": "No products found with the given filters."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serializing the filtered products
            serializer = ProductSerializer(products, many=True)

            # Return the serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unforeseen exceptions
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

# class BlogsCountView(APIView):
#     """
#     View for fetching all blogs of the authenticated user.
#     If query parameters are provided, the blogs will be filtered based on those parameters.
#     """
#     permission_classes = [IsAuthenticated, isGuestOrUserAuthenticated]
#     authentication_classes = [JWTAuthentication]

#     def get(self, request):
#         try:
#             # Base queryset for all blogs
#             blogs = Blog.objects.all()

#             # Filter blogs based on query parameters (if provided)
#             if request.query_params:
#                 for param, value in request.query_params.items():
#                     if param == 'status':
#                         blogs = blogs.filter(status=value)
#                     elif param == 'category':
#                         blogs = blogs.filter(category__icontains=value)

#             # Count total blogs
#             total_count = blogs.count()

#             # Count blogs by category
#             category_counts = blogs.values('category').annotate(count=Count('id')).order_by('category')

#             # Prepare response data
#             response_data = {
#                 "total_count": total_count,
#                 "categories": {item['category']: item['count'] for item in category_counts}
#             }

#             # Return the counts
#             return Response(response_data, status=status.HTTP_200_OK)

#         except Exception as e:
#             # Handle any unforeseen exceptions
#             return Response(
#                 {"error": str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


class CartDetailView(APIView):
    """
    View to retrieve the cart and its items for the authenticated user.
    """
    permission_classes = [isGuestOrUserAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            # Fetch the user's active cart
            cart = Cart.objects.filter(user=request.user, is_active=True).first()

            # If no active cart is found
            if not cart:
                return Response(
                    {"message": "No active cart found for this user."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the cart and its items
            serializer = CartSerializer(cart)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)