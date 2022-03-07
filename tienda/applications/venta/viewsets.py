from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

from applications.producto.models import Product
from .models import Sale, SaleDetail
from .serializers import ProcessoVentaSerializer2, VentaReporteSerializer

#no esta vinculado estrictamente a un modelo, 
# y las acciones como (list, create, retrieve, updated etc)
#  se deben crear manualmente porque por defecto no las reconoce
class VentasViewSets(viewsets.ViewSet):
    
    authentication_classes = (TokenAuthentication, )
    queryset = Sale.objects.all()

    def get_permissions(self):
        if (self.action == 'list' or self.action == 'retrieve'):
            permission_classes = (AllowAny, )    
        else:
            permission_classes = (IsAuthenticated, )
        
        return [permission() for permission in permission_classes]
        
            
    def list(self, request, *args, **kwargs):
        queryset = Sale.objects.all().order_by('-id')
        serializer = VentaReporteSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #tomamos toda la data del serializador
        serializer = ProcessoVentaSerializer2(data = request.data)
        serializer.is_valid(raise_exception=True)

        venta = Sale.objects.create(
            date_sale = timezone.now(), 
            amount = 0,
            count = 0,
            type_invoce = serializer.validated_data['type_invoce'],
            type_payment = serializer.validated_data['type_payment'],
            adreese_send = serializer.validated_data['adreese_send'],
            user = self.request.user,
        )
        #variables para la venta
        amount = 0
        count = 0

        productos = Product.objects.filter(id__in = serializer.validated_data['productos'])
        cantidades = serializer.validated_data['cantidades']
        
        ventas_detalles = []
        for producto, cantidad in zip(productos, cantidades): #recorremos dos listas al mismo tiempo
            venta_detalle = SaleDetail(
                sale = venta,
                product = producto,
                count = cantidad,
                price_purchase = producto.price_purchase,
                price_sale = producto.price_sale,
            )
            amount = amount + producto.price_sale * cantidad
            count = count + cantidad
            ventas_detalles.append(venta_detalle)

        venta.amount = amount
        venta.count = count
        venta.save()

        #crea objetos que estan almacenados en una lista de python para guardarlos en la base de datos 
        SaleDetail.objects.bulk_create(ventas_detalles)

        return Response({'msj': 'Venta exitosa'})

    #obtener un dato en especifico
    def retrieve(self, request, pk=None):
        venta = get_object_or_404(Sale.objects.all(), pk=pk)
        serializer = VentaReporteSerializer(venta)
        return Response(serializer.data)
