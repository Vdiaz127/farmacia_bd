# from xhtml2pdf import pisa
# from io import BytesIO
# from django.template.loader import get_template
from django.http import HttpResponse
from wkhtmltopdf.views import PDFTemplateResponse

# def render_to_pdf(funtion):
#     def wrapper(*args, **kwargs):
#         template_name, context_data= funtion(*args, **kwargs)
#         template = get_template(template_name)
#         html = template.render(context_data)
#         result = BytesIO()
#         pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
#         if not pdf.err:
#             return HttpResponse(result.getvalue(), content_type='application/pdf')
#         return HttpResponse("Error Rendering PDF", status=400)
#     return wrapper

def render_to_pdf_wkhtmltopdf(request, template_name, context_data):
    pdf = PDFTemplateResponse(
        request=request,
        template=template_name,
        context=context_data,
        show_content_in_browser=True,
        filename="Test.pdf",
    )
    return pdf
