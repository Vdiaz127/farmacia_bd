from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from farmacias.controladores.GestionUsuarios import *
from farmacias.models import Medicamento, Medicamento_Sucursal, MedicamentoLaboratorio

class MedicamentoSucursalForm(forms.ModelForm):
    class Meta:
        model = Medicamento_Sucursal
        fields = '__all__'

@login_required
@role_required(['admin'])
def gestion_medicamento_sucursal(request, pk=None):
    medicamentos = Medicamento.objects.all()
    medicamentos_sucursal = Medicamento_Sucursal.objects.filter(sucursal_id=pk)
    laboratorio_medicamento = MedicamentoLaboratorio.objects.all()

    ctx = {
        'medicamentos': [{
            "medicamento": medicamento,
            "laboratorios": [{"pk": lab.laboratorio.id, "nombre": lab.laboratorio.nombre} for lab in laboratorio_medicamento if lab.medicamento_id == medicamento.id]
        } for medicamento in medicamentos],
        'medicamentos_sucursal': medicamentos_sucursal,
        'sucursal_id': pk,
    }
    return render(request, 'admin/GestionMedicamentoSucursal.html', context=ctx)

@login_required
@role_required(['admin'])
def agregar_medicamento_sucursal(request):
    if request.method == 'POST':
        form = MedicamentoSucursalForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Medicamento en sucursal agregado correctamente.")
                return redirect('gestion_medicamento_sucursal', pk=request.POST.get('sucursal'))
            except IntegrityError:
                messages.error(request, "Error: Este medicamento en sucursal ya existe.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
            return redirect('gestion_medicamento_sucursal', pk=int(request.POST.get('sucursal')))
    else:
        return redirect('gestion_sucursal')

@login_required
@role_required(['admin'])
def editar_medicamento_sucursal(request, pk):
    medicamento_sucursal = Medicamento_Sucursal.objects.get(pk=pk)
    if request.method == 'POST':
        form = MedicamentoSucursalForm(request.POST, instance=medicamento_sucursal)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Medicamento en sucursal actualizado correctamente.")
                return redirect('gestion_medicamento_sucursal')
            except IntegrityError:
                messages.error(request, "Error: Este medicamento en sucursal ya existe.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en el campo {field}: {error}")
            return redirect('gestion_medicamento_sucursal')
    else:
        return redirect('gestion_medicamento_sucursal')

@login_required
@role_required(['admin'])
def eliminar_medicamento_sucursal(request, pk):
    medicamento_sucursal = Medicamento_Sucursal.objects.get(pk=pk)
    medicamento_sucursal.delete()
    messages.success(request, "Medicamento en sucursal eliminado correctamente.")
    return redirect('gestion_medicamento_sucursal')