from django.db import models
from django.forms import ModelForm, PasswordInput

# Create your models here.
class Producto(models.Model):
    TIPOS = [
        ("OMN", "Omnívora"),
        ("VGT", "Vegetariana"),
        ("VGN", "Vegana"),
        ("ACO", "Acompañamiento")
    ]

    nombre = models.CharField(max_length=40)
    precio_unico = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    precio_mediana = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    precio_familiar = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    ingredientes = models.CharField(max_length=200)
    disponible = models.BooleanField(default=True)
    tipo = models.CharField(
        max_length = 3,
        choices = TIPOS,
        default = TIPOS[0][0]
    )

class FormProducto(ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "tipo", "precio_unico", "precio_mediana", "precio_familiar", "ingredientes"]

class Pedido(models.Model):
    ESTADO = [
        ("PG", "No pagado"),
        ("PD", "Pendiente"),
        ("EN", "Enviado"),
        ("RC", "Recibido"),
        ("CN", "Cancelado")
    ]

    estado = models.CharField(
        max_length = 2,
        choices = ESTADO,
        default = ESTADO[1][0]
    )
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_completada = models.DateTimeField(null=True)
    direccion = models.CharField(max_length=300)

class FragmentoPedido(models.Model):
    TAMANOS = [
        ("MD", "Mediana"),
        ("FM", "Familiar"),
        ("AC", "Acompañamiento")
    ]
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    cantidad = models.IntegerField()
    tamano  = models.CharField(
        max_length = 2,
        choices = TAMANOS,
        default = TAMANOS[0][0]
    )
    precio_total = models.DecimalField(max_digits=20, decimal_places=2)

class Trabajador(models.Model):
    rut = models.IntegerField(unique=True)
    password = models.CharField(max_length=30)

class FormTrabajador(ModelForm):
    class Meta:
        model = Trabajador
        fields = ["rut", "password"]
        labels = {
            'rut': 'RUT (sin guión o puntos):',
            'password': 'Contraseña:'
        }
        widgets = {'password': PasswordInput()}