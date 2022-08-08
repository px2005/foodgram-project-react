from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from recipes.models import IngredientAmount


def download_list(request):
    final_list = {}
    ingredients = IngredientAmount.objects.filter(
        recipe__shopping_cart__user=request.user).values_list(
        'ingredient__name', 'ingredient__measurement_unit',
        'amount'
    )
    for item in ingredients:
        name = item[0]
        if name not in final_list:
            final_list[name] = {
                'measurement_unit': item[1],
                'amount': item[2]
            }
        else:
            final_list[name]['amount'] += item[2]
    pdfmetrics.registerFont(
        TTFont('Handicraft', 'data/Handicraft.ttf', 'UTF-8'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.pdf"')
    page = canvas.Canvas(response)
    page.setFont('Handicraft', size=24)
    page.drawString(200, 800, 'Список покупок')
    page.setFont('Handicraft', size=16)
    height = 750
    for i, (name, data) in enumerate(final_list.items(), 1):
        page.drawString(75, height, (f'{i}. {name} - {data["amount"]} '
                                     f'{data["measurement_unit"]}'))
        height -= 25
    page.showPage()
    page.save()
    return response
