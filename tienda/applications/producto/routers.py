from rest_framework.routers import DefaultRouter

from .viewsets import ColorsViewSet

router = DefaultRouter()
router.register(r"colors", ColorsViewSet, basename="colors")

urlpatterns = router.urls