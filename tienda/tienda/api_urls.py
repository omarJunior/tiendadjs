from django.urls import path, include

urlpatterns = [
    path('', include('applications.producto.routers')),
]