from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
from django.http import HttpResponse

def render_to_pdf(funtion):
    def wrapper(*args, **kwargs):
        template_name, context_data= funtion(*args, **kwargs)
        template = get_template(template_name)
        html = template.render(context_data)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return HttpResponse("Error Rendering PDF", status=400)
    return wrapper