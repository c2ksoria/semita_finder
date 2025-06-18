from rest_framework import serializers
from core.models import Pedido, ItemPedido, MovimientoPedido, Producto, Comercio
from core.serializers.producto import ProductoSerializer
from core.serializers.movimiento import MovimientoPedidoSerializer
from django.db import transaction
from django.utils import timezone
from ..utils.constants import ESTADOS_PEDIDO

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
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        pedido = Pedido.objects.create(cliente=self.context['request'].user, **validated_data)

        for item_data in items_data:
            producto = item_data['producto']
            cantidad = item_data['cantidad']
            precio = producto.precio * cantidad
            ItemPedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, precio_item=precio)

        MovimientoPedido.objects.create(pedido=pedido, estado='registrado', observacion='Pedido creado automáticamente')

        return pedido
    
class ItemPedidoCrearSerializer(serializers.Serializer):
    producto = serializers.IntegerField()
    cantidad = serializers.IntegerField(min_value=1)

class PedidoCrearSerializer(serializers.Serializer):
    comercio = serializers.IntegerField()
    fecha_hora_retiro = serializers.DateTimeField()
    comentario = serializers.CharField(required=False, allow_blank=True)
    items = ItemPedidoCrearSerializer(many=True)

    def validate_comercio(self, value):
        usuario = self.context['request'].user
        try:
            comercio = Comercio.objects.get(id=value)
        except Comercio.DoesNotExist:
            raise serializers.ValidationError("Comercio no encontrado")

        if not comercio.activo:
            raise serializers.ValidationError("El comercio no está activo")
        return value

    @transaction.atomic
    def create(self, validated_data):
        usuario = self.context['request'].user
        comercio_id = validated_data['comercio']
        items_data = validated_data['items']

        comercio = Comercio.objects.get(id=comercio_id)

        pedido = Pedido.objects.create(
            cliente=usuario,
            comercio=comercio,
            fecha_hora_retiro=validated_data['fecha_hora_retiro'],
            comentario=validated_data.get('comentario', ''),
            estado='registrado'  # estado inicial, opcional si default
        )

        for item in items_data:
            producto = Producto.objects.get(id=item['producto'], comercio=comercio)
            cantidad = item['cantidad']
            precio_unitario = producto.precio
            ItemPedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad,
                precio_item=precio_unitario * cantidad
            )

        MovimientoPedido.objects.create(
            pedido=pedido,
            estado='registrado',
            comentario='Pedido creado',
            # fecha=timezone.now()
        )

        return pedido
    
    def validate_fecha_hora_retiro(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("La fecha y hora de retiro debe ser futura.")
        return value

class PedidoResumenSerializer(serializers.ModelSerializer):
    comercio_nombre = serializers.CharField(source='comercio.nombre', read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.username', read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = ['id', 'comercio', 'cliente_nombre', 'comercio_nombre','estado', 'fecha_hora_retiro', 'creado_en', 'total']

    def get_total(self, obj):
        return obj.calcular_total()
    
class ItemPedidoDetalleSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    tipo_nombre = serializers.CharField(source='producto.tipo.nombre', read_only=True)
    
    class Meta:
        model = ItemPedido
        fields = ['id', 'producto', 'producto_nombre', 'tipo_nombre', 'cantidad', 'precio_item']

class PedidoDetalleSerializer(serializers.ModelSerializer):
    comercio_nombre = serializers.CharField(source='comercio.nombre', read_only=True)
    items = ItemPedidoDetalleSerializer(many=True, read_only=True)
    movimientos = MovimientoPedidoSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Pedido
        fields = [
            'id',
            'comercio',
            'comercio_nombre',
            'estado',
            'fecha_hora_retiro',
            'comentario',
            'creado_en',
            'items',
            'movimientos',
            'total'
        ]

    def get_total(self, obj):
        return obj.calcular_total()

class MovimientoPedidoCreateSerializer(serializers.Serializer):
    estado = serializers.ChoiceField(choices=ESTADOS_PEDIDO)
    comentario = serializers.CharField(required=False, allow_blank=True)

class ChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()