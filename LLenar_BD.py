import os
import django
from datetime import date

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadena_farmacias.settings')
django.setup()

from farmacias.models import Empleado, Sucursal, Laboratorio, Monodroga

def create_sucursales():
    # Lista de sucursales extraídas o deducidas del texto
    sucursales = [
        {"nombre": "Farmacia X", "ciudad": "Ciudad A", "direccion": "Av. Principal #123", "telefono": "0212-1234567"},
        {"nombre": "Farmacia Z", "ciudad": "Ciudad B", "direccion": "Calle Secundaria #456", "telefono": "0212-7654321"},
        {"nombre": "Farmacia Central", "ciudad": "Ciudad C", "direccion": "Centro Comercial XYZ, Local 10", "telefono": "0212-1112233"},
        {"nombre": "Farmacia Norte", "ciudad": "Ciudad D", "direccion": "Carretera Nacional Km. 12", "telefono": "0212-3344556"},
        {"nombre": "Farmacia Sur", "ciudad": "Ciudad E", "direccion": "Zona Industrial, Parcela 45", "telefono": "0212-6677889"},
    ]

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
            'cargo': 'admin',
            'sucursal': 'Farmacia X'
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
            'cargo': 'farmaceutico',
            'sucursal': 'Farmacia Z'
        },
        {
            'email': 'empleado2@empresa.com',
            'nombre': 'Empleado',
            'apellido': 'Dos',
            'cedula': '1234567892',
            'fecha_nacimiento': date(1988, 3, 22),
            'telefono': '123123123',
            'direccion': 'Calle Real 789',
            'password': '123456',
            'fecha_ingreso': date(2021, 7, 1),
            'cargo': 'auxiliar',
            'sucursal': 'Farmacia Central'
        },
        {
            'email': 'empleado3@empresa.com',
            'nombre': 'Empleado',
            'apellido': 'Tres',
            'cedula': '1234567893',
            'fecha_nacimiento': date(1992, 8, 30),
            'telefono': '321321321',
            'direccion': 'Avenida Siempre Viva 123',
            'password': '123456',
            'fecha_ingreso': date(2019, 9, 1),
            'cargo': 'pasante',
            'sucursal': 'Farmacia Norte'
        },
        {
            'email': 'farmaceutico1@empresaX.com',
            'nombre': 'Empleado',
            'apellido': 'Uno',
            'cedula': '12345815',
            'fecha_nacimiento': date(1985, 5, 15),
            'telefono': '987654321',
            'direccion': 'Avenida Ficticia 456',
            'password': '123456',
            'fecha_ingreso': date(2022, 6, 1),
            'cargo': 'farmaceutico',
            'sucursal': 'Farmacia X'
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
            
            # Asociar la sucursal según el nombre
            sucursal_nombre = user_data.get('sucursal')
            if sucursal_nombre:
                try:
                    sucursal_obj = Sucursal.objects.get(nombre=sucursal_nombre)
                    user.sucursal = sucursal_obj
                except Sucursal.DoesNotExist:
                    print(f"La sucursal '{sucursal_nombre}' no existe. No se pudo asociar al usuario {user.email}.")
            user.save()
            print(f"Usuario '{user.email}' creado exitosamente.")
        else:
            print(f"Usuario '{user_data['email']}' ya existe.")

def create_laboratorios():
    # Lista de laboratorios de ejemplo
    laboratorios = [
        {"nombre": "Laboratorio A", "direccion": "Calle Lab A 123", "telefono": "0212-1112222", "email": "labA@example.com"},
        {"nombre": "Laboratorio B", "direccion": "Calle Lab B 456", "telefono": "0212-3334444", "email": "labB@example.com"},
        {"nombre": "Laboratorio C", "direccion": "Calle Lab C 789", "telefono": "0212-5556666", "email": "labC@example.com"},
    ]
    for lab in laboratorios:
        obj, created = Laboratorio.objects.get_or_create(
            nombre=lab["nombre"],
            defaults={
                "direccion": lab["direccion"],
                "telefono": lab["telefono"],
                "email": lab["email"],
            }
        )
        if created:
            print(f"Laboratorio '{obj.nombre}' registrado con éxito.")
        else:
            print(f"Laboratorio '{obj.nombre}' ya existe en la base de datos.")

def create_monodrogas():
    # Lista de monodrogas de ejemplo
    monodrogas = [
        {"nombre": "Paracetamol"},
        {"nombre": "Ibuprofeno"},
        {"nombre": "Ambroxol"},
    ]
    for mono in monodrogas:
        obj, created = Monodroga.objects.get_or_create(
            nombre=mono["nombre"]
        )
        if created:
            print(f"Monodroga '{obj.nombre}' registrada con éxito.")
        else:
            print(f"Monodroga '{obj.nombre}' ya existe en la base de datos.")

if __name__ == '__main__':
    create_sucursales()
    create_test_users()
    create_laboratorios()
    create_monodrogas()
