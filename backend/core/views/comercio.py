from math import asin, cos, radians, sin, sqrt

from core.models import Comercio, ComercioImagen, FranjaHorario
from core.serializers.comercio import (
    ComercioDetallePublicoSerializer,
    ComercioImagenSerializer,
    ComercioSerializer,
    FranjaHorariaSerializer,
)
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ComercioListaAPIView(APIView):
    """
    Listado público de comercios activos
    """

    @swagger_auto_schema(
        operation_description=(
            "Listar comercios activos con opción"
            " de búsqueda por nombre, dirección o descripción."
        ),
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                description="Texto de búsqueda (nombre, dirección o descripción)",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def get(self, request):
        search = request.query_params.get("search")
        qs = Comercio.objects.filter(activo=True)

        if search:
            qs = qs.filter(
                Q(nombre__icontains=search)
                | Q(descripcion__icontains=search)
                | Q(direccion__icontains=search)
            )

        serializer = ComercioSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def calcular_distancia_km(lat1, lon1, lat2, lon2):
    """
    Calcula distancia entre dos coordenadas (Haversine).
    """
    # convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c  # radio de la Tierra en km
    return km


class ComercioCercanoAPIView(APIView):
    """
    Lista comercios activos dentro de un radio desde lat/lng
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "lat",
                openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                required=True,
                description="Latitud actual",
            ),
            openapi.Parameter(
                "lng",
                openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                required=True,
                description="Longitud actual",
            ),
            openapi.Parameter(
                "radio",
                openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                required=False,
                description="Radio en km (default 0.5)",
                default=0.5,
                example=0.5,
            ),
        ],
        operation_description="Buscar comercios cercanos a una ubicación dada.",
    )
    def get(self, request):
        try:
            lat = float(request.query_params.get("lat"))
            lng = float(request.query_params.get("lng"))
        except (TypeError, ValueError):
            return Response(
                {"detail": "lat y lng son requeridos y deben ser numéricos."},
                status=400,
            )

        radio = float(request.query_params.get("radio", 5))

        comercios = Comercio.objects.filter(activo=True)

        resultado = []
        for comercio in comercios:
            if comercio.latitud and comercio.longitud:
                distancia = calcular_distancia_km(
                    lat, lng, comercio.latitud, comercio.longitud
                )
                if distancia <= radio:
                    data = ComercioSerializer(comercio).data
                    data["distancia_km"] = round(distancia, 2)
                    resultado.append(data)

        return Response(resultado, status=200)


class MisComerciosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     comercios = Comercio.objects.filter(usuario=request.user)
    #     serializer = ComercioSerializer(comercios, many=True)
    #     return Response(serializer.data)

    @swagger_auto_schema(
        operation_description=(
            "Listar los comercios registrados por el usuario autenticado."
        )
    )
    def get(self, request):
        comercios = Comercio.objects.filter(usuario=request.user)
        serializer = ComercioSerializer(comercios, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ComercioSerializer,
        operation_description=(
            "Crear un nuevo comercio vinculado al usuario autenticado."
        ),
    )
    def post(self, request):
        serializer = ComercioSerializer(data=request.data)
        if serializer.is_valid():
            comercio = serializer.save(usuario=request.user)
            return Response(
                ComercioSerializer(comercio).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MisComercioDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=(
            "Listar los comercios registrados por el usuario autenticado."
        )
    )
    def get(self, request, pk=None):
        if pk:
            try:
                comercio = Comercio.objects.get(pk=pk, usuario=request.user)
                serializer = ComercioSerializer(comercio)
                return Response(serializer.data)
            except Comercio.DoesNotExist:
                return Response(
                    {"error": "Comercio no encontrado"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            comercios = Comercio.objects.filter(usuario=request.user)
            serializer = ComercioSerializer(comercios, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ComercioSerializer,
        operation_description="Editar parcialmente un comercio propio (PATCH)",
    )
    def patch(self, request, pk):
        try:
            comercio = Comercio.objects.get(pk=pk, usuario=request.user)
        except Comercio.DoesNotExist:
            return Response(
                {"error": "Comercio no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ComercioSerializer(comercio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comercio_id):
        comercio = get_object_or_404(Comercio, pk=comercio_id)

        if comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para eliminar este comercio.")

        comercio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ComercioImagenUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Subir una imagen para un comercio propio.",
        request_body=ComercioImagenSerializer,
        responses={201: ComercioImagenSerializer},
    )
    def post(self, request, comercio_id):
        comercio = get_object_or_404(Comercio, pk=comercio_id)

        if comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para modificar este comercio.")

        serializer = ComercioImagenSerializer(
            data=request.data, context={"comercio": comercio}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComercioImagenListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Listar imágenes de un comercio propio.",
        responses={200: ComercioImagenSerializer(many=True)},
    )
    def get(self, request, comercio_id):
        comercio = get_object_or_404(Comercio, pk=comercio_id)

        if comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para acceder a este comercio.")

        imagenes = comercio.imagenes.all()
        serializer = ComercioImagenSerializer(imagenes, many=True)
        return Response(serializer.data)


class ComercioImagenDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Eliminar una imagen de un comercio propio.",
        responses={204: "Imagen eliminada correctamente"},
    )
    def delete(self, request, comercio_id, imagen_id):
        comercio = get_object_or_404(Comercio, pk=comercio_id)

        if comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para acceder a este comercio.")

        imagen = get_object_or_404(ComercioImagen, pk=imagen_id, comercio=comercio)
        imagen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ComercioDetallePublicoAPIView(APIView):
    def get(self, request, comercio_id):
        try:
            comercio = Comercio.objects.get(id=comercio_id, activo=True)
        except Comercio.DoesNotExist:
            return Response(
                {"detail": "Comercio no encontrado o inactivo"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ComercioDetallePublicoSerializer(comercio)
        return Response(serializer.data)


class HorariosComerciosAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Obtener Horario de un comercio por id.",
    )
    def get(self, request, comercio_id):
        try:
            comercio = Comercio.objects.get(id=comercio_id)
        except Comercio.DoesNotExist:
            return Response(
                {"detail": "Comercio no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        franjas = FranjaHorario.objects.filter(comercio=comercio).order_by(
            "dia", "apertura"
        )
        serializer = FranjaHorariaSerializer(franjas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FranjaHorarioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Obtener Horarios de un comercio por id con permisos.",
    )
    def get(self, request, comercio_id):
        try:
            comercio = Comercio.objects.get(id=comercio_id, usuario=request.user)
        except Comercio.DoesNotExist:
            return Response({"detail": "No autorizado"}, status=403)

        franjas = FranjaHorario.objects.filter(comercio=comercio)
        serializer = FranjaHorariaSerializer(franjas, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Guardar Horarios de un comercio por id con permisos.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),
    )
    def post(self, request, comercio_id):
        try:
            comercio = Comercio.objects.get(id=comercio_id, usuario=request.user)
        except Comercio.DoesNotExist:
            return Response({"detail": "No autorizado"}, status=403)

        # Reemplaza todas las franjas horarias actuales
        FranjaHorario.objects.filter(comercio=comercio).delete()

        serializer = FranjaHorariaSerializer(data=request.data, many=True)
        if serializer.is_valid():
            for franja in serializer.validated_data:
                FranjaHorario.objects.create(comercio=comercio, **franja)
            return Response({"detail": "Horarios actualizados correctamente"})
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Eliminar Horarios de un comercio por id con permisos.",
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),
    )
    def delete(self, request, comercio_id):
        franja_id = request.data.get("franja_id")
        if not franja_id:
            return Response({"detail": "Se requiere franja_id"}, status=400)

        try:
            franja = FranjaHorario.objects.get(
                id=franja_id, comercio__usuario=request.user
            )
            franja.delete()
            return Response({"detail": "Franja eliminada"})
        except FranjaHorario.DoesNotExist:
            return Response(
                {"detail": "Franja no encontrada o no autorizada"}, status=404
            )
