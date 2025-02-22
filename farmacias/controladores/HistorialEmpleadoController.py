from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from farmacias.models import HistorialEmpleado
from farmacias.controladores.GestionUsuarios import *
from django.contrib.auth.decorators import login_required
from farmacias.controladores.GestionUsuarios import role_required

class HistorialEmpleadoForm(forms.ModelForm):
    class Meta:
        model = HistorialEmpleado
        fields = '__all__'

@role_required(['admin'])
@login_required
def get_historial(request, sucursal=None):
    historiales = HistorialEmpleado.objects.all()

    if sucursal:
        historiales = historiales.filter(sucursal=sucursal)

    return render(request, 'admin/GestionHistorialEmpleado.html', {'historiales': historiales})