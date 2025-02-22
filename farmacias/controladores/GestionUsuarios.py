from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from ..models import Empleado, Sucursal, HistorialEmpleado
from django.db import IntegrityError

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("Debes iniciar sesión")
            if request.user.cargo not in allowed_roles:
                messages.error(request, 'No tienes permisos para acceder a esta página.')
                return redirect(f'inicio_{request.user.cargo}')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def registrar_empleado(request):
    if request.method == 'POST':
        # Recogemos los datos manualmente desde request.POST
        email = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono', None)
        direccion = request.POST.get('direccion', None)
        fecha_ingreso = request.POST.get('fecha_ingreso')
        sucursal_id = request.POST.get('sucursal')
        cargo = request.POST.get('cargo')
        password = request.POST.get('password')

        # Validación básica
        errores = []
        if not email:
            errores.append("El campo 'Correo Electrónico' es obligatorio.")
        if not nombre:
            errores.append("El campo 'Nombre' es obligatorio.")
        if not apellido:
            errores.append("El campo 'Apellido' es obligatorio.")
        if not cedula:
            errores.append("El campo 'Cédula' es obligatorio.")
        if not fecha_nacimiento:
            errores.append("El campo 'Fecha de Nacimiento' es obligatorio.")
        if not fecha_ingreso:
            errores.append("El campo 'Fecha de Ingreso' es obligatorio.")
        if not password:
            errores.append("El campo 'Contraseña' es obligatorio.")
        if not cargo:
            errores.append("Debe seleccionar un cargo.")

        # Verificación de unicidad para email y cédula
        if Empleado.objects.filter(email=email).exists():
            errores.append("El correo electrónico ya está registrado.")
        if Empleado.objects.filter(cedula=cedula).exists():
            errores.append("La cédula ya está registrada.")

        # Validar sucursal (si se selecciona)
        sucursal = None
        if sucursal_id:
            try:
                sucursal = Sucursal.objects.get(id=sucursal_id)
            except Sucursal.DoesNotExist:
                errores.append("La sucursal seleccionada no es válida.")

        # Si hay errores, se muestran en el template
        if errores:
            messages.error(request, "Por favor corrige los errores del formulario.")
            return render(request, 'registroEmpleado.html', {
                'sucursales': Sucursal.objects.all(),
                'cargos': Empleado.CARGOS,
                'errores': errores,
            })

        # Crear empleado si todo es válido
        try:
            empleado = Empleado.objects.create(
                email=email,
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                direccion=direccion,
                fecha_ingreso=fecha_ingreso,
                sucursal=sucursal,
                cargo=cargo,
            )
            empleado.set_password(password)  # Encriptar la contraseña
            empleado.save()
            messages.success(request, "Empleado registrado con éxito.")

            #Creamos el primer registro del usuario:
            historial = HistorialEmpleado.objects.create(
                empleado=empleado,
                sucursal=sucursal,
                fecha_inicio=fecha_ingreso,
                cargo=cargo
            )
            historial.save()
            return redirect('login')  # Redirigir a la página de login o donde prefieras
        except IntegrityError:
            messages.error(request, "Ocurrió un error al registrar el empleado. Intente nuevamente.")
    else:
        return render(request, 'publico/registroEmpleado.html', {
        'sucursales': Sucursal.objects.all(),
        'cargos': Empleado.CARGOS
    })



@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login') 



def login_view(request):

    next_url = request.GET.get('next', 'inicio_publico')  

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect(next_url) 
        else:
            messages.error(request, 'Credenciales inválidas. Intenta de nuevo.')
    
    return render(request, 'publico/Login.html')


