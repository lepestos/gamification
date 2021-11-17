from rest_framework import viewsets

from calculator.models.product import Product
from calculator.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.exclude(name='mock')
