import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from farmacias.models import Compra, Pedido, Empleado, HistorialEmpleado, Sucursal

def factura_compra_pdf(request, compra_id):
    """
    Genera la factura de compra en PDF.
    
    Se consulta la compra (modelo Compra) y se recorren sus items (modelo CompraItem, relacionado por related_name='items').
    La plantilla 'factura_compra.html' debe estar creada y ubicada en tu directorio de plantillas.
    """
    # Obtenemos la compra o devolvemos 404 si no existe
    compra = get_object_or_404(Compra, id=compra_id)
    
    # Preparamos una lista de items con sus totales (cada item es un diccionario)
    items_qs = compra.items.all()  # Asumiendo que en CompraItem definiste related_name='items'
    items = []
    for item in items_qs:
        total_item = item.medicamento.precio * item.cantidad
        items.append({
            'medicamento': item.medicamento,
            'cantidad': item.cantidad,
            'precio_unitario': item.medicamento.precio,
            'total': total_item,
        })
    
    context = {
        'compra': compra,
        'items': items,
        'fecha_actual': datetime.date.today(),
    }
    
    # Renderizamos la plantilla a una cadena HTML
    html_string = render_to_string('pdfs/factura_compra.html', context, request=request)
    
    # Usamos WeasyPrint para convertir el HTML en PDF.
    # El parámetro base_url ayuda a resolver rutas relativas (por ejemplo, a archivos estáticos).
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()
    
    # Preparamos la respuesta HTTP para forzar la descarga del PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FacturaCompra_{compra_id}.pdf"'
    return response

# Nota: Para que este código funcione, necesitas instalar WeasyPrint en tu entorno virtual:
# pip install WeasyPrint

def factura_pedido_pdf(request, pedido_id):
    """
    Genera la factura de un pedido en PDF.
    
    Se consulta el pedido (modelo Pedido) y se recorren sus items (modelo PedidoItem, relacionado por related_name='items').
    La plantilla 'factura_pedido.html' debe estar creada y ubicada en tu directorio de plantillas.
    """
    # Obtenemos el pedido o devolvemos 404 si no existe
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    # Preparamos una lista de items con sus totales (cada item es un diccionario)
    items_qs = pedido.items.all()  # Asumiendo que en PedidoItem definiste related_name='items'
    items = []
    for item in items_qs:
        total_item = item.medicamento.precio * item.cantidad
        items.append({
            'medicamento': item.medicamento,
            'cantidad': item.cantidad,
            'precio_unitario': item.medicamento.precio,
            'total': total_item,
        })
    
    context = {
        'pedido': pedido,
        'items': items,
        'fecha_actual': datetime.date.today(),
    }
    
    # Renderizamos la plantilla a una cadena HTML
    html_string = render_to_string('pdfs/factura_pedido.html', context, request=request)
    
    # Usamos WeasyPrint para convertir el HTML en PDF.
    # El parámetro base_url ayuda a resolver rutas relativas (por ejemplo, a archivos estáticos).
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()
    
    # Preparamos la respuesta HTTP para forzar la descarga del PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="FacturaPedido_{pedido_id}.pdf"'
    return response

def constancia_trabajo_pdf(request, empleado_id):
    """
    Genera una constancia de trabajo en PDF para un empleado pasante o auxiliar.
    
    La plantilla 'constancia_trabajo.html' debe estar creada y ubicada en tu directorio de plantillas.
    """
    empleado = get_object_or_404(Empleado, cedula=empleado_id)
    
    if empleado.cargo not in ['auxiliar', 'pasante']:
        return HttpResponse("Solo se pueden generar constancias para auxiliares o pasantes.", status=400)
    
    context = {
        'empleado': empleado,
        'fecha_actual': datetime.date.today(),
    }
    
    html_string = render_to_string('pdfs/constancia_trabajo.html', context, request=request)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ConstanciaTrabajo_{empleado_id}.pdf"'
    return response

def historial_trabajo_pdf(request, empleado_id):
    """
    Genera el historial de trabajo en PDF de un empleado.
    
    La plantilla 'historial_trabajo.html' debe estar creada y ubicada en tu directorio de plantillas.
    """
    empleado = get_object_or_404(Empleado, cedula=empleado_id)
    historial = HistorialEmpleado.objects.filter(empleado=empleado).order_by('fecha_inicio')
    
    context = {
        'empleado': empleado,
        'historial': historial,
        'fecha_actual': datetime.date.today(),
    }
    
    html_string = render_to_string('pdfs/historial_trabajo.html', context, request=request)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="HistorialTrabajo_{empleado_id}.pdf"'
    return response

def rotacion_personal_pdf(request, sucursal_id):
    """
    Genera un reporte en PDF de la rotación de personal de una sucursal específica.
    
    La plantilla 'rotacion_personal.html' debe estar creada y ubicada en tu directorio de plantillas.
    """
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    rotacion = HistorialEmpleado.objects.filter(sucursal=sucursal).order_by('fecha_inicio')
    
    context = {
        'sucursal': sucursal,
        'rotacion': rotacion,
        'fecha_actual': datetime.date.today(),
    }
    
    html_string = render_to_string('pdfs/rotacion_personal.html', context, request=request)
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    pdf_file = html.write_pdf()
    
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="RotacionPersonal_{sucursal_id}.pdf"'
    return response