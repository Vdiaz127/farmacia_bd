from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from farmacias.models import Pedido, Laboratorio, Compra, CompraItem, Medicamento_Sucursal
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@csrf_exempt  # Solo si no usas protección CSRF en formularios simples
def procesar_pedido(request):
    if request.method == "POST":
        email = request.POST.get("email")
        especialPassword = request.POST.get("especialPassword")
        laboratorio = Laboratorio.objects.filter(email=email, especialPassword=especialPassword).first()

        if not laboratorio:
            return JsonResponse({"error": "Credenciales inválidas"}, status=403)

        # Obtener pedidos del laboratorio autenticado
        pedidos = Pedido.objects.filter(laboratorio=laboratorio)
        return render(request, "laboratorio/GestionCompras.html", {"pedidos": pedidos, "laboratorio": laboratorio })

    return render(request, "laboratorio/GestionCompras.html")

@csrf_exempt
def procesar_compra(request, pk):
    if request.method == "POST":
        pedido = get_object_or_404(Pedido, id=pk)
        # Crear la compra a partir del pedido
        compra = Compra.objects.create(
            pedido=pedido,
            fecha_compra=timezone.now(),
            monto_total=0,  # Inicialmente en 0, se actualizará más adelante
            forma_pago=pedido.forma_pago
        )
        
        monto_total = 0
        selected_item_ids = request.POST.getlist('items')  # Lista de ids en formato string
        for item in pedido.items.all():
            if str(item.id) in selected_item_ids:
                cantidad = int(request.POST.get(f"cantidad_{item.id}", item.cantidad))
                if cantidad > 0:
                    CompraItem.objects.create(
                        compra=compra,
                        medicamento=item.medicamento,
                        cantidad=cantidad
                    )
                    monto_total += item.medicamento.precio * cantidad

                    # Actualizar el stock de medicamentos en la sucursal
                    medicamento_sucursal, created = Medicamento_Sucursal.objects.get_or_create(
                        medicamento=item.medicamento,
                        sucursal=pedido.sucursal,
                        laboratorio=pedido.laboratorio,
                        defaults={'cantidad': 0}
                    )
                    medicamento_sucursal.cantidad += cantidad
                    medicamento_sucursal.save()
        
        # Actualizar el monto total de la compra
        compra.monto_total = monto_total
        compra.save()
        
        return redirect('laboratorio_procesar_pedido')

    return JsonResponse({"error": "Método no permitido"}, status=405)
