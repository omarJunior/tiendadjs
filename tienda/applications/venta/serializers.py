from rest_framework import serializers

from .models import Sale, SaleDetail

class VentaReporteSerializer(serializers.ModelSerializer):
	productos = serializers.SerializerMethodField()

	class Meta:
		model = Sale
		fields = ['id',
			'date_sale', 
			'amount', 
			'count', 
			'type_invoce', 
			'cancelado', 
			'type_payment', 
			'state' , 
			'adreese_send', 
			'anulate', 
			'user',
			'productos'
			]

	def get_productos(self, obj):
		query = SaleDetail.objects.productos_por_venta(obj.id)
		productos_serializado = DetalleVentaProductoSerializer(query, many=True).data
		return productos_serializado


class DetalleVentaProductoSerializer(serializers.ModelSerializer):

	class Meta:
		model = SaleDetail
		fields = ['id',
			'sale',
			'product',
			'count',
			'price_purchase',
			'price_sale',
			'anulate'
		]

class ProductDetailSerializer(serializers.Serializer):
	pk = serializers.IntegerField()
	count = serializers.IntegerField()

#arreglo (ListField)
class ArrayIntegerSerializer(serializers.ListField):
	child = serializers.IntegerField()
	
class ProcessoVentaSerializer(serializers.Serializer):
	type_invoce = serializers.CharField()
	type_payment = serializers.CharField()
	adreese_send = serializers.CharField()
	productos = ProductDetailSerializer(many=True)


#listFieldSerializer
class ProcessoVentaSerializer2(serializers.Serializer):
	type_invoce = serializers.CharField()
	type_payment = serializers.CharField()
	adreese_send = serializers.CharField()
	productos = ArrayIntegerSerializer()
	cantidades = ArrayIntegerSerializer()

	#captura todos los campos del serializer como un diccionario
	#tipo de pago
	def validate(self, data):
		if data['type_payment'] != '0' and data['type_payment'] != '1' and data['type_payment'] != '2':
			raise serializers.ValidationError('Ingrese un tipo de pago correcto')
		return data

	#validacion de los serializers en un campo especifico
	#tipo de factura
	def validate_type_invoce(self, value):
		if value != '0' and value != '3' and value != '4':
			raise serializers.ValidationError('Ingrese un valor correcto')
		return value