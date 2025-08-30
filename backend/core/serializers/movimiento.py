from core.models import MovimientoPedido
from rest_framework import serializers


class MovimientoPedidoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source="usuario.username", read_only=True)

    class Meta:
        model = MovimientoPedido
        fields = ["id", "estado", "comentario", "usuario_nombre", "fecha_moviminto"]
