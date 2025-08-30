# core/views/choices_views.py

from core.serializers.utils import ChoiceSerializer
from core.utils.constants import ESTADOS_PEDIDO
from rest_framework.response import Response
from rest_framework.views import APIView


class EstadoPedidoChoicesAPIView(APIView):
    def get(self, request):
        data = [{"value": val, "label": label} for val, label in ESTADOS_PEDIDO]
        serializer = ChoiceSerializer(data, many=True)
        return Response(serializer.data)
