import datetime
from django import forms
from django.shortcuts import render, redirect
from farmacias.models import HistorialEmpleado, Empleado, Sucursal
from farmacias.controladores.GestionUsuarios import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from farmacias.controladores.GestionUsuarios import role_required
from farmacias.utils import render_to_pdf_wkhtmltopdf

class HistorialEmpleadoForm(forms.ModelForm):
    class Meta:
        model = HistorialEmpleado
        fields = '__all__'

@role_required(['admin'])
@login_required
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
        'sucursales': sucursales,
        'cargos': Empleado.CARGOS,
    }

    return render(request, 'admin/GestionHistorialEmpleado.html', ctx)

@role_required(['admin'])
@login_required
def agregar_historial_empleado(request):
    if request.method == "POST":
        form = HistorialEmpleadoForm(request.POST)
        if form.is_valid():
            empleado_id = request.POST.get('empleado')
            fecha_inicio = form.cleaned_data['fecha_inicio']
            fecha_fin = form.cleaned_data.get('fecha_fin')  # Puede ser None si es un historial en vigor
            nueva_sucursal = form.cleaned_data['sucursal']
            nuevo_cargo = form.cleaned_data['cargo']

            # Finalizar historiales activos previos
            active_historiales = HistorialEmpleado.objects.filter(empleado_id=empleado_id, estado=True)
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
            if fecha_fin is None:
                nuevo_historial.estado = True
            else:
                nuevo_historial.estado = False
            nuevo_historial.save()

            # Actualizar empleado solo si el historial recién creado está en vigor
            if nuevo_historial.estado:
                empleado = Empleado.objects.get(id=empleado_id)
                empleado.sucursal = nueva_sucursal
                empleado.cargo = nuevo_cargo
                empleado.save()

            messages.success(request, "Historial agregado correctamente.")
            return redirect('get_historial')
        else:
            messages.error(request, "Error en el formulario, por favor revisa los datos.")
            return redirect('get_historial')
    return redirect('get_historial')

def get_historial_pdf(request, sucursal=None):
    historiales = HistorialEmpleado.objects.all()
    if sucursal:
        historiales = historiales.filter(sucursal=sucursal)
    return render_to_pdf_wkhtmltopdf(request, 'admin/GestionHistorialEmpleado.html', {'historiales': historiales})
