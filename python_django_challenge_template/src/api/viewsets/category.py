from api.models import Category, ProductCategory
from api.serializers import CategorySerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /categories
    GET /categories/<id>
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, url_path='inProduct/(?P<product_id>[^/.]+)', methods=['get'])
    def get_category_in_product(self, request, product_id=None):
        product_category = ProductCategory.objects.filter(product_id=product_id).first()
        if not product_category:
            return Response({"detail": "Product not found"}, status=404)
        category = Category.objects.filter(category_id=product_category.category_id).first()
        if not category:
            return Response({"detail": "Category not found"}, status=404)
        serializer = self.get_serializer(category)
        response_data =serializer.data
        del response_data['description']
        return Response(response_data)

    @action(detail=False, url_path='inDepartment/(?P<department_id>[^/.]+)', methods=['get'])
    def get_categories_in_department(self, request, department_id=None):
        categories = Category.objects.filter(department_id=department_id)
        serializer = self.get_serializer(categories, many=True)
        return Response({"rows": serializer.data})