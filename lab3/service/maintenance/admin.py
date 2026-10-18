from django.contrib import admin

from .models import (Brand, Country, Enterprise, Machine, MachineType,
                     Repair, RepairType)


class RepairInline(admin.TabularInline):
    """Ремонты станка прямо на странице станка (история ремонтов)."""
    model = Repair
    extra = 0
    fields = ('repair_type', 'start_date', 'end_date', 'author')
    readonly_fields = ('author',)


class MachineAdmin(admin.ModelAdmin):
    list_display = ('inventory_no', 'repairs_count', 'total_repair_cost',
                    'machine_type', 'brand', 'release_year', 'enterprise',
                    'last_repair_date')
    list_filter = ('machine_type', 'brand__country', 'release_year', 'enterprise')
    search_fields = ('inventory_no',)
    inlines = [RepairInline]


class RepairAdmin(admin.ModelAdmin):
    list_display = ('machine', 'repair_type', 'start_date', 'end_date',
                    'duration_actual', 'get_excerpt', 'author', 'created_date')
    list_filter = ('repair_type', 'machine__machine_type', 'start_date')
    search_fields = ('machine__inventory_no',)
    date_hierarchy = 'start_date'


admin.site.register(Country)
admin.site.register(MachineType)
admin.site.register(Brand)
admin.site.register(Enterprise)
admin.site.register(RepairType)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Repair, RepairAdmin)
