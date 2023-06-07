from django.http import HttpResponse


def working(request):
    return HttpResponse('Работает')
