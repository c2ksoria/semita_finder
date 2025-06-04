from rest_framework import serializers
from core.models import Pedido, ItemPedido
from core.serializers.producto import ProductoSerializer

class ItemPedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = ItemPedido
        fields = ['id', 'producto', 'cantidad', 'precio_item']

class PedidoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'comercio', 'fecha_hora_retiro', 'comentario', 'estado', 'creado_en', 'items', 'total']
        read_only_fields = ['cliente', 'estado', 'creado_en']

    def get_total(self, obj):
        return obj.calcular_total()
