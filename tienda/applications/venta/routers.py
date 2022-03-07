from rest_framework.routers import DefaultRouter

from .viewsets import VentasViewSets

router = DefaultRouter()
router.register(r'ventas', VentasViewSets, basename='ventas')

urlpatterns = router.urls