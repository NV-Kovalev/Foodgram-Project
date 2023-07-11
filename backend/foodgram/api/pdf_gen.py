from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from foodgram.settings import NUMBER_OF_ITEMS_ON_PDF_PAGE


def generate_shopping_list_pdf(request, shopping_list):
    """Функция создающая и отправляющая пользователю
    PDF со списком покупок."""

    # Вычисляем количество необходимых страниц.
    items_count = len(shopping_list)
    pages_amount = items_count // NUMBER_OF_ITEMS_ON_PDF_PAGE + (
        items_count % NUMBER_OF_ITEMS_ON_PDF_PAGE > 0)

    # Подготавливаем ответ на запрос.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"')

    file = canvas.Canvas(response, pagesize=letter)

    for page in range(pages_amount):

        page_items = []
        count = 0

        while count != NUMBER_OF_ITEMS_ON_PDF_PAGE and any(shopping_list):
            page_items.append(shopping_list.pop())
            count += 1

        # Собираем footer.
        file.setFont("Geologica", 18)
        file.setFillColor(colors.black)
        file.rect(0, 0, file._pagesize[0], 100, fill=True)
        file.setFillColor(colors.white)
        file.drawString(30, 45, 'Продуктовый помощник')

        # Ставим заголовок.
        file.setFillColor(colors.black)
        title_text = "Корзина покупок"
        file.drawString(30, 720, title_text)

        # Нумеруем страницу.
        file.setFont("Geologica", 16)
        file.drawString(300, 120, (str(page + 1)))

        # Наполняем список.
        file.setFont("Geologica", 16)
        x = 50
        y = 650
        for item in page_items:
            file.drawString(
                x,
                y,
                (f"•  {item.get('name')}    "
                 f"{item.get('amount')}  {item.get('measurement_unit')}")
            )
            y -= 20

        # Сохраняем страницу.
        file.showPage()

    # Сохраняем и отправляем файл.
    file.save()
    return response
