from rest_framework import serializers
from core.models import Comercio, FranjaHorario

class FranjaHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranjaHorario
        fields = ['id', 'dia', 'apertura', 'cierre']

class ComercioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comercio
        fields = ['id', 'nombre', 'descripcion', 'direccion', 'latitud', 'longitud', 'activo', 'anio_inicio', 'mes_inicio']

class ComercioDetalleSerializer(serializers.ModelSerializer):
    franjas_horarias = FranjaHorarioSerializer(many=True, read_only=True)

    class Meta:
        model = Comercio
        fields = '__all__'
