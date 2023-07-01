from django.http import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors


def generate_shopping_list_pdf(request, shopping_list):
    """
    Функция создающая и отправляющая пользователю PDF со списком покупок.
    """

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"')

    file = canvas.Canvas(response, pagesize=letter)
    file.setFont("Geologica", 22)
    file.setFillColor(colors.black)
    file.rect(0, 0, file._pagesize[0], 100, fill=True)
    file.setFillColor(colors.black)

    title_text = "Корзина покупок"

    file.drawString(30, 700, title_text)
    file.setFont("Geologica", 16)
    x = 50
    y = 650
    for item in shopping_list:
        file.drawString(
            x,
            y,
            (f"•  {item.get('name')}    "
             f"{item.get('amount')}  {item.get('measurement_unit')}")
        )
        y -= 20
    file.setFillColor(colors.white)
    file.drawString(30, 45, 'Продуктовый помощник')
    file.showPage()
    file.save()

    return response
