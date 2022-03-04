from django.utils import timezone
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.generics import (
	ListAPIView,
	CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .models import Sale, SaleDetail
from applications.producto.models import Product

from .serializers import (
	VentaReporteSerializer, 
	DetalleVentaProductoSerializer, 
	ProcessoVentaSerializer,
	ProcessoVentaSerializer2
)

# Create your views here.
class ReporteVentaList(ListAPIView):
	serializer_class = VentaReporteSerializer

	def get_queryset(self):
		venta = Sale.objects.all()
		return venta


class DetailVentaList(ListAPIView):
	serializer_class = DetalleVentaProductoSerializer

	def get_queryset(self):
		detalle = SaleDetail.objects.all()
		return detalle


class RegistrarVenta(CreateAPIView):
	#Registrar venta
	authentication_classes = (TokenAuthentication, )
	permission_classes = [IsAuthenticated,]
	serializer_class = ProcessoVentaSerializer

	def create(self, request, *args, **kwargs):
		#tomamos toda la data del serializador
		serializer = ProcessoVentaSerializer(data = request.data)
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

		#recuperamos los productos de las ventas que es un arreglo de objetos
		productos = serializer.validated_data['productos']
		
		ventas_detalles = []
		for producto in productos:
			try:
				prod = Product.objects.get(pk = producto['pk'])
				venta_detalle = SaleDetail(
					sale = venta,
					product = prod,
					count = producto['count'],
					price_purchase = prod.price_purchase,
					price_sale = prod.price_sale,
				)
				amount = amount + prod.price_sale * producto['count']
				count = count + producto['count']
				ventas_detalles.append(venta_detalle)
			except:
				pass

		venta.amount = amount
		venta.count = count
		venta.save()

		#crea objetos que estan almacenados en una lista de python para guardarlos en la base de datos 
		SaleDetail.objects.bulk_create(ventas_detalles)

		return Response({'msj': 'Venta exitosa'})


#usando ListField Serializer
class RegistrarVenta2(CreateAPIView):
	#Registrar venta
	authentication_classes = (TokenAuthentication, )
	permission_classes = [IsAuthenticated,]
	serializer_class = ProcessoVentaSerializer2

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
