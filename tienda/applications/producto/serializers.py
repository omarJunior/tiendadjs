
from rest_framework import serializers, pagination
from .models import Product, Colors

class PaginationSerializer(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 50

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ('__all__')

class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'man',
            'woman',
            'weight',
            'price_purchase',
            'price_sale',
            'main_image',
            'image1',
            'image2',
            'image3',
            'image4',
            'colors',
            'video',
            'stok',
            'num_sales',
            'user_created',
        ]


class ProductSerializerViewSet(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('__all__')


