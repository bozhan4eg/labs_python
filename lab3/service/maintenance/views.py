from django.shortcuts import render

from .models import Repair


def archive(request):
    """Главная страница: список всех фактов ремонта (журнал ремонтов)."""
    return render(request, 'archive.html', {'repairs': Repair.objects.all()})
