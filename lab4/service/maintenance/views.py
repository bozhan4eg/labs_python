from django.db.models import Count, Sum
from django.http import Http404
from django.shortcuts import render

from .models import Machine, Repair


def archive(request):
    """Главная страница: список всех фактов ремонта (журнал ремонтов)."""
    return render(request, 'archive.html', {'repairs': Repair.objects.all()})


def get_repair(request, repair_id):
    """Страница одного факта ремонта (адрес вида /repair/5/)."""
    try:
        repair = Repair.objects.get(id=repair_id)
        return render(request, 'repair.html', {'post': repair})
    except Repair.DoesNotExist:
        raise Http404


def get_machine(request, machine_id):
    """Страница станка: сколько раз ремонтировался, история и стоимость ремонтов."""
    try:
        machine = Machine.objects.get(id=machine_id)
        repairs = machine.repairs.select_related('repair_type').order_by('-start_date')
        return render(request, 'machine.html', {
            'machine': machine,
            'repairs': repairs,
            'repairs_count': machine.repairs_count,
            'total_cost': machine.total_repair_cost,
        })
    except Machine.DoesNotExist:
        raise Http404


def machines_list(request):
    """Анализ: список станков с числом ремонтов (по убыванию)."""
    machines = (Machine.objects
                .select_related('machine_type', 'brand', 'brand__country', 'enterprise')
                .annotate(repairs_num=Count('repairs'),
                          total_cost=Sum('repairs__repair_type__cost'))
                .order_by('-repairs_num', 'inventory_no'))
    return render(request, 'machines.html', {'machines': machines})
