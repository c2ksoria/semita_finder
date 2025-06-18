from django.urls import path
from core.views.comercio import ComercioListaAPIView, ComercioCercanoAPIView, MisComerciosAPIView, MisComercioDetalleAPIView, ComercioImagenUploadAPIView, ComercioImagenListAPIView, ComercioImagenDeleteAPIView, ComercioDetallePublicoAPIView, HorariosComerciosAPIView, FranjaHorarioAPIView

urlpatterns = [
    path('', ComercioListaAPIView.as_view(), name='comercio'),
    path('cercanos/', ComercioCercanoAPIView.as_view(), name='comercio-cercanos'),
    path('<int:comercio_id>/', ComercioDetallePublicoAPIView.as_view(), name='comercio-detalle-publico'),
    path('mis-comercios/', MisComerciosAPIView.as_view(), name='mis-comercios'),
    path('mis-comercios/<int:pk>/', MisComercioDetalleAPIView.as_view()),
    path('mis-comercios/<int:comercio_id>/', MisComercioDetalleAPIView.as_view(), name='mis-comercio-detalle'),
    path('mis-comercios/<int:comercio_id>/imagenes/', ComercioImagenUploadAPIView.as_view(), name='comercio-subir-imagen'),
    path('mis-comercios/<int:comercio_id>/imagenes/', ComercioImagenListAPIView.as_view(), name='comercio-listar-imagenes'),
    path('mis-comercios/<int:comercio_id>/imagenes/<int:imagen_id>/', ComercioImagenDeleteAPIView.as_view(), name='comercio-eliminar-imagen'),
    path('mis-comercios/<int:comercio_id>/horarios/', HorariosComerciosAPIView.as_view(), name='comercio-eliminar-imagen'),
    path('<int:comercio_id>/horarios/', FranjaHorarioAPIView.as_view(), name='crud-horarios-comercio'),
]

