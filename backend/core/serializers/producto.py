from rest_framework import serializers
from core.models import TipoSemita, SemitaImagen, Producto

class TipoSemitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSemita
        fields = ['id', 'nombre']

class SemitaImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemitaImagen
        fields = ['id', 'imagen', 'principal']

class ProductoSerializer(serializers.ModelSerializer):
    imagenes = SemitaImagenSerializer(many=True, read_only=True)
    tipo = TipoSemitaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'tipo', 'precio', 'en_stock', 'activo', 'imagenes']