from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .serializers import ProductSerializer
from .models import Product

# Create your views here.

class ListProductUser(ListAPIView):
    serializer_class = ProductSerializer
    #necesita token por las cabeceras
    authentication_classes = (TokenAuthentication, )
    #necesita estar authenticado
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user
        print(usuario)
        resp = Product.objects.productos_por_user(usuario)
        return resp

class ListProductStok(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        resp = Product.objects.productos_con_stock()
        return resp

class ListProductGenero(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        gender = self.kwargs['gender']
        resp = Product.objects.productos_por_genero(gender)
        return resp

class FiltrarProductos(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        #example = parametro get ?man = ""
        varon = self.request.query_params.get('man', None)
        mujer = self.request.query_params.get('woman', None)
        nombre = self.request.query_params.get('name', None)
        print("**************************")
        print(varon, mujer, nombre)
        return []