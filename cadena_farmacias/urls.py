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
from farmacias.controladores.SucursalesController import *
from farmacias.controladores.MedicamentoSucursalController import *
from farmacias.controladores.MonodrogaController import *


from farmacias.controladores.farmaceutico.InicioFarmaceuticoController import *
from farmacias.controladores.farmaceutico.PedidosController import *


urlpatterns = [ 
    
    #PUBLICO
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', consulta_medicamento, name='inicio_publico'),  
    path('registrar_empleado/', registrar_empleado, name='registrar_empleado'),
    path('sucursal/<int:pk>/', perfil_sucursal, name='perfil_sucursal'),

    #USUARIO: ADMINISTRADOR
    path('admin/',inicio_admin, name='inicio_admin'),
    path('farmaceutico/',inicio_farmaceutico, name='inicio_farmaceutico'),

    #LABORATORIOS
    path('gestion_laboratorios/', gestion_laboratorios , name='gestion_laboratorios'),
    path('agregar-laboratorio/', agregar_laboratorio, name='agregar_laboratorio'),
    path('editar-laboratorio/<int:pk>/', editar_laboratorio, name='editar_laboratorio'),
    path('eliminar-laboratorio/<int:pk>/', eliminar_laboratorio, name='eliminar_laboratorio'),

    #MONODROGAS
    path('monodrogas/', listar_monodrogas, name='listar_monodrogas'),
    path('monodrogas/agregar/', agregar_monodroga, name='agregar_monodroga'),
    path('monodrogas/editar/<int:pk>/', editar_monodroga, name='editar_monodroga'),
    path('monodrogas/eliminar/<int:pk>/', eliminar_monodroga, name='eliminar_monodroga'),

    #MEDICAMENTOS
    path('gestion_medicamentos/', gestion_medicamentos, name='gestion_medicamentos'),
    path('agregar-medicamento/', agregar_medicamento, name='agregar_medicamento'),
    path('editar-medicamento/<int:pk>/', editar_medicamento, name='editar_medicamento'),
    path('eliminar-medicamento/<int:pk>/', eliminar_medicamento, name='eliminar_medicamento'),

    #SUCURSALES
    path('gestion_sucursales/', sucursal_get, name='gestion_sucursales'),
    path('agregar-sucursales/', agregar_sucursal, name='agregar_sucursal'),
    path('editar-sucursales/<int:pk>/', editar_sucursal, name='editar_sucursal'),
    path('eliminar-sucursales/<int:pk>/', eliminar_sucursal, name='eliminar_sucursal'),

    #MEDICAMENTOS EN SUCURSALES
    path('gestion_medicamento_sucursal/<int:pk>', gestion_medicamento_sucursal, name='gestion_medicamento_sucursal'),
    path('agregar_medicamento_sucursal/', agregar_medicamento_sucursal, name='agregar_medicamento_sucursal'),


    #USUARIO: FARMAUCETICO
    path('farmaceutico/', inicio_farmaceutico, name='inicio_farmaceutico'),
    path('crear_pedido/', crear_pedido, name='crear_pedido'),
    path('editar_pedido/<int:pedido_id>/', editar_pedido, name='editar_pedido'),
    path('eliminar_pedido_pedido/<int:pedido_id>/', eliminar_pedido, name='eliminar_pedido'),
   
]