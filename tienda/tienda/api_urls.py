from django.urls import path, include

urlpatterns = [
    path('app_producto/', include('applications.producto.routers')),
    path('app_venta/', include('applications.venta.routers')),
]