from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from farmacias.controladores.GestionUsuarios import role_required
from farmacias.models import Compra, Pedido, Sucursal
from datetime import timedelta, date
from django.db.models import Sum, Value, Q, F, DecimalField, ExpressionWrapper
from django.db.models.functions import Coalesce

def calculate_due_date(fecha, forma_pago):
    if forma_pago == '30d':
        return fecha + timedelta(days=30)
    elif forma_pago == '15d':
        return fecha + timedelta(days=15)
    elif forma_pago == '5d':
        return fecha + timedelta(days=5)
    else:
        return fecha

@login_required
@role_required(['admin'])
def gestion_deudas(request):
    # Obtención de compras y pedidos que no sean de contado.
    compras_deuda = Compra.objects.exclude(forma_pago='contado')
    pedidos_deuda = Pedido.objects.exclude(forma_pago='contado')
    sucursales = Sucursal.objects.all()

    # Calculamos la fecha de pago para cada registro.
    for compra in compras_deuda:
        compra.fecha_pago = calculate_due_date(compra.fecha_compra, compra.forma_pago)
    for pedido in pedidos_deuda:
        pedido.fecha_pago = calculate_due_date(pedido.fecha_pedido, pedido.forma_pago)

    # Se construye una estructura de datos por sucursal
    deudas = []
    for sucursal in sucursales:
        # Para compras, accedemos a la sucursal mediante compra.pedido.sucursal
        sucursal_compras = [compra for compra in compras_deuda if compra.pedido.sucursal_id == sucursal.id]
        sucursal_pedidos = [pedido for pedido in pedidos_deuda if pedido.sucursal_id == sucursal.id]
        deudas.append({
            'sucursal': sucursal,
            'compras_deuda': sucursal_compras,
            'pedidos_deuda': sucursal_pedidos,
        })

    return render(request, 'admin/GestionDeudas.html', {
        'deudas': deudas,
        'today': date.today(),
    })

