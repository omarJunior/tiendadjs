from django.urls import path, include

from .views import ReporteVentaList, DetailVentaList

app_name = "venta_app"

urlpatterns = [
	path('api/venta/reporte/', ReporteVentaList.as_view()),
	path('api/venta/detail/', DetailVentaList.as_view()),

]