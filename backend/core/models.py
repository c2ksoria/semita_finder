from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from .utils.constants import ESTADOS_PEDIDO

# Main User Class
class Usuario(AbstractUser):
    def es_cliente(self):
        return self.pedidos.exists()

    def es_vendedor(self):
        return self.comercios.exists()
    
    def __str__(self):
        return f"{self.username}"

# Define a commercial building
class Comercio(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comercios'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    latitud = models.DecimalField(max_digits=9, decimal_places=7)
    longitud = models.DecimalField(max_digits=9, decimal_places=7)
    
    stock_semitas = models.PositiveIntegerField(default=0)

    # Month and Year of beginning activity
    anio_inicio = models.PositiveIntegerField()
    mes_inicio = models.PositiveSmallIntegerField(choices=[
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ])

    # Active or non active state
    activo = models.BooleanField(default=True)

    # Timestamps
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.usuario.username})"

# Model used to save opening ranges of commercial business
class FranjaHorario(models.Model):
    DIA_CHOICES = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    comercio = models.ForeignKey(
        'Comercio',
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    dia = models.IntegerField(choices=DIA_CHOICES)
    apertura = models.TimeField()
    cierre = models.TimeField()

    class Meta:
        ordering = ['dia', 'apertura']

    def __str__(self):
        return f"{self.get_dia_display()} {self.apertura.strftime('%H:%M')}–{self.cierre.strftime('%H:%M')}"

# Used to save differents type of semitas
class TipoSemita(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Model used to save differents products relative to each commerce
class Producto(models.Model):
    comercio = models.ForeignKey(
        'Comercio',
        on_delete=models.CASCADE,
        related_name='productos'
    )
    tipo = models.ForeignKey(
        'TipoSemita',
        on_delete=models.PROTECT,
        related_name='productos'
    )
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    en_stock = models.BooleanField(default=True)
    activo = models.BooleanField(default=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} – {self.tipo.nombre} - {self.comercio.nombre}"

# You can save images relatives to one product
class SemitaImagen(models.Model):
    producto = models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE,
        related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='imagesSemitas/')
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"

# Products order model
class Pedido(models.Model):

    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    comercio = models.ForeignKey(
        'Comercio',
        on_delete=models.CASCADE,
        related_name='pedidos'
    )
    fecha_hora_retiro = models.DateTimeField()
    comentario = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} – {self.cliente.username} a {self.comercio.nombre}"

    def calcular_total(self):
        return sum(item.subtotal() for item in self.items.all())

# Items of products relative to each product order
class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        related_name='items'
    )
    producto = models.ForeignKey(
        'Producto',
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField()
    precio_item = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.precio_item is None:
            self.precio_item = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} – Pedido #{self.pedido.id}"
    
    def subtotal(self):
        return self.precio_item or 0  # por seguridad

# Regiter earch movement of each order
class MovimientoPedido(models.Model):
    pedido = models.ForeignKey(
        'Pedido',
        on_delete=models.CASCADE,
        related_name='movimientos'
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cambios_pedido'
    )
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO)
    comentario = models.TextField(blank=True, null=True)
    fecha_moviminto = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Estado: {self.estado} – Pedido #{self.pedido.id} – {self.fecha_moviminto.strftime('%Y-%m-%d %H:%M')}"

# Images relative to each Commerce
class ComercioImagen(models.Model):
    comercio = models.ForeignKey(
        Comercio, on_delete=models.CASCADE, related_name='imagenes'
    )
    imagen = models.ImageField(upload_to='comercios/')
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f"Imagen de {self.comercio.nombre} - Principal: {self.principal}"