"""URL-конфигурация проекта service (лабораторная работа № 6)."""
from django.contrib import admin
from django.urls import path, re_path

from maintenance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.archive, name='archive'),
    path('machines/', views.machines_list, name='machines_list'),
    path('repair/new/', views.create_repair, name='create_repair'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_view, name='logout_page'),
    re_path(r'^repair/(?P<repair_id>\d+)$', views.get_repair, name='get_repair'),
    re_path(r'^machine/(?P<machine_id>\d+)$', views.get_machine, name='get_machine'),
]
