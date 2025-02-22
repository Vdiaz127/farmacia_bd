from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from farmacias.models import Empleado, Pedido
from farmacias.controladores.GestionUsuarios import role_required




@login_required
# @role_required(['farmaceutico'])
def inicio_farmaceutico(request):
    empleado = request.user
    pedidos = Pedido.objects.filter(empleado=empleado)

    context = {
        'empleado': empleado,
        'pedidos': pedidos
    }

    return render(request, 'farmaceutico/inicio.html', context)