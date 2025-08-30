from core.views.pedido import (
    CambiarEstadoPedidoAPIView,
    EstadoPedidoChoicesAPIView,
    MisPedidosAPIView,
    PedidoCreateAPIView,
    PedidoDetalleAPIView,
    PedidoRecibidoDetalleAPIView,
    PedidosRecibidosAPIView,
)
from django.urls import path

urlpatterns = [
    path("", PedidoCreateAPIView.as_view()),
    path("mis-pedidos/", MisPedidosAPIView.as_view()),
    path(
        "mis-pedidos/<int:pk>/", PedidoDetalleAPIView.as_view(), name="pedido-detalle"
    ),
    path(
        "pedidos-recibidos/",
        PedidosRecibidosAPIView.as_view(),
        name="pedidos-recibidos",
    ),
    path(
        "pedidos-recibidos/<int:pedido_id>/",
        PedidoRecibidoDetalleAPIView.as_view(),
        name="pedidos-recibidos-detalle",
    ),
    path(
        "<int:pedido_id>/cambiar-estado/",
        CambiarEstadoPedidoAPIView.as_view(),
        name="cambiar-estado-pedido",
    ),
    path("estados/", EstadoPedidoChoicesAPIView.as_view(), name="pedido-estados"),
]
