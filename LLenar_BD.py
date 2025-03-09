import os
import django
from datetime import date
import random
import string

# Configuración del entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cadena_farmacias.settings')
django.setup()

from farmacias.models import Empleado, Sucursal, Laboratorio, Monodroga, Medicamento, HistorialEmpleado, Medicamento_Sucursal, MedicamentoLaboratorio

def create_sucursales():
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
            create_empleados_for_sucursal(obj)
        else:
            print(f"Sucursal '{obj.nombre}' ya existe en la base de datos.")

def create_empleados_for_sucursal(sucursal):
    cargos = ['admin', 'farmaceutico', 'auxiliar', 'pasante']
    for cargo in cargos:
        email = f"{cargo}@{sucursal.nombre.replace(' ', '').lower()}.com"
        empleado = Empleado.objects.create_user(
            email=email,
            nombre=cargo.capitalize(),
            apellido=sucursal.nombre.replace(' ', ''),
            cedula=str(random.randint(1000000000, 9999999999)),
            fecha_nacimiento=date(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28)),
            telefono=str(random.randint(1000000000, 9999999999)),
            direccion=f"Dirección {cargo} {sucursal.nombre}",
            password='123456',
            cargo=cargo,
            sucursal=sucursal
        )
        HistorialEmpleado.objects.create(
            empleado=empleado,
            sucursal=sucursal,
            cargo=cargo,
            fecha_inicio=date.today()
        )
        print(f"Empleado '{empleado.email}' creado y registrado en el historial.")

def create_laboratorios():
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
                "especialPassword": generar_contraseña_aleatoria()
            }
        )
        if created:
            print(f"Laboratorio '{obj.nombre}' registrado con éxito.")
        else:
            print(f"Laboratorio '{obj.nombre}' ya existe en la base de datos.")

def generar_contraseña_aleatoria(length=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for i in range(length))

def create_monodrogas():
    monodrogas = [
        {"nombre": "Paracetamol"},
        {"nombre": "Ibuprofeno"},
        {"nombre": "Ambroxol"},
        {"nombre": "Amoxicilina"},
        {"nombre": "Clorfenamina"},
        {"nombre": "Dexametasona"},
        {"nombre": "Loratadina"},
        {"nombre": "Ranitidina"},
        {"nombre": "Omeprazol"},
        {"nombre": "Metformina"},
    ]
    for mono in monodrogas:
        obj, created = Monodroga.objects.get_or_create(
            nombre=mono["nombre"]
        )
        if created:
            print(f"Monodroga '{obj.nombre}' registrada con éxito.")
        else:
            print(f"Monodroga '{obj.nombre}' ya existe en la base de datos.")

def create_medicamentos():
    monodrogas = list(Monodroga.objects.all())
    laboratorios = list(Laboratorio.objects.all())
    medicamentos = [
        {"nombre": "Medicamento A", "presentacion": "Tabletas", "precio": 10.50, "accion_terapeutica": "Analgésico"},
        {"nombre": "Medicamento B", "presentacion": "Jarabe", "precio": 15.75, "accion_terapeutica": "Antiinflamatorio"},
        {"nombre": "Medicamento C", "presentacion": "Inyección", "precio": 25.00, "accion_terapeutica": "Antibiótico"},
        {"nombre": "Medicamento D", "presentacion": "Cápsulas", "precio": 12.30, "accion_terapeutica": "Antihistamínico"},
        {"nombre": "Medicamento E", "presentacion": "Suspensión", "precio": 8.90, "accion_terapeutica": "Antipirético"},
    ]
    for med in medicamentos:
        medicamento, created = Medicamento.objects.get_or_create(
            nombre=med["nombre"],
            defaults={
                "presentacion": med["presentacion"],
                "precio": med["precio"],
                "accion_terapeutica": med["accion_terapeutica"],
            }
        )
        if created:
            medicamento.monodrogas.set(random.sample(monodrogas, k=random.randint(1, 3)))
            medicamento.save()
            print(f"Medicamento '{medicamento.nombre}' registrado con éxito.")
        else:
            print(f"Medicamento '{medicamento.nombre}' ya existe en la base de datos.")
        
        # Asignar el medicamento a un laboratorio
        laboratorio = random.choice(laboratorios)
        MedicamentoLaboratorio.objects.create(
            medicamento=medicamento,
            laboratorio=laboratorio
        )
        print(f"Medicamento '{medicamento.nombre}' asignado al laboratorio '{laboratorio.nombre}'.")

        assign_medicamento_to_sucursales(medicamento, laboratorios)

def assign_medicamento_to_sucursales(medicamento, laboratorios):
    sucursales = list(Sucursal.objects.all())
    for sucursal in random.sample(sucursales, k=random.randint(1, len(sucursales))):
        laboratorio = random.choice(laboratorios)
        cantidad = random.randint(1, 100)
        Medicamento_Sucursal.objects.create(
            medicamento=medicamento,
            sucursal=sucursal,
            laboratorio=laboratorio,
            cantidad=cantidad
        )
        print(f"Medicamento '{medicamento.nombre}' asignado a la sucursal '{sucursal.nombre}' con cantidad {cantidad}.")

if __name__ == '__main__':
    create_sucursales()
    create_laboratorios()
    create_monodrogas()
    create_medicamentos()
