from django.db import IntegrityError
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django import forms
from farmacias.controladores.GestionUsuarios import *
from farmacias.models import Medicamento, Medicamento_Sucursal, MedicamentoLaboratorio

# Formulario para Medicamento en Sucursal
class MedicamentoSucursalForm(forms.ModelForm):
    class Meta:
        model = Medicamento_Sucursal
        fields = '__all__'


@login_required
@role_required(['admin'])
def gestion_medicamento_sucursal(request, pk=None):
    # Obtenemos la sucursal con el pk proporcionado
    sucursal = get_object_or_404(Sucursal, pk=pk)
    
    medicamentos = Medicamento.objects.all()
    medicamentos_sucursal = Medicamento_Sucursal.objects.filter(sucursal_id=pk)
    laboratorio_medicamento = MedicamentoLaboratorio.objects.all()

    ctx = {
        'sucursal': sucursal,  
        'medicamentos': [{
            "medicamento": medicamento,
            "laboratorios": [
                {"pk": lab.laboratorio.id, "nombre": lab.laboratorio.nombre} 
                for lab in laboratorio_medicamento if lab.medicamento_id == medicamento.id
            ]
        } for medicamento in medicamentos],
        'medicamentos_sucursal': medicamentos_sucursal,
    }
    return render(request, 'admin/GestionMedicamentoSucursal.html', context=ctx)


@login_required
@role_required(['admin'])
def agregar_medicamento_sucursal(request):
    if request.method == 'POST':
        data = request.POST.copy()
        # Se espera que "medicamento_laboratorio" tenga el formato "med_id|lab_id"
        ml_value = data.get('medicamento_laboratorio')
        if ml_value:
            try:
                med_id, lab_id = ml_value.split('|')
                data['medicamento'] = med_id
                data['laboratorio'] = lab_id
            except ValueError:
                messages.error(request, "Error al procesar la selección de medicamento y laboratorio.")
                return redirect('gestion_medicamento_sucursal', pk=data.get('sucursal'))
        else:
            messages.error(request, "No se seleccionó ningún medicamento-laboratorio.")
            return redirect('gestion_medicamento_sucursal', pk=data.get('sucursal'))

        sucursal_id = data.get('sucursal')
        try:
            cantidad_nueva = int(data.get('cantidad', 0))
        except ValueError:
            messages.error(request, "La cantidad debe ser un número válido.")
            return redirect('gestion_medicamento_sucursal', pk=sucursal_id)

        # Verificar si ya existe un registro para ese medicamento en ese laboratorio y sucursal
        existing_record = Medicamento_Sucursal.objects.filter(
            sucursal_id=sucursal_id,
            medicamento_id=med_id,
            laboratorio_id=lab_id
        ).first()

        if existing_record:
            # Si existe, se incrementa la cantidad
            existing_record.cantidad += cantidad_nueva
            if existing_record.cantidad <= 0:
                print("Cantidad no válida, eliminando registro.")
                existing_record.delete()
                messages.success(request, "El medicamento en sucursal fue eliminado debido a cantidad no válida.")
            else:
                existing_record.save()
                messages.success(request, "La cantidad del medicamento en sucursal fue actualizada correctamente.")
            return redirect('gestion_medicamento_sucursal', pk=sucursal_id)
        else:
            # Si no existe, se crea un registro nuevo
            if cantidad_nueva <= 0:
                messages.error(request, "La cantidad debe ser mayor a cero para agregar un nuevo medicamento.")
                return redirect('gestion_medicamento_sucursal', pk=sucursal_id)
            form = MedicamentoSucursalForm(data)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, "Medicamento en sucursal agregado correctamente.")
                    return redirect('gestion_medicamento_sucursal', pk=sucursal_id)
                except IntegrityError:
                    messages.error(request, "Error: Este medicamento en sucursal ya existe.")
                    return redirect('gestion_medicamento_sucursal', pk=sucursal_id)
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"Error en el campo {field}: {error}")
                return redirect('gestion_medicamento_sucursal', pk=int(sucursal_id))
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
