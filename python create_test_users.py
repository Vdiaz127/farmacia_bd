import os
import django
from datetime import date

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadena_farmacias.settings')
django.setup()

from farmacias.models import Empleado  # Modelo personalizado

def create_test_users():
    # Lista de usuarios de prueba
    users = [
        {
            'email': 'admin@empresa.com',
            'nombre': 'Admin',
            'apellido': 'Admin',
            'cedula': '1234567890',
            'fecha_nacimiento': date(1990, 1, 1),
            'telefono': '123456789',
            'direccion': 'Calle Ficticia 123',
            'password': '123456',
            'fecha_ingreso': date(2020, 1, 1),
            'cargo': 'admin'
        },
        {
            'email': 'empleado1@empresa.com',
            'nombre': 'Empleado',
            'apellido': 'Uno',
            'cedula': '1234567891',
            'fecha_nacimiento': date(1985, 5, 15),
            'telefono': '987654321',
            'direccion': 'Avenida Ficticia 456',
            'password': '123456',
            'fecha_ingreso': date(2022, 6, 1),
            'cargo': 'farmaceutico'
        },
    ]

    for user_data in users:
        # Verificar si el usuario ya existe por correo electrónico
        if not Empleado.objects.filter(email=user_data['email']).exists():
            user = Empleado.objects.create_user(
                email=user_data['email'],
                nombre=user_data['nombre'],
                apellido=user_data['apellido'],
                cedula=user_data['cedula'],
                telefono=user_data['telefono'],
                direccion=user_data['direccion'],
                password=user_data['password'],
                fecha_nacimiento=user_data['fecha_nacimiento'],
                fecha_ingreso=user_data['fecha_ingreso'],
                cargo=user_data['cargo']
            )
            # Asignar atributos adicionales
            user.is_staff = user_data.get('is_staff', False)
            user.is_active = user_data.get('is_active', True)
            user.is_superuser = user_data.get('is_superuser', False)
            user.save()
            print(f"Usuario '{user.email}' creado exitosamente.")
        else:
            print(f"Usuario '{user_data['email']}' ya existe.")

# Script para registrar sucursales en la base de datos
from farmacias.models import Sucursal  

# Lista de sucursales extraídas o deducidas del texto
sucursales = [
    {"nombre": "Farmacia X", "ciudad": "Ciudad A", "direccion": "Av. Principal #123", "telefono": "0212-1234567"},
    {"nombre": "Farmacia Z", "ciudad": "Ciudad B", "direccion": "Calle Secundaria #456", "telefono": "0212-7654321"},
    {"nombre": "Farmacia Central", "ciudad": "Ciudad C", "direccion": "Centro Comercial XYZ, Local 10", "telefono": "0212-1112233"},
    {"nombre": "Farmacia Norte", "ciudad": "Ciudad D", "direccion": "Carretera Nacional Km. 12", "telefono": "0212-3344556"},
    {"nombre": "Farmacia Sur", "ciudad": "Ciudad E", "direccion": "Zona Industrial, Parcela 45", "telefono": "0212-6677889"},
]

# Registro de sucursales en la base de datos
for sucursal in sucursales:
    obj, created = Sucursal.objects.get_or_create(
        nombre=sucursal["nombre"],
        defaults={
            "ciudad": sucursal["ciudad"],
            "direccion": sucursal["direccion"],
            "telefono": sucursal["telefono"],
        },
    )
    if created:
        print(f"Sucursal '{obj.nombre}' registrada con éxito.")
    else:
        print(f"Sucursal '{obj.nombre}' ya existe en la base de datos.")


if __name__ == '__main__':
    create_test_users()
