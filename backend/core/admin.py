from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Comercio, FranjaHorario, TipoSemita, Producto, SemitaImagen, Pedido, ItemPedido, MovimientoPedido

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    ordering = ('id',)

@admin.register(Comercio)
class ComercioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'activo', 'stock_semitas', 'anio_inicio', 'mes_inicio')
    list_filter = ('nombre', 'usuario', 'activo')
    search_fields = ('nombre', 'usuario__username', 'direccion')
    ordering = ('nombre',)

@admin.register(FranjaHorario)
class FranjaHorarioAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FranjaHorario._meta.get_fields()]
    ordering = ('id',)

@admin.register(TipoSemita)
class TipoSemitaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('comercio', 'tipo', 'nombre', 'precio', 'en_stock', 'activo')

@admin.register(SemitaImagen)
class SemitaImagendmin(admin.ModelAdmin):
    list_display = ('producto','imagen', 'principal')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('cliente','comercio','fecha_hora_retiro', 'comentario','estado', 'creado_en')


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido','producto', 'cantidad', 'precio_item')


@admin.register(MovimientoPedido)
class MovimientoPedidodmin(admin.ModelAdmin):
    list_display = ('pedido','usuario', 'estado','comentario', 'fecha_moviminto')