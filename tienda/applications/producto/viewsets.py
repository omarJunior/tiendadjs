from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Colors, Product

from .serializers import (
     PaginationSerializer,
     ColorSerializer, 
     ProductSerializer, 
     ProductSerializerViewSet,
)

class ColorsViewSet(viewsets.ModelViewSet):
    queryset = Colors.objects.all().order_by('id')
    serializer_class = ColorSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerViewSet
    pagination_class = PaginationSerializer

    """ Acciones que son opcionales en el modelViewSet """
    def perform_create(self, serializer):
        serializer.save(
            video = "https://youtu.be/h8a1gLl9C5A"
        )

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.productos_por_user(self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
