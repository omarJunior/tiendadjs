from rest_framework import viewsets

from .models import Colors

from .serializers import ColorSerializer

class ColorsViewSet(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Colors.objects.all()