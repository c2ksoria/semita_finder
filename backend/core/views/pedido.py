from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions

from core.models import Pedido, MovimientoPedido
from core.serializers.pedido import PedidoSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from core.serializers.pedido import PedidoCrearSerializer, PedidoResumenSerializer, PedidoDetalleSerializer, MovimientoPedidoCreateSerializer, ChoiceSerializer
from drf_yasg import openapi
from core.utils.constants import ESTADOS_PEDIDO

class CrearPedidoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=PedidoSerializer)
    def post(self, request):
        serializer = PedidoSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        pedido = serializer.save()
        return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)
    
class MisPedidosAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(operation_description="Obtener los pedidos realizados por un cliente")
    def get(self, request):
        pedidos = Pedido.objects.filter(cliente=request.user)
        serializer = PedidoResumenSerializer(pedidos, many=True)
        return Response(serializer.data)

class PedidosRecibidosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pedidos = Pedido.objects.filter(comercio__usuario=request.user)
        serializer = PedidoSerializer(pedidos, many=True)
        return Response(serializer.data)

# class CambiarEstadoPedidoAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     class InputSerializer(serializers.Serializer):
#         estado = serializers.ChoiceField(choices=ESTADOS_PEDIDO)
#         observacion = serializers.CharField(allow_blank=True, required=False)

#     @swagger_auto_schema(request_body=InputSerializer)
#     def patch(self, request, pedido_id):
#         pedido = get_object_or_404(Pedido, pk=pedido_id)

#         # Solo puede cambiar estado el dueño del comercio
#         if pedido.comercio.usuario != request.user:
#             raise PermissionDenied("No tenés permiso para modificar este pedido.")

#         serializer = self.InputSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         nuevo_estado = serializer.validated_data['estado']
#         observacion = serializer.validated_data.get('observacion', '')

#         pedido.estado = nuevo_estado
#         pedido.save()

#         MovimientoPedido.objects.create(
#             pedido=pedido,
#             estado=nuevo_estado,
#             observacion=observacion
#         )

#         return Response({"detail": f"Estado actualizado a {nuevo_estado}."})

class PedidoCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=PedidoCrearSerializer)
    def post(self, request):
        serializer = PedidoCrearSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pedido = serializer.save()
            return Response({'id': pedido.id, 'mensaje': 'Pedido creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PedidoDetalleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk, cliente=request.user)
        except Pedido.DoesNotExist:
            return Response({'detail': 'Pedido no encontrado o no autorizado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PedidoDetalleSerializer(pedido)
        return Response(serializer.data)

class PedidosRecibidosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Obtener IDs de los comercios que pertenecen al usuario
        comercio_ids = request.user.comercios.values_list('id', flat=True)

        # Buscar pedidos hechos a esos comercios
        pedidos = Pedido.objects.filter(comercio_id__in=comercio_ids).order_by('-creado_en')

        serializer = PedidoResumenSerializer(pedidos, many=True)
        return Response(serializer.data)

class PedidoRecibidoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pedido_id):
        try:
            pedido = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            return Response({'detail': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Validar que el comercio sea del usuario actual
        if pedido.comercio.usuario != request.user:
            return Response({'detail': 'No tenés permiso para ver este pedido'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PedidoDetalleSerializer(pedido)
        return Response(serializer.data)

class CambiarEstadoPedidoAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['estado'],
        properties={
            'estado': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Nuevo estado del pedido (registrado, confirmado, cancelado, entregado)',
                enum=['registrado', 'confirmado', 'cancelado', 'entregado']
            ),
            'comentario': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='Comentario opcional sobre el cambio de estado',
                default=''
            ),
        }
    ),
    responses={
        200: openapi.Response(description='Estado actualizado correctamente'),
        400: 'Error de validación',
        403: 'No autorizado',
        404: 'Pedido no encontrado'
    }
    )
    def post(self, request, pedido_id):
        try:
            pedido = Pedido.objects.get(id=pedido_id)
        except Pedido.DoesNotExist:
            return Response({'detail': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Validar que el pedido pertenezca a un comercio del usuario autenticado
        if pedido.comercio.usuario != request.user:
            return Response({'detail': 'No tenés permiso para modificar este pedido'}, status=status.HTTP_403_FORBIDDEN)

         # ✅ Nueva validación: no permitir modificar si ya fue entregado
        if pedido.estado == 'entregado':
            return Response(
                {'detail': 'No se puede modificar un pedido que ya fue entregado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MovimientoPedidoCreateSerializer(data=request.data)
        if serializer.is_valid():
            nuevo_estado = serializer.validated_data['estado']
            comentario = serializer.validated_data.get('comentario', '')

            # Actualizar el estado actual del pedido
            pedido.estado = nuevo_estado
            pedido.save()

            # Registrar el movimiento
            MovimientoPedido.objects.create(
                pedido=pedido,
                usuario=request.user,
                estado=nuevo_estado,
                comentario=comentario
            )

            return Response({'detail': 'Estado actualizado'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EstadoPedidoChoicesAPIView(APIView):
    @swagger_auto_schema(operation_description="Obtener listado de los estados posibles de un pedido")

    def get(self, request):
        data = [{"value": val, "label": label} for val, label in ESTADOS_PEDIDO]
        serializer = ChoiceSerializer(data, many=True)
        return Response(serializer.data)
