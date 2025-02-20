from django.shortcuts import render, get_object_or_404
from farmacias.controladores.GestionUsuarios import role_required
from farmacias.models import Sucursal, Medicamento_Sucursal
from django.contrib.auth.decorators import login_required
from farmacias.controladores.GestionUsuarios import *

from farmacias.models import Medicamento_Sucursal

def consulta_medicamento(request):
    query = request.GET.get('q', '')
    resultados = None
    if query:
        # Se filtran los registros de Medicamento_Sucursal por el nombre del medicamento
        resultados = Medicamento_Sucursal.objects.filter(
            medicamento__nombre__icontains=query
        ).select_related('sucursal', 'medicamento', 'laboratorio')
    return render(request, 'publico/ConsultaMedicamento.html', {
        'query': query,
        'resultados': resultados
    })

@login_required
@role_required(['admin'])
def inicio_admin(request): 
    return render(request, 'admin/inicio.html', {'empleado': request.user})

# @login_required
# @role_required(['farmaceutico'])
# def inicio_farmaceutico(request):
#     return render(request, 'farmaceutico/inicio.html', {'empleado': request.user})




def perfil_sucursal(request, pk):
    # Obtiene la sucursal o devuelve 404 si no existe
    sucursal = get_object_or_404(Sucursal, pk=pk)
    # Obtiene todos los empleados asociados a esta sucursal (relación definida con related_name="empleados")
    empleados = sucursal.empleados.all()
    # Obtiene el stock de medicamentos en la sucursal, trayendo además el medicamento y el laboratorio relacionado
    medicamentos = Medicamento_Sucursal.objects.filter(sucursal=sucursal).select_related('medicamento', 'laboratorio')
    
    context = {
        'sucursal': sucursal,
        'empleados': empleados,
        'medicamentos': medicamentos,
    }
    return render(request, 'publico/PerfilSucursal.html', context)
