from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from farmacias.models import Sucursal
from farmacias.controladores.GestionUsuarios import *
from django.contrib.auth.decorators import login_required

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = '__all__'


@login_required
@role_required(['admin'])
def sucursal_get(request):
    sucursales = Sucursal.objects.all()
    return render(request, 'admin/GestionSucursales.html', {'sucursales': sucursales})


@login_required
@role_required(['admin'])
def agregar_sucursal(request):
    form = SucursalForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('gestion_sucursales')
    return redirect("gestion_sucursales")


@login_required
@role_required(['admin'])
def editar_sucursal(request, pk=None):
    if pk:
        sucursal = get_object_or_404(Sucursal, id=pk)
    else:
        sucursal = None

    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            return redirect('gestion_sucursales')
    else:
        form = SucursalForm(instance=sucursal)

    return redirect("gestion_sucursales")

@login_required
@role_required(['admin'])
def eliminar_sucursal(request, pk):
    sucursal = Sucursal.objects.get(pk=pk)
    sucursal.delete()
    messages.success(request, "sucursal eliminado correctamente.")
    return redirect('gestion_sucursales')
