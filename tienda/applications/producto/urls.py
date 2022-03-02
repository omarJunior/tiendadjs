
from django.urls import path

from .views import ListProductUser, ListProductStok, ListProductGenero, FiltrarProductos

app_name = "producto_app"

urlpatterns = [
    path('api/product/por-usuario/', ListProductUser.as_view()),  
    path('api/product/por-stock/', ListProductStok.as_view()),
    path('api/product/por-genero/<gender>/', ListProductGenero.as_view()),
    path('api/product/filtrar/', FiltrarProductos.as_view()),
]