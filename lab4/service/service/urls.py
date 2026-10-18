"""URL-конфигурация проекта service (лабораторная работа № 4).

Адрес страницы одной записи обязан нести ключ (id), поэтому используются
регулярные выражения с именованной группой. В Django 2.0+ функция path()
регулярных выражений не принимает — для них существует re_path()
(в методичке пример записан через path(), что в актуальных версиях не работает).
"""
from django.contrib import admin
from django.urls import path, re_path

from maintenance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # главная: список всех фактов ремонта
    path('', views.archive, name='archive'),
    # анализ: сколько раз ремонтировался каждый станок
    path('machines/', views.machines_list, name='machines_list'),
    # страница одного факта ремонта: /repair/5/
    re_path(r'^repair/(?P<repair_id>\d+)$', views.get_repair, name='get_repair'),
    # страница станка с историей ремонтов: /machine/3/
    re_path(r'^machine/(?P<machine_id>\d+)$', views.get_machine, name='get_machine'),
]
