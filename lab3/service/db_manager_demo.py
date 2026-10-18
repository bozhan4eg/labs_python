# -*- coding: utf-8 -*-
"""
Лабораторная работа № 3, задание 2.

Работа с файлом базы данных SQLite в обход Django: открытие файла БД,
просмотр созданных через админ-панель записей, изменение текста одной записи,
изменение «названия» (вида ремонта) другой записи и создание новой записи
напрямую в таблице (то же самое можно сделать в SQLite Manager /
DB Browser for SQLite).

Запуск:  python3 db_manager_demo.py
"""
import os
import sqlite3

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'service.settings')
django.setup()

from django.conf import settings  # noqa: E402

DB = str(settings.DATABASES['default']['NAME'])
print('$ sqlite3 %s' % os.path.basename(DB))
con = sqlite3.connect(DB)
cur = con.cursor()

print("sqlite> .tables")
rows = cur.execute("SELECT name FROM sqlite_master WHERE type='table' "
                   "ORDER BY name").fetchall()
print('  ' + '  '.join(r[0] for r in rows))

print()
print("sqlite> SELECT id, machine_id, repair_type_id, start_date, end_date")
print("   ...>   FROM maintenance_repair ORDER BY id DESC LIMIT 4;")
for r in cur.execute("SELECT id, machine_id, repair_type_id, start_date, end_date "
                     "FROM maintenance_repair ORDER BY id DESC LIMIT 4"):
    print('|'.join(str(x) for x in r))

print()
print('-- 1) изменяем текст (примечание) записи id=15')
print("sqlite> UPDATE maintenance_repair SET comment = ")
print("   ...>   'Замена ремней привода, регулировка суппорта, замена масла в СУП.'")
print("   ...>   WHERE id = 15;")
cur.execute("UPDATE maintenance_repair SET comment = ? WHERE id = 15",
            ('Замена ремней привода, регулировка суппорта, замена масла в СУП.',))
print('rows affected: %d' % cur.rowcount)

print()
print('-- 2) изменяем «название» (вид ремонта) записи id=16 на «Диагностика и дефектовка»')
print("sqlite> UPDATE maintenance_repair SET repair_type_id = ")
print("   ...>   (SELECT id FROM maintenance_repairtype WHERE name = 'Диагностика и дефектовка'),")
print("   ...>   end_date = '2026-09-07'")
print("   ...>   WHERE id = 16;")
cur.execute("UPDATE maintenance_repair SET repair_type_id = "
            "(SELECT id FROM maintenance_repairtype WHERE name = 'Диагностика и дефектовка'), "
            "end_date = '2026-09-07' WHERE id = 16")
print('rows affected: %d' % cur.rowcount)

print()
print('-- 3) создаём новую запись напрямую в таблице')
print("sqlite> INSERT INTO maintenance_repair")
print("   ...>   (machine_id, repair_type_id, start_date, end_date, author_id, comment, created_date)")
print("   ...> VALUES (3, 4, '2026-09-21', '2026-09-21', 1,")
print("   ...>   'Проверка люфтов, подтяжка крепежа, замена фильтров СОЖ.', '2026-09-20');")
cur.execute("INSERT INTO maintenance_repair "
            "(machine_id, repair_type_id, start_date, end_date, author_id, comment, created_date) "
            "VALUES (3, 4, '2026-09-21', '2026-09-21', 1, "
            "'Проверка люфтов, подтяжка крепежа, замена фильтров СОЖ.', '2026-09-20')")
print('rows affected: %d, last id: %d' % (cur.rowcount, cur.lastrowid))
con.commit()

print()
print("sqlite> SELECT r.id, m.inventory_no, t.name, r.start_date, r.end_date")
print("   ...>   FROM maintenance_repair r JOIN maintenance_machine m ON m.id = r.machine_id")
print("   ...>   JOIN maintenance_repairtype t ON t.id = r.repair_type_id")
print("   ...>   WHERE r.id >= 15 ORDER BY r.id;")
for r in cur.execute(
        "SELECT r.id, m.inventory_no, t.name, r.start_date, r.end_date "
        "FROM maintenance_repair r JOIN maintenance_machine m ON m.id = r.machine_id "
        "JOIN maintenance_repairtype t ON t.id = r.repair_type_id "
        "WHERE r.id >= 15 ORDER BY r.id"):
    print('|'.join(str(x) for x in r))
con.close()
print('sqlite> .quit')
