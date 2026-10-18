"""URL-конфигурация проекта service (лабораторная работа № 5)."""
from django.contrib import admin
from django.urls import path, re_path

from maintenance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
    path('machines/', views.machines_list, name='machines_list'),
    # форма нового факта ремонта (должна идти раньше /repair/<id>/)
    path('repair/new/', views.create_repair, name='create_repair'),
    re_path(r'^repair/(?P<repair_id>\d+)$', views.get_repair, name='get_repair'),
    re_path(r'^machine/(?P<machine_id>\d+)$', views.get_machine, name='get_machine'),
]
