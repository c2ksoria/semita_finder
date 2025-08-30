from core.models import Comercio, Producto, SemitaImagen, TipoSemita
from core.serializers.producto import (
    ProductoSerializer,
    SemitaImagenSerializer,
    TipoSemitaSerializer,
)
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class MisProductosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=(
            "Listar los productos de los comercios del usuario autenticado."
        )
    )
    def get(self, request):
        productos = Producto.objects.filter(comercio__usuario=request.user)
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductoSerializer,
        operation_description=(
            "Crear un producto asociado a un comercio del usuario autenticado."
        ),
    )
    def post(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            comercio = serializer.validated_data.get("comercio")

            if comercio.usuario != request.user:
                return Response(
                    {
                        "detail": (
                            "No tenés permiso para cargar "
                            "productos en este comercio."
                        )
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            producto = serializer.save()
            return Response(
                ProductoSerializer(producto).data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Obtener producto por id")
    def get(self, request, producto_id):
        try:
            producto = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            return Response(
                {"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Verifica que el producto pertenezca al usuario autenticado
        if producto.comercio.usuario != request.user:
            return Response(
                {"error": "No autorizado"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductoSerializer(producto)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ProductoSerializer,
        operation_description=(
            "Editar parcialmente un producto del usuario autenticado."
        ),
    )
    def patch(self, request, producto_id):
        producto = get_object_or_404(Producto, pk=producto_id)

        if producto.comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para modificar este producto.")

        serializer = ProductoSerializer(producto, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Eliminar un producto del usuario autenticado.",
        responses={204: "Producto eliminado correctamente"},
    )
    def delete(self, request, producto_id):
        producto = get_object_or_404(Producto, pk=producto_id)

        if producto.comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para eliminar este producto.")

        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SemitaImagenUploadAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Subir una imagen para un producto propio",
        request_body=SemitaImagenSerializer,
        responses={201: SemitaImagenSerializer},
    )
    def post(self, request, producto_id):
        producto = get_object_or_404(Producto, pk=producto_id)

        if producto.comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para modificar este producto.")

        data = request.data.copy()
        data["producto"] = producto.id

        # serializer = SemitaImagenSerializer(data=data)
        serializer = SemitaImagenSerializer(
            data=request.data, context={"producto": producto}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SemitaImagenListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description=(
            "Listar todas las imágenes de un producto del usuario autenticado."
        ),
        manual_parameters=[
            openapi.Parameter(
                "producto_id",
                openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                required=True,
                description="ID del producto",
            ),
        ],
        responses={200: SemitaImagenSerializer(many=True)},
    )
    def get(self, request, producto_id):
        producto = get_object_or_404(Producto, pk=producto_id)

        if producto.comercio.usuario != request.user:
            raise PermissionDenied(
                "No tenés permiso para ver las imágenes de este producto."
            )

        imagenes = SemitaImagen.objects.filter(producto=producto)
        serializer = SemitaImagenSerializer(imagenes, many=True)
        return Response(serializer.data)


class SemitaImagenDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Eliminar una imagen de un producto propio.",
        manual_parameters=[
            openapi.Parameter(
                "producto_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True
            ),
            openapi.Parameter(
                "imagen_id", openapi.IN_PATH, type=openapi.TYPE_INTEGER, required=True
            ),
        ],
        responses={204: "Imagen eliminada correctamente"},
    )
    def delete(self, request, producto_id, imagen_id):
        producto = get_object_or_404(Producto, pk=producto_id)

        if producto.comercio.usuario != request.user:
            raise PermissionDenied("No tenés permiso para acceder a este producto.")

        imagen = get_object_or_404(SemitaImagen, pk=imagen_id, producto=producto)
        imagen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TipoSemitaAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description="Listar los tipos de semitas")
    def get(self, request):
        tipos = TipoSemita.objects.all()
        serializer = TipoSemitaSerializer(tipos, many=True)
        return Response(serializer.data)


class ProductosPorComercioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, comercio_id):
        try:
            comercio = Comercio.objects.get(id=comercio_id, activo=True)
        except Comercio.DoesNotExist:
            return Response(
                {"error": "Comercio no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        productos = Producto.objects.filter(
            comercio=comercio, activo=True, en_stock=True
        )
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
