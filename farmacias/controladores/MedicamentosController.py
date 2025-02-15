from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from farmacias.controladores.GestionUsuarios import *
from farmacias.models import Laboratorio, Medicamento, MedicamentoLaboratorio
from django import forms

from django.contrib import messages

class MedicamentoForm(forms.ModelForm):
    laboratorios = forms.ModelMultipleChoiceField(
        queryset=Laboratorio.objects.all(),  # Obtener todos los laboratorios
        widget=forms.CheckboxSelectMultiple,  # Usar casillas de verificación para seleccionar laboratorios
        required=False
    )

    class Meta:
        model = Medicamento
        fields = ['nombre', 'monodrogas', 'presentacion', 'accion_terapeutica', 'precio', 'laboratorios']


@login_required
@role_required(['admin'])
def gestion_medicamentos(request):
    medicamentos = Medicamento.objects.all()
    laboratorios = Laboratorio.objects.all()
    # Se asume que también envías en el contexto las monodrogas para usarlas en la vista (en creación y edición)
    from farmacias.models import Monodroga
    monodrogas = Monodroga.objects.all()
    return render(request, 'admin/GestionMedicamentos.html', {
        'medicamentos': medicamentos, 
        'laboratorios': laboratorios,
        'monodrogas': monodrogas,
    })  


@login_required
@role_required(['admin'])
def agregar_medicamento(request):
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            # Guardamos el medicamento sin comprometer la relación many-to-many aún
            medicamento = form.save(commit=False)
            medicamento.save()
            # Procesamos el campo ManyToMany de monodrogas
            form.save_m2m()

            # Obtener los IDs de los laboratorios seleccionados
            laboratorios_seleccionados = request.POST.getlist('laboratorios')
            # Asociar cada laboratorio seleccionado con el medicamento usando la tabla intermedia
            for laboratorio_id in laboratorios_seleccionados:
                laboratorio = Laboratorio.objects.get(id=laboratorio_id)
                MedicamentoLaboratorio.objects.create(medicamento=medicamento, laboratorio=laboratorio)

            messages.success(request, "Medicamento agregado correctamente.")
            return redirect('gestion_medicamentos')  # Redirige al listado de medicamentos
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
            return redirect('gestion_medicamentos')
    else:
        return redirect('gestion_medicamentos')


@login_required
@role_required(['admin'])
def editar_medicamento(request, pk):
    medicamento = Medicamento.objects.get(pk=pk)
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.save()
            # Actualizamos las relaciones many-to-many de monodrogas
            form.save_m2m()
            
            # Limpiar las asociaciones previas con los laboratorios
            MedicamentoLaboratorio.objects.filter(medicamento=medicamento).delete()
            
            # Obtener los laboratorios seleccionados desde el formulario
            laboratorios_seleccionados = request.POST.getlist('laboratorios')
            for laboratorio_id in laboratorios_seleccionados:
                laboratorio = Laboratorio.objects.get(id=laboratorio_id)
                MedicamentoLaboratorio.objects.create(medicamento=medicamento, laboratorio=laboratorio)

            messages.success(request, "Medicamento actualizado correctamente.")
            return redirect('gestion_medicamentos')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
            return redirect('gestion_medicamentos')
    else:
        return redirect('gestion_medicamentos')


@login_required
@role_required(['admin'])
def eliminar_medicamento(request, pk):
    medicamento = Medicamento.objects.get(pk=pk)
    medicamento.delete()
    messages.success(request, "Medicamento eliminado correctamente.")
    return redirect('gestion_medicamentos')
