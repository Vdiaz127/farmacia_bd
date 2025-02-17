from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from farmacias.models import Empleado
from farmacias.controladores.GestionUsuarios import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

@login_required
@role_required(['admin'])
def gestion_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'admin/empleados/GestionEmpleados.html', {'empleados': empleados})

# @login_required
# @role_required(['admin'])
# def agregar_empleado(request):
#     form = EmpleadoForm(request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect('gestion_empleados')
#     return render(request, 'publico/RegistroEmpleado.html', {'form': form})

@login_required
@role_required(['admin'])
def editar_empleado(request, pk=None):
    if pk:
        empleado = get_object_or_404(Empleado, id=pk)
    else:
        empleado = None

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('gestion_empleados')
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, 'admin/empleados/FormularioEmpleado.html', {'form': form})

@login_required
@role_required(['admin'])
def eliminar_empleado(request, pk):
    empleado = Empleado.objects.get(pk=pk)
    empleado.delete()
    messages.success(request, "Empleado eliminado correctamente.")
    return redirect('gestion_empleados')