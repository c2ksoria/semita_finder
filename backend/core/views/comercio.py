from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from core.models import Comercio
from core.serializers.comercio import ComercioSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from math import radians, cos, sin, asin, sqrt
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class ComercioListaAPIView(APIView):
    """
    Listado público de comercios activos
    """
    @swagger_auto_schema(
        operation_description="Listar comercios activos con opción de búsqueda por nombre, dirección o descripción.",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Texto de búsqueda (nombre, dirección o descripción)",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request):
        search = request.query_params.get('search')
        qs = Comercio.objects.filter(activo=True)

        if search:
            qs = qs.filter(
                Q(nombre__icontains=search) |
                Q(descripcion__icontains=search) |
                Q(direccion__icontains=search)
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

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c  # radio de la Tierra en km
    return km

class ComercioCercanoAPIView(APIView):
    """
    Lista comercios activos dentro de un radio desde lat/lng
    """

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('lat', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True, description="Latitud actual"),
            openapi.Parameter('lng', openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=True, description="Longitud actual"),
            openapi.Parameter(
    'radio',
    openapi.IN_QUERY,
    type=openapi.TYPE_NUMBER,
    required=False,
    description="Radio en km (default 0.5)",
    default=0.5,
    example=0.5
),
        ],
        operation_description="Buscar comercios cercanos a una ubicación dada."
    )
    def get(self, request):
        try:
            lat = float(request.query_params.get('lat'))
            lng = float(request.query_params.get('lng'))
        except (TypeError, ValueError):
            return Response({"detail": "lat y lng son requeridos y deben ser numéricos."}, status=400)

        radio = float(request.query_params.get('radio', 5))

        comercios = Comercio.objects.filter(activo=True)

        resultado = []
        for comercio in comercios:
            if comercio.latitud and comercio.longitud:
                distancia = calcular_distancia_km(lat, lng, comercio.latitud, comercio.longitud)
                if distancia <= radio:
                    data = ComercioSerializer(comercio).data
                    data["distancia_km"] = round(distancia, 2)
                    resultado.append(data)

        return Response(resultado, status=200)

class MisComerciosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Listar los comercios registrados por el usuario autenticado."
    )
    def get(self, request):
        comercios = Comercio.objects.filter(usuario=request.user)
        serializer = ComercioSerializer(comercios, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ComercioSerializer,
        operation_description="Crear un nuevo comercio vinculado al usuario autenticado."
    )
    def post(self, request):
        serializer = ComercioSerializer(data=request.data)
        if serializer.is_valid():
            comercio = serializer.save(usuario=request.user)
            return Response(ComercioSerializer(comercio).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class MisComercioDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=ComercioSerializer,
        operation_description="Editar parcialmente un comercio propio (PATCH)",
    )
    def patch(self, request, comercio_id):
        comercio = get_object_or_404(Comercio, pk=comercio_id)

        if comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para modificar este comercio.")

        serializer = ComercioSerializer(comercio, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
