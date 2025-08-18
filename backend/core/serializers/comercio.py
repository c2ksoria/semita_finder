from rest_framework import serializers
from core.models import Comercio, FranjaHorario, ComercioImagen
from core.serializers.producto import TipoSemitaSerializer, SemitaImagen, Producto
from core.serializers.comercio import FranjaHorario

class FranjaHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranjaHorario
        fields = ['id', 'dia', 'apertura', 'cierre']

class ComercioImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComercioImagen
        fields = ['id', 'imagen', 'principal']
        ref_name = 'ComercioImagenUpload'

    def create(self, validated_data):
        comercio = self.context['comercio']
        validated_data['comercio'] = comercio

        # Auto-principal si es la primera imagen
        if not validated_data.get('principal', False):
            if not comercio.imagenes.exists():
                validated_data['principal'] = True

        # Si viene como principal, desmarcar otras
        if validated_data.get('principal', False):
            comercio.imagenes.update(principal=False)

        return super().create(validated_data)

class ComercioSerializer(serializers.ModelSerializer):
    imagenes = ComercioImagenSerializer(many=True, read_only=True)
    horarios = FranjaHorarioSerializer(many=True, read_only=True)
    class Meta:
        model = Comercio
        fields = ['id', 'nombre', 'descripcion', 'direccion', 'latitud', 'longitud', 'activo', 'anio_inicio', 'mes_inicio', 'imagenes', 'telefono', 'horarios']

class ComercioDetalleSerializer(serializers.ModelSerializer):
    franjas_horarias = FranjaHorarioSerializer(many=True, read_only=True)

    class Meta:
        model = Comercio
        fields = '__all__'

class SemitaImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemitaImagen
        fields = ['id', 'imagen', 'principal']

class ProductoPublicoSerializer(serializers.ModelSerializer):
    tipo = TipoSemitaSerializer(read_only=True)
    imagenes = SemitaImagenSerializer(many=True, read_only=True)

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'tipo', 'imagenes']

class ComercioImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComercioImagen
        fields = ['id', 'imagen', 'principal']
        ref_name = 'ComercioImagenPublica'

class FranjaHorariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranjaHorario
        fields = ['id','dia','apertura', 'cierre']

class ComercioDetallePublicoSerializer(serializers.ModelSerializer):
    productos = ProductoPublicoSerializer(many=True, read_only=True,)
    imagenes = ComercioImagenSerializer(many=True, read_only=True)
    horarios = FranjaHorariaSerializer(many=True, read_only=True)

    class Meta:
        model = Comercio
        fields = [
            'id', 'nombre', 'descripcion', 'direccion',
            'latitud', 'longitud', 'activo', 'anio_inicio', 'mes_inicio',
            'imagenes', 'productos', 'horarios'
        ]