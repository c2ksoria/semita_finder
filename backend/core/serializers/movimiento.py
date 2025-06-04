from rest_framework import serializers
from core.models import MovimientoPedido

class MovimientoPedidoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = MovimientoPedido
        fields = ['id', 'estado', 'comentario', 'usuario', 'fecha_moviminto']
