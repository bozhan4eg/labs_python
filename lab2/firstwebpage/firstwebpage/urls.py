from django.contrib import admin
from django.urls import path
from flatpages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # главная страница: html-шаблон index.html
    path('', views.home, name='home'),
    # задание 1: по адресу /hello/ возвращается тот же текст, что и на главной
    path('hello/', views.hello, name='hello'),
    # задание 2: тот же текст, но без явного указания типа ответа (сравнение)
    path('hello-html/', views.hello_html, name='hello_html'),
    # страница, оформленная через шаблон static_handler.html + CSS
    path('static-page/', views.static_page, name='static_page'),
]
