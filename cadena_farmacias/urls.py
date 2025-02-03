"""
URL configuration for cadena_farmacias project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from farmacias.views import *
from farmacias.controladores.GestionUsuarios import *
from farmacias.controladores.LaboratorioController import *
from farmacias.controladores.MedicamentosController import *

urlpatterns = [ 
    #USUARIOS 
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', inicio_publico, name='inicio_publico'),  
    path('admin/',inicio_admin, name='inicio_admin'),
    path('farmaceutico/',inicio_farmaceutico, name='inicio_farmaceutico'),
    path('registrar_empleado/', registrar_empleado, name='registrar_empleado'),

    #LABORATORIOS
    path('gestion_laboratorios/', gestion_laboratorios , name='gestion_laboratorios'),
    path('agregar-laboratorio/', agregar_laboratorio, name='agregar_laboratorio'),
    path('editar-laboratorio/<int:pk>/', editar_laboratorio, name='editar_laboratorio'),
    path('eliminar-laboratorio/<int:pk>/', eliminar_laboratorio, name='eliminar_laboratorio'),

    #MEDICAMENTOS
    path('gestion_medicamentos/', gestion_medicamentos, name='gestion_medicamentos'),
    path('agregar-medicamento/', agregar_medicamento, name='agregar_medicamento'),
    path('editar-medicamento/<int:pk>/', editar_medicamento, name='editar_medicamento'),
    path('eliminar-medicamento/<int:pk>/', eliminar_medicamento, name='eliminar_medicamento'),
]