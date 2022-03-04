from rest_framework.routers import DefaultRouter

from .viewsets import ColorsViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"colors", ColorsViewSet, basename="colors")
router.register(r"product", ProductViewSet, basename="product")

urlpatterns = router.urls