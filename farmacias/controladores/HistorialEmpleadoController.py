import datetime
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from farmacias.models import HistorialEmpleado, Empleado, Sucursal
from farmacias.controladores.GestionUsuarios import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmacias.controladores.GestionUsuarios import role_required
from weasyprint import HTML

class HistorialEmpleadoForm(forms.ModelForm):
    class Meta:
        model = HistorialEmpleado
        fields = '__all__'

@login_required
@role_required(['admin'])
def get_historial(request, sucursal=None):
    historiales = HistorialEmpleado.objects.all()
    sucursales = Sucursal.objects.all()
    sucursal_name = None

    if sucursal:
        historiales = historiales.filter(sucursal=sucursal)
        sucursales = sucursales.exclude(id=sucursal)
        sucursal_name = Sucursal.objects.get(pk=sucursal).nombre

    ctx = {
        'historiales': historiales,
        'sucursal_name': sucursal_name,
        'sucursal': sucursal,
        'sucursales': sucursales,
        'cargos': Empleado.CARGOS,
    }

    return render(request, 'admin/GestionHistorialEmpleado.html', ctx)

@login_required
@role_required(['admin'])
def agregar_historial_empleado(request):
    if request.method == "POST":
        form = HistorialEmpleadoForm(request.POST)
        if form.is_valid():
            empleado_cedula = request.POST.get('empleado')
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data.get('fecha_fin')  # Puede ser None si es un historial en vigor
            nueva_sucursal = form.cleaned_data['sucursal']
            nuevo_cargo = form.cleaned_data['cargo']

            # Finalizar historiales activos previos
            active_historiales = HistorialEmpleado.objects.filter(empleado_id=empleado_cedula, estado=True)
            for historial in active_historiales:
                if fecha_inicio <= historial.fecha_inicio:
                    messages.error(
                        request, 
                        "Error: La nueva fecha de inicio debe ser posterior a la fecha de inicio del historial activo."
                    )
                    return redirect('get_historial')
                if historial.fecha_fin is None:
                    historial.fecha_fin = fecha_inicio
                    historial.estado = False
                    historial.save()

            # Crear el nuevo historial
            nuevo_historial = form.save(commit=False)
            # Se marca como activo si no se provee fecha_fin, sin importar si la fecha de inicio es futura
            nuevo_historial.estado = True if fecha_fin is None else False
            nuevo_historial.save()

            # Actualizar empleado solo si el historial recién creado está en vigor
            if nuevo_historial.estado:
                empleado = Empleado.objects.get(cedula=empleado_cedula)
                empleado.sucursal = nueva_sucursal
                empleado.cargo = nuevo_cargo
                empleado.save()

            messages.success(request, "Historial agregado correctamente.")
            return redirect('get_historial')
        else:
            messages.error(request, "Error en el formulario, por favor revisa los datos.")
            return redirect('get_historial')
    return redirect('get_historial')

# @login_required
# @role_required(['admin'])
# def get_historial_pdf(request, sucursal=None):
#     # Filtrar historiales según la sucursal si se indicó
#     historiales = HistorialEmpleado.objects.all()
#     if sucursal:
#         historiales = historiales.filter(sucursal=sucursal)
    
#     # Contexto para la plantilla
#     context = {'historiales': historiales}
#     # Renderiza la plantilla a una cadena HTML
#     html_string = render_to_string('admin/GestionHistorialEmpleado.html', context)
#     # Usar WeasyPrint para generar el PDF; base_url es importante para resolver rutas relativas a archivos estáticos
#     html = HTML(string=html_string, base_url=request.build_absolute_uri())
#     pdf = html.write_pdf()
    
#     # Crear la respuesta HTTP con el contenido PDF
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="HistorialEmpleado.pdf"'
#     return response
