import logging

from api import errors
from api.models import Category, Product, ProductCategory, Review
from api.serializers import (ProductSerializer, ReviewOfProductSerializer,
                             ReviewSerializer)
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class ProductSetPagination(PageNumberPagination):
    page_size = 20
    page_query_description = 'Inform the page. Starting with 1. Default: 1'
    page_size_query_param = 'limit'
    page_size_query_description = 'Limit per page, Default: 20.'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'rows': data, # originally 'results': data,
        })


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Return a list of products
    retrieve: Return a product by ID.
    """
    queryset = Product.objects.all().order_by('product_id')
    serializer_class = ProductSerializer
    pagination_class = ProductSetPagination
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'description')

    def _get_products_from_category_ids(self, category_ids):
        product_ids = ProductCategory.objects.filter(
            category_id__in=category_ids
        ).values_list("product_id", flat=True)

        return Product.objects.filter(product_id__in=product_ids)

    @action(methods=['GET'], detail=False, url_path='search', url_name='Search products')
    def search(self, request, *args, **kwargs):
        """        
        Search products
        """
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False, url_path='inCategory/(?P<category_id>[^/.]+)')
    def get_products_by_category(self, request, category_id):
        """
        Get a list of Products by Categories
        """

        products = self._get_products_from_category_ids([category_id])
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductSerializer(products, many=True)
        return Response({"rows": serializer.data})

    @action(methods=['GET'], detail=False, url_path='inDepartment/(?P<department_id>[^/.]+)')
    def get_products_by_department(self, request, department_id):
        """
        Get a list of Products of Departments
        """
        department_categories = Category.objects.filter(department_id=department_id)
        if not department_categories.exists():
            return errors.handle(errors.DEP_02)
        
        category_ids = department_categories.values_list('category_id', flat=True)

        products = self._get_products_from_category_ids(category_ids)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductSerializer(products, many=True)
        return Response({"rows": serializer.data})

    @action(methods=['GET'], detail=True, url_path='details')
    def details(self, request, pk):
        """
        Get details of a Product
        """
        # TODO: place the code here

    @action(methods=['GET'], detail=True, url_path='locations')
    def locations(self, request, pk):
        """
        Get locations of a Product
        """
        # TODO: place the code here


    @action(methods=['GET'], detail=True, url_path='reviews', url_name='List reviews')
    def reviews(self, request, pk):
        """
        Return a list of reviews
        """
        reviews = Review.objects.filter(product_id = pk)
        serializer = ReviewOfProductSerializer(reviews,many=True)
        return Response(serializer.data)

    @swagger_auto_schema(method='POST', request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'review': openapi.Schema(type=openapi.TYPE_STRING, description='Review Text of Product', required=['true']),
            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description='Rating of Product', required=['true']),
        }
    ))
    @action(methods=['POST'], detail=True, url_path='review', url_name='Create review')
    def review(self, request, pk):
        """
        Create a new review
        """
        data = request.data

        review_text = data.get("review")
        rating = data.get("rating")

        # TODO: get customer_id from authenticated user
        customer_id = data.get('customer_id',1)

        if review_text is None or rating is None:
            return errors.handle(errors.REV_01)

        # TODO: replace customer_id with authenticated user's customer_id
        new_review = Review.objects.create(
            customer_id=customer_id,
            product_id=pk,
            review=review_text,
            rating=rating,
            created_on=timezone.now()
        )

        serializer = ReviewSerializer(new_review)
        return Response(serializer.data, status=201)
