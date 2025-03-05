from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from farmacias.models import HistorialEmpleado, Empleado
from farmacias.controladores.GestionUsuarios import *
from django.contrib.auth.decorators import login_required
from farmacias.controladores.GestionUsuarios import role_required
from farmacias.utils import render_to_pdf
class HistorialEmpleadoForm(forms.ModelForm):
    class Meta:
        model = HistorialEmpleado
        fields = '__all__'

@role_required(['admin'])
@login_required
def get_historial(request, sucursal=None):
    historiales = HistorialEmpleado.objects.all()
    sucursales = Sucursal.objects.all()

    if sucursal:
        historiales = historiales.filter(sucursal=sucursal)
        sucursales = sucursales.exclude(id=sucursal)

    ctx = {
        'historiales': historiales,
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
            old_historial = request.POST.get('historial')
            old_historial = HistorialEmpleado.objects.get(id=old_historial)
            old_historial.fecha_fin = request.POST.get('fecha_inicio')
            old_historial.save()
            form.save()
            return redirect('get_historial')
    print("TODO FINO POR AQUI")
    return redirect('get_historial')
    # else:
    # form = HistorialEmpleadoForm()

    # return render(request, 'admin/AgregarHistorialEmpleado.html', {'form': form})
    # return render(request, 'admin/GestionHistorialEmpleado.html', {'historiales': historiales})

@render_to_pdf
def get_historial_pdf(request, sucursal=None):
    historiales = HistorialEmpleado.objects.all()

    if sucursal:
        historiales = historiales.filter(sucursal=sucursal)

    return ('admin/GestionHistorialEmpleado.html', {'historiales': historiales})
