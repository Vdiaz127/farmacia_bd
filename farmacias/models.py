from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class EmpleadoManager(BaseUserManager):
    """
    Manager personalizado para el modelo Empleado.
    Permite crear usuarios validando que se proporcione un email y gestionando la normalización del mismo.
    """
    def create_user(self, email, nombre, apellido, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Sucursal(models.Model):
    """
    Representa una sucursal de la cadena de farmacias.
    Contiene información como el nombre, ciudad, dirección y teléfono de la sucursal.
    """
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)


    def __str__(self):
        return self.nombre


class Empleado(AbstractBaseUser):
    """
    Representa a un empleado de la farmacia.
    Cada empleado tiene atributos personales y profesionales, y se relaciona con una sucursal.
    Se definen los cargos disponibles: admin, farmacéutico, auxiliar y pasante.
    """
    CARGOS = [
        ('admin', 'Administrador'),
        ('farmaceutico', 'Farmacéutico'),
        ('auxiliar', 'Auxiliar de Farmacia'),
        ('pasante', 'Pasante'),
    ]

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=15, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True, null=True)
    fecha_ingreso = models.DateField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, null=True, blank=True, related_name='empleados')
    cargo = models.CharField(max_length=20, choices=CARGOS, default='auxiliar')


    objects = EmpleadoManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'cargo']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Laboratorio(models.Model):
    """
    Representa un laboratorio que fabrica medicamentos.
    Se registra información de contacto y ubicación, como dirección, teléfono y email.
    """
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.TextField(unique=True)
    telefono = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    especialPassword = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre


class HistorialEmpleado(models.Model):
    """
    Representa el historial de cargos que ha tenido un empleado en diferentes sucursales.
    Se registra el cargo desempeñado, la fecha de inicio y la fecha de fin de cada período.
    """
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.empleado} - {self.cargo}"


class Monodroga(models.Model):
    """
    Representa una monodroga, es decir, el componente principal de un medicamento.
    Cada monodroga es única en la base de datos.
    """
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


class Medicamento(models.Model):
    """
    Representa un medicamento.
    Se incluye el nombre, presentación, precio, acción terapéutica y las monodrogas que lo componen.
    """
    nombre = models.CharField(max_length=255)
    presentacion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    monodrogas = models.ManyToManyField(Monodroga, related_name='medicamentos')
    accion_terapeutica = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Medicamento_Sucursal(models.Model):
    """
    Representa el stock de un medicamento en una sucursal específica.
    Se relaciona con el medicamento, la sucursal y el laboratorio que lo comercializa, 
    y registra la cantidad disponible.
    """
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.medicamento} en {self.sucursal}"


class MedicamentoLaboratorio(models.Model):
    """
    Representa la relación entre un medicamento y un laboratorio que lo fabrica.
    Permite que un mismo medicamento pueda ser producido por diferentes laboratorios.
    """
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.medicamento} - {self.laboratorio}"



FORMA_PAGO_CHOICES = [
    ('contado', 'Contado'),
    ('5d', '5 días'),
    ('15d', '15 días'),
    ('30d', '30 días'),
]

class Pedido(models.Model):
    """
    Representa la orden de compra emitida por una sucursal.
    """
    sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE)
    empleado = models.ForeignKey('Empleado', on_delete=models.SET_NULL, null=True, blank=True,
                                 help_text="Farmacéutico que emite el pedido")
    laboratorio = models.ForeignKey('Laboratorio', on_delete=models.CASCADE,
                                    help_text="Laboratorio al que se dirige el pedido")
    fecha_pedido = models.DateField()
    forma_pago = models.CharField(max_length=10, choices=FORMA_PAGO_CHOICES,
                                  help_text="Forma de pago de la orden de compra")
    @property
    def total(self):
        return sum(item.medicamento.precio * item.cantidad for item in self.items.all())
    
    def __str__(self):
        return f"Pedido {self.id} - {self.sucursal.nombre}"

class PedidoItem(models.Model):
    """
    Representa cada producto (medicamento) solicitado en un pedido.
    """
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    
    medicamento = models.ForeignKey('Medicamento', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    def __str__(self):
        return f"{self.cantidad} x {self.medicamento.nombre} (Pedido {self.pedido.id})"

class Compra(models.Model):
    """
    Representa la compra realizada a partir de un pedido. 
    Es decir, se registra lo que realmente llegó.
    """
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE,
                                  help_text="Número de pedido asociado a la compra")
    fecha_compra = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    forma_pago = models.CharField(max_length=10, choices=FORMA_PAGO_CHOICES,
                                  help_text="Forma de pago de la compra")
    
    def __str__(self):
        return f"Compra {self.id} - Pedido {self.pedido.id}"

class CompraItem(models.Model):
    """
    Representa cada producto (medicamento) que llegó en la compra.
    Estos items pueden ser distintos (en cantidad o selección) a los solicitados en el pedido.
    """
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='items')
    medicamento = models.ForeignKey('Medicamento', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    
    
    def __str__(self):
        return f"{self.cantidad} x {self.medicamento.nombre} (Compra {self.compra.id})"
