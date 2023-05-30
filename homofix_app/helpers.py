from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import uuid
from django.conf import settings


def save_pdf(params: dict):
    template = get_template("test.html")
    html = template.render(params)
    file_name = f"{uuid.uuid4()}.pdf"
    print("sssss",file_name)

    try:
        with open(str(settings.BASE_DIR) + f'/media/Invoice/{file_name}.pdf', 'wb') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)

        if pdf.err:
            return '', False

    except Exception as e:
        print(e)
        return '', False

    return file_name, True
