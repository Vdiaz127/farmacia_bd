from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class EmpleadoManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre


class Empleado(AbstractBaseUser):
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
    telefono = models.CharField(max_length=15, blank=True, null=True)
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
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nombre


# Tabla de Cargos Históricos de Empleados
class Historial_empleado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.empleado} - {self.cargo}"


# Tabla de Medicamentos
class Medicamento(models.Model):
    nombre = models.CharField(max_length=255)
    presentacion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    monodrogas = models.CharField(max_length=255)
    accion_terapeutica = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre



# Tabla de Medicamentos en Sucursales (STOCK)
class Medicamento_Sucursal(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    presentacion = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.medicamento} en {self.sucursal}"


# Tabla de Medicamentos por Laboratorio
class MedicamentoLaboratorio(models.Model):
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.medicamento} - {self.laboratorio}"


# Tabla de Pedidos
class Pedido(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha_pedido = models.DateField()
    analista = models.CharField(max_length=255)
    condiciones_pago = models.CharField(max_length=100)

    def __str__(self):
        return f"Pedido {self.id} - {self.sucursal}"


# Tabla de Compras
class Compra(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    fecha_compra = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra {self.id} - {self.monto_total}"


# Tabla de Productos en pedido
class ProductoS_pedido(models.Model):
    compra = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.medicamento}"


# Tabla de Cuentas por Pagar
class CuentaPorPagar(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento = models.DateField()
    estado_pago = models.CharField(max_length=20, choices=[('pagado', 'Pagado'), ('pendiente', 'Pendiente')])

    def __str__(self):
        return f"Cuenta {self.id} - {self.estado_pago}"

