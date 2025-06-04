from django.urls import path
from core.views.auth import RegistroUsuarioAPIView, LoginAPIView, LogoutAPIView, UsuarioActualAPIView

urlpatterns = [
    path('register/', RegistroUsuarioAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('me/', UsuarioActualAPIView.as_view(), name='me'),  # 👈 nuevo endpoint
]
