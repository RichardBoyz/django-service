import logging

from api import errors
from api.models import Attribute, AttributeValue, ProductAttribute
from api.serializers import (AttributeSerializer,
                             AttributeValueExtendedSerializer,
                             AttributeValueSerializer)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class AttributeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    list: Return a list of attributes
    retrieve: Return a attribute by ID.
    """
    queryset = Attribute.objects.all()
    serializer_class = AttributeSerializer

    @action(detail=False, url_path='values/<int:attribute_id>')
    def get_values_from_attribute(self, request, *args, **kwargs):
        """
        Get Values Attribute from Attribute ID
        """
        attribute_id = kwargs.get("attribute_id")
        values = AttributeValue.objects.filter(attribute_id=attribute_id)

        if not values.exists():
            return errors.handle(errors.ATTR_00)

        serializer = AttributeValueSerializer(values, many=True)
        return Response(serializer.data)

    @action(detail=False, url_path='inProduct/<int:product_id>')
    def get_attributes_from_product(self, request, *args, **kwargs):
        """
        Get all Attributes with Product ID
        """
        product_id = kwargs.get("product_id")
        product_attrs = ProductAttribute.objects.filter(product_id=product_id)

        if not product_attrs.exists():
            return errors.handle(errors.ATTR_01)
        
        value_ids = product_attrs.values_list('attribute_value_id', flat=True)
        attribute_values = AttributeValue.objects.filter(pk__in = value_ids)

        serializer = AttributeValueExtendedSerializer(attribute_values, many=True)
        return Response(serializer.data)
