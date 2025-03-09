import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from farmacias.models import Compra, Pedido, CompraItem, PedidoItem

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
