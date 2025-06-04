from django.urls import path
from core.views.comercio import ComercioListaAPIView, ComercioCercanoAPIView, MisComerciosAPIView, MisComercioDetalleAPIView


urlpatterns = [
    path('', ComercioListaAPIView.as_view(), name='comercio'),
    path('cercanos/', ComercioCercanoAPIView.as_view(), name='comercio-cercanos'),
    path('mis-comercios/', MisComerciosAPIView.as_view(), name='mis-comercios'),
    path('mis-comercios/<int:comercio_id>/', MisComercioDetalleAPIView.as_view(), name='mis-comercio-detalle'),
]

