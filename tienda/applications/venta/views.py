from django.shortcuts import render
from rest_framework.generics import ListAPIView

from .models import Sale, SaleDetail
from .serializers import VentaReporteSerializer, DetalleVentaProductoSerializer


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



