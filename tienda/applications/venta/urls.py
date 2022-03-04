from django.urls import path, include

from .views import (
	ReporteVentaList, 
	DetailVentaList, 
	RegistrarVenta,
	RegistrarVenta2,
)

app_name = "venta_app"

urlpatterns = [
	path('api/venta/reporte/', ReporteVentaList.as_view(), name="venta-reporte"),
	path('api/venta/detail/', DetailVentaList.as_view(), name="venta-detail"),
	path('api/venta/create/', RegistrarVenta.as_view(), name="venta-register"),
	path('api/venta/add/', RegistrarVenta.as_view(), name="venta-add"),
]