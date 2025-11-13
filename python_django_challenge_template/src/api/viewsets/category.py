from api.models import Category
from api.serializers import CategorySerializer
from rest_framework import viewsets


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /categories
    GET /categories/<id>
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer