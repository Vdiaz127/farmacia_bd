
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from farmacias.models import Laboratorio, Medicamento, Pedido, PedidoItem, FORMA_PAGO_CHOICES, MedicamentoLaboratorio
from django.contrib.auth.decorators import login_required
from farmacias.controladores.GestionUsuarios import role_required
import json

@login_required
@role_required(['farmaceutico'])
def crear_pedido(request):
    if request.method == 'POST':
        laboratorio_id = request.POST.get('laboratorio')
        medicamentos_ids = request.POST.getlist('medicamentos')
        forma_pago = request.POST.get('forma_pago')

        if not laboratorio_id or not medicamentos_ids or not forma_pago:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect(reverse('crear_pedido'))

        laboratorio = Laboratorio.objects.get(id=laboratorio_id)
        empleado = request.user
        sucursal = empleado.sucursal

        pedido = Pedido.objects.create(
            sucursal=sucursal,
            empleado=empleado,
            laboratorio=laboratorio,
            fecha_pedido=timezone.now(),
            forma_pago=forma_pago
        )

        for medicamento_id in medicamentos_ids:
            cantidad = request.POST.get(f'cantidades_{medicamento_id}')
            if cantidad:
                medicamento = Medicamento.objects.get(id=medicamento_id)
                PedidoItem.objects.create(
                    pedido=pedido,
                    medicamento=medicamento,
                    cantidad=cantidad
                )

        messages.success(request, "Pedido realizado con éxito.")
        return redirect(reverse('inicio_farmaceutico'))
    

    laboratorios = Laboratorio.objects.all()
    medicamentos_laboratorios = MedicamentoLaboratorio.objects.select_related('medicamento', 'laboratorio').all()
    forma_pago_choices = FORMA_PAGO_CHOICES
    

    context = {
    'laboratorios': laboratorios,
    'medicamentos': json.dumps(list(Medicamento.objects.values('id', 'nombre'))),  # Asegurar formato JSON
    'medicamentos_laboratorios': json.dumps(list(medicamentos_laboratorios.values('medicamento_id', 'laboratorio_id'))),
    'forma_pago_choices': forma_pago_choices
}


    return render(request, 'farmaceutico/Pedido.html', context)

@login_required
@role_required(['farmaceutico'])
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        medicamentos_ids = request.POST.getlist('medicamentos')
        forma_pago = request.POST.get('forma_pago')

        if not medicamentos_ids or not forma_pago:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect(reverse('editar_pedido', args=[pedido_id]))

        pedido.forma_pago = forma_pago
        pedido.save()

        PedidoItem.objects.filter(pedido=pedido).delete()
        for medicamento_id in medicamentos_ids:
            cantidad = request.POST.get(f'cantidades_{medicamento_id}')
            if cantidad:
                medicamento = Medicamento.objects.get(id=medicamento_id)
                PedidoItem.objects.create(
                    pedido=pedido,
                    medicamento=medicamento,
                    cantidad=cantidad
                )

        messages.success(request, "Pedido actualizado con éxito.")
        return redirect(reverse('inicio_farmaceutico'))

    laboratorios = Laboratorio.objects.all()
    medicamentos_laboratorios = MedicamentoLaboratorio.objects.filter(laboratorio=pedido.laboratorio).select_related('medicamento')
    medicamentos = Medicamento.objects.filter(id__in=medicamentos_laboratorios.values('medicamento_id'))
    forma_pago_choices = FORMA_PAGO_CHOICES

    context = {
        'pedido': pedido,
        'laboratorios': laboratorios,
        'medicamentos': medicamentos,
        'forma_pago_choices': forma_pago_choices,
        'selected_medicamentos': list(pedido.items.values_list('medicamento_id', flat=True)),
        'selected_cantidades': {item.medicamento_id: item.cantidad for item in pedido.items.all()}
    }

    return render(request, 'farmaceutico/EditarPedido.html', context)

@login_required
@role_required(['farmaceutico'])
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    pedido.delete()
    messages.success(request, "Pedido eliminado con éxito.")
    return redirect(reverse('inicio_farmaceutico'))