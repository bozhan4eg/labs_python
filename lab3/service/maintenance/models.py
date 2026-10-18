# -*- coding: utf-8 -*-
"""
Модели данных предметной области «Техническое обслуживание станков» (задача 13).

Компания занимается ремонтом станков и другого оборудования; клиенты —
промышленные предприятия. Все станки классифицированы по типам,
странам-производителям, годам выпуска и маркам. Все виды ремонта отличаются
названием, продолжительностью в днях и стоимостью. По каждому факту ремонта
фиксируются станок (вид станка), дата начала и дата окончания ремонта.
Кроме того, требуется хранить информацию о том, сколько раз ремонтировался
тот или иной станок.
"""
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Country(models.Model):
    """Страна-производитель станка (одна из классификаций)."""
    name = models.CharField('страна', max_length=100, unique=True)

    class Meta:
        verbose_name = 'страна-производитель'
        verbose_name_plural = 'страны-производители'
        ordering = ['name']

    def __str__(self):
        return self.name


class MachineType(models.Model):
    """Тип станка: токарный, фрезерный, шлифовальный и т. д."""
    name = models.CharField('тип станка', max_length=100, unique=True)
    description = models.TextField('описание', blank=True)

    class Meta:
        verbose_name = 'тип станка'
        verbose_name_plural = 'типы станков'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Марка станка (привязана к стране-производителю)."""
    name = models.CharField('марка', max_length=120)
    country = models.ForeignKey(Country, verbose_name='страна-производитель',
                                on_delete=models.CASCADE, related_name='brands')

    class Meta:
        verbose_name = 'марка станка'
        verbose_name_plural = 'марки станков'
        ordering = ['name']
        unique_together = ('name', 'country')

    def __str__(self):
        return self.name


class Enterprise(models.Model):
    """Промышленное предприятие — клиент компании, владелец оборудования."""
    name = models.CharField('предприятие', max_length=200)
    city = models.CharField('город', max_length=80, blank=True)

    class Meta:
        verbose_name = 'предприятие-клиент'
        verbose_name_plural = 'предприятия-клиенты'
        ordering = ['name']

    def __str__(self):
        return self.name


class Machine(models.Model):
    """Единица оборудования (станок), закреплённая за предприятием-клиентом."""
    inventory_no = models.CharField('инвентарный номер', max_length=30, unique=True)
    machine_type = models.ForeignKey(MachineType, verbose_name='тип станка',
                                     on_delete=models.PROTECT, related_name='machines')
    brand = models.ForeignKey(Brand, verbose_name='марка',
                              on_delete=models.PROTECT, related_name='machines')
    release_year = models.PositiveSmallIntegerField(
        'год выпуска',
        validators=[MinValueValidator(1950), MaxValueValidator(timezone.now().year)])
    enterprise = models.ForeignKey(Enterprise, verbose_name='предприятие-клиент',
                                   on_delete=models.PROTECT, related_name='machines')

    class Meta:
        verbose_name = 'станок'
        verbose_name_plural = 'станки'
        ordering = ['inventory_no']

    def __str__(self):
        return '%s (%s, %s)' % (self.inventory_no, self.machine_type.name, self.brand.name)

    # ------------------------------------------------------------------
    # Анализ: сколько раз ремонтировался станок
    # ------------------------------------------------------------------
    @property
    def repairs_count(self):
        """Количество ремонтов данного станка."""
        return self.repairs.count()

    @property
    def total_repair_cost(self):
        """Суммарная стоимость всех ремонтов станка, руб."""
        return sum(r.repair_type.cost for r in self.repairs.all())

    @property
    def last_repair_date(self):
        """Дата окончания последнего ремонта (или None)."""
        last = self.repairs.order_by('-end_date').first()
        return last.end_date if last else None

    @property
    def country(self):
        """Страна-производитель (через марку)."""
        return self.brand.country


class RepairType(models.Model):
    """Вид ремонта: название, продолжительность в днях, стоимость."""
    name = models.CharField('вид ремонта', max_length=120, unique=True)
    duration_days = models.PositiveSmallIntegerField('продолжительность, дн.')
    cost = models.DecimalField('стоимость, руб.', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'вид ремонта'
        verbose_name_plural = 'виды ремонта'
        ordering = ['-duration_days']

    def __str__(self):
        return self.name


class Repair(models.Model):
    """Факт ремонта: станок, вид ремонта, дата начала и дата окончания."""
    machine = models.ForeignKey(Machine, verbose_name='станок',
                                on_delete=models.CASCADE, related_name='repairs')
    repair_type = models.ForeignKey(RepairType, verbose_name='вид ремонта',
                                    on_delete=models.PROTECT, related_name='repairs')
    start_date = models.DateField('дата начала')
    end_date = models.DateField('дата окончания')
    author = models.ForeignKey(User, verbose_name='заявку оформил',
                               on_delete=models.CASCADE, related_name='repairs')
    comment = models.TextField('примечание (выполненные работы)', blank=True)
    created_date = models.DateField('дата оформления заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'факт ремонта'
        verbose_name_plural = 'факты ремонта'
        ordering = ['-start_date']
        unique_together = ('machine', 'start_date')

    def __str__(self):
        return '%s: %s' % (self.machine, self.repair_type.name)

    def get_excerpt(self):
        """Как в методичке: первые 140 символов примечания для списка."""
        return self.comment[:140] + '...' if len(self.comment) > 140 else self.comment

    @property
    def duration_actual(self):
        """Фактическая продолжительность ремонта, дней."""
        return (self.end_date - self.start_date).days + 1

    @property
    def planned_end_date(self):
        """Плановая дата окончания = начало + продолжительность вида ремонта."""
        return self.start_date + timedelta(days=self.repair_type.duration_days - 1)

    @property
    def is_delayed(self):
        """Ремонт занял больше дней, чем предусмотрено нормативом."""
        return self.duration_actual > self.repair_type.duration_days

    def get_absolute_url(self):
        return reverse('get_repair', kwargs={'repair_id': self.id})
