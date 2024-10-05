from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def sort_by_price(self, request):
        order = request.query_params.get('order', 'asc')
        products = self.get_queryset().order_by('price' if order == 'asc' else '-price')
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)