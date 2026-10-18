"""URL-конфигурация проекта service.

Задание лабораторной работы № 3: указать Django, что при заходе пользователя
на главную страницу нужно отображать список всех записей модели Repair.
"""
from django.contrib import admin
from django.urls import path

from maintenance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
]
