from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from farmacias.controladores.GestionUsuarios import *
from farmacias.models import Monodroga
from django import forms

# Formulario para Monodroga
class MonodrogaForm(forms.ModelForm):
    class Meta:
        model = Monodroga
        fields = ['nombre']


@login_required
@role_required(['admin'])
def listar_monodrogas(request):
    """
    Lista todas las monodrogas y las muestra en la vista de gestión.
    """
    monodrogas = Monodroga.objects.all()
    return render(request, 'admin/GestionMonodrogas.html', {'monodrogas': monodrogas})


@login_required
@role_required(['admin'])
def agregar_monodroga(request):
    """
    Procesa el formulario para agregar una nueva monodroga.
    """
    if request.method == 'POST':
        form = MonodrogaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Monodroga agregada correctamente.")
            return redirect('listar_monodrogas')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
            return redirect('listar_monodrogas')
    else:
        return redirect('listar_monodrogas')


@login_required
@role_required(['admin'])
def editar_monodroga(request, pk):
    """
    Permite editar una monodroga existente.
    """
    monodroga = Monodroga.objects.get(pk=pk)
    if request.method == 'POST':
        form = MonodrogaForm(request.POST, instance=monodroga)
        if form.is_valid():
            form.save()
            messages.success(request, "Monodroga actualizada correctamente.")
            return redirect('listar_monodrogas')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
            return redirect('listar_monodrogas')
    else:
        return redirect('listar_monodrogas')


@login_required
@role_required(['admin'])
def eliminar_monodroga(request, pk):
    """
    Elimina una monodroga de la base de datos.
    """
    monodroga = Monodroga.objects.get(pk=pk)
    monodroga.delete()
    messages.success(request, "Monodroga eliminada correctamente.")
    return redirect('listar_monodrogas')
