from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    """Главная страница: рендеринг html-шаблона index.html."""
    return render(request, 'templates/index.html')


def hello(request):
    """Задание 1: по адресу /hello/ возвращается тот же текст, что и на главной.

    Тип ответа указан явно — «text/plain», браузер показывает строку как есть.
    """
    return HttpResponse(u'Привет, Мир!', content_type="text/plain")


def hello_html(request):
    """Задание 2: то же самое, но БЕЗ указания типа ответа.

    Класс HttpResponse выставляет тип по умолчанию — «text/html; charset=utf-8»,
    поэтому браузер трактует строку как HTML-документ.
    """
    return HttpResponse(u'Привет, Мир!')


def static_page(request):
    """Страница, оформленная шаблоном static_handler.html и файлом index.css."""
    return render(request, 'templates/static_handler.html')
