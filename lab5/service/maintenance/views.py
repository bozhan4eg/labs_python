from datetime import datetime

from django.db.models import Count, Sum
from django.http import Http404
from django.shortcuts import redirect, render

from .models import Machine, Repair, RepairType


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


def create_repair(request):
    """Форма нового факта ремонта (анлог create_post из методички).

    GET  — вернуть страницу с формой;
    POST — проверить данные и сохранить запись в базу.
    """
    # в Django 2+ is_anonymous — свойство, а не метод (в методичке — вызов метода)
    if not request.user.is_anonymous:
        machines = Machine.objects.all()
        repair_types = RepairType.objects.all()

        if request.method == 'POST':
            form = {
                'machine': request.POST.get('machine', ''),
                'repair_type': request.POST.get('repair_type', ''),
                'start_date': request.POST.get('start_date', ''),
                'end_date': request.POST.get('end_date', ''),
                'comment': request.POST.get('comment', ''),
            }
            errors = []

            machine = Machine.objects.filter(id=form['machine']).first()
            repair_type = RepairType.objects.filter(id=form['repair_type']).first()
            if machine is None:
                errors.append('Не выбран станок.')
            if repair_type is None:
                errors.append('Не выбран вид ремонта.')

            start_date = end_date = None
            for field, key in ((form['start_date'], 'start_date'),
                               (form['end_date'], 'end_date')):
                try:
                    value = datetime.strptime(field, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    value = None
                if key == 'start_date':
                    start_date = value
                else:
                    end_date = value
            if start_date is None or end_date is None:
                errors.append('Даты указаны некорректно.')
            elif end_date < start_date:
                errors.append('Дата окончания не может быть раньше даты начала.')

            # задание: проверка уникальности (станок + дата начала)
            if machine is not None and start_date is not None and \
                    Repair.objects.filter(machine=machine,
                                          start_date=start_date).exists():
                errors.append('На этот станок уже оформлен ремонт с такой датой начала.')

            if errors:
                form['errors'] = errors
                return render(request, 'create_repair.html',
                              {'form': form, 'machines': machines,
                               'repair_types': repair_types})

            repair = Repair.objects.create(
                machine=machine, repair_type=repair_type,
                start_date=start_date, end_date=end_date,
                comment=form['comment'], author=request.user)
            return redirect('get_repair', repair_id=repair.id)

        return render(request, 'create_repair.html',
                      {'machines': machines, 'repair_types': repair_types})
    else:
        raise Http404
