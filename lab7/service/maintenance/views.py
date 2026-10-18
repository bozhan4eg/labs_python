from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
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
    """Форма нового факта ремонта (аналог create_post из методички)."""
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
            for value, key in ((form['start_date'], 'start'), (form['end_date'], 'end')):
                try:
                    parsed = datetime.strptime(value, '%Y-%m-%d').date()
                except (ValueError, TypeError):
                    parsed = None
                if key == 'start':
                    start_date = parsed
                else:
                    end_date = parsed
            if start_date is None or end_date is None:
                errors.append('Даты указаны некорректно.')
            elif end_date < start_date:
                errors.append('Дата окончания не может быть раньше даты начала.')

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


# ---------------------------------------------------------------------------
# Лабораторная работа № 6: регистрация, авторизация, выход
# ---------------------------------------------------------------------------
def register(request):
    """Форма и представление регистрации нового пользователя."""
    if request.method == 'POST':
        form = {
            'username': request.POST.get('username', ''),
            'email': request.POST.get('email', ''),
            'password1': request.POST.get('password1', ''),
            'password2': request.POST.get('password2', ''),
        }
        errors = []
        if not form['username'] or not form['password1']:
            errors.append('Не все поля заполнены.')
        try:
            User.objects.get(username=form['username'])
            errors.append('Пользователь с таким именем уже зарегистрирован.')
        except User.DoesNotExist:
            pass
        if form['password1'] != form['password2']:
            errors.append('Пароли не совпадают.')
        if errors:
            form['errors'] = errors
            return render(request, 'register.html', {'form': form})
        User.objects.create_user(form['username'], form['email'], form['password1'])
        return redirect('login_page')
    return render(request, 'register.html', {})


def login_page(request):
    """Форма и представление авторизации зарегистрированного пользователя."""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        form = {'username': username}
        if not username or not password:
            form['errors'] = ['Не все поля заполнены.']
            return render(request, 'login.html', {'form': form})
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('archive')
        form['errors'] = ['Такого аккаунта не существует или пароль неверен.']
        return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    return redirect('archive')
