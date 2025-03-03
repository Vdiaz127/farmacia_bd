from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from farmacias.controladores.GestionUsuarios import *
from farmacias.models import Laboratorio
from django import forms

from django.contrib import messages
import random
import string

class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ['nombre', 'direccion', 'telefono', 'email']

@login_required
@role_required(['admin'])
def gestion_laboratorios(request):
    laboratorios = Laboratorio.objects.all()
    return render(request, 'admin/GestionLaboratorio.html', {'laboratorios': laboratorios})

def generar_contraseña_aleatoria(length=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for i in range(length))

@login_required
@role_required(['admin'])
def agregar_laboratorio(request):
    if request.method == 'POST':
        form = LaboratorioForm(request.POST)
        if form.is_valid():
            try:
                laboratorio = form.save(commit=False)
                laboratorio.especialPassword = generar_contraseña_aleatoria()
                laboratorio.save()
                messages.success(request, "Laboratorio agregado correctamente.")
                return redirect('gestion_laboratorios')  # Redirige al listado de laboratorios
            except IntegrityError:
                messages.error(request, "Error: Este laboratorio ya existe.")
        else:
            # Mostrar los errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
            return redirect('gestion_laboratorios')
    else:
        return redirect('gestion_laboratorios')


@login_required
@role_required(['admin'])
def editar_laboratorio(request, pk):
    laboratorio = Laboratorio.objects.get(pk=pk)
    if request.method == 'POST':
        form = LaboratorioForm(request.POST, instance=laboratorio)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Laboratorio actualizado correctamente.")
                return redirect('gestion_laboratorios')
            except IntegrityError:
                messages.error(request, "Error: Este laboratorio ya existe.")
        else:
            # Mostrar los errores específicos del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
            return redirect('gestion_laboratorios')
    else:
        return redirect('gestion_laboratorios')


@login_required
@role_required(['admin'])
def eliminar_laboratorio(request, pk):
    laboratorio = Laboratorio.objects.get(pk=pk)
    laboratorio.delete()
    messages.success(request, "Laboratorio eliminado correctamente.")
    return redirect('gestion_laboratorios')


