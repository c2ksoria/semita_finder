from core.models import Producto, SemitaImagen, TipoSemita
from rest_framework import serializers


class TipoSemitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoSemita
        fields = ["id", "nombre"]


class SemitaImagenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemitaImagen
        fields = ["id", "imagen", "principal"]

    def create(self, validated_data):
        producto = self.context["producto"]

        validated_data["producto"] = producto

        # Si no vino "principal" o es False, pero no hay ninguna imagen previa
        if not validated_data.get("principal", False):
            if not producto.imagenes.exists():
                validated_data["principal"] = True

        if validated_data.get("principal", False):
            producto.imagenes.update(principal=False)

        return super().create(validated_data)


class ProductoSerializer(serializers.ModelSerializer):
    imagenes = SemitaImagenSerializer(many=True, read_only=True)
    tipo = TipoSemitaSerializer(read_only=True)
    tipo_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoSemita.objects.all(), source="tipo", write_only=True
    )

    class Meta:
        model = Producto
        fields = "__all__"
