from rest_framework.permissions import BasePermission


class EsVendedor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.comercios.exists()


class EsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.pedidos.exists()


class EsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
