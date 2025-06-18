from django.urls import path
from core.views.producto import MisProductosAPIView, ProductoDetalleAPIView, SemitaImagenUploadAPIView, SemitaImagenDeleteAPIView, TipoSemitaAPIView, ProductosPorComercioAPIView

urlpatterns = [
    path('', MisProductosAPIView.as_view(), name='mis-productos'),
    path('tiposemita/', TipoSemitaAPIView.as_view(), name='mis-productos-tipo'),
    path('comercio/<int:comercio_id>/', ProductosPorComercioAPIView.as_view(), name='producto-por-comercio'),
    path('mis-productos/<int:producto_id>', ProductoDetalleAPIView.as_view(), name='mis-productos-detalle'),
    path('mis-productos/<int:producto_id>/imagenes/', SemitaImagenUploadAPIView.as_view(), name='producto-subir-imagen'),
    path('mis-productos/<int:producto_id>/imagenes/<int:imagen_id>/',SemitaImagenDeleteAPIView.as_view(),name='producto-eliminar-imagen'),
]
