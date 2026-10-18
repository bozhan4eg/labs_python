# -*- coding: utf-8 -*-
"""
Лабораторная работа № 1. Задание по Python.

Данные о студентах группы хранятся в одном списке (переменная groupmates).
Для каждого студента заполнены поля: имя, фамилия, список экзаменов, оценки.

Задание: написать функцию фильтрации студентов по средней оценке —
на экран выводится список студентов, средний балл которых выше заданного.
Средний балл для фильтрации вводится пользователем с клавиатуры.
"""

groupmates = [
    {
        "name": "Александр",
        "surname": "Иванов",
        "exams": ["ПИС", "Web-программирование", "Базы данных"],
        "marks": [5, 4, 5]
    },
    {
        "name": "Иван",
        "surname": "Петров",
        "exams": ["ПИС", "Операционные системы", "Сети"],
        "marks": [3, 4, 4]
    },
    {
        "name": "Кирилл",
        "surname": "Смирнов",
        "exams": ["ПИС", "Алгоритмы и графы", "КТП"],
        "marks": [5, 5, 5]
    },
    {
        "name": "Дарья",
        "surname": "Кузнецова",
        "exams": ["Web-программирование", "Базы данных", "История"],
        "marks": [4, 5, 4]
    },
    {
        "name": "Павел",
        "surname": "Соколов",
        "exams": ["ПИС", "Философия", "КТП"],
        "marks": [3, 3, 4]
    },
    {
        "name": "Анна",
        "surname": "Попова",
        "exams": ["Web-программирование", "Сети", "Операционные системы"],
        "marks": [4, 4, 5]
    },
    {
        "name": "Максим",
        "surname": "Волков",
        "exams": ["ПИС", "Алгоритмы и графы", "Базы данных"],
        "marks": [3, 4, 3]
    },
]


def print_students(students):
    """Вывод списка студентов в виде таблицы."""
    print(u"Имя".ljust(15), u"Фамилия".ljust(10), u"Экзамены".ljust(50), u"Оценки".ljust(20))
    for student in students:
        print(student["name"].ljust(15),
              student["surname"].ljust(10),
              str(student["exams"]).ljust(50),
              str(student["marks"]).ljust(20))


def average_mark(student):
    """Средний балл студента."""
    return sum(student["marks"]) / len(student["marks"])


def filter_students_by_average(students, min_average):
    """
    Фильтрация студентов по средней оценке.

    :param students: список словарей с данными о студентах
    :param min_average: пороговое значение среднего балла
    :return: список студентов, средний балл которых строго выше заданного
    """
    return [student for student in students if average_mark(student) > min_average]


def print_students_with_average(students):
    """Вывод отфильтрованного списка вместе со значением среднего балла."""
    print(u"Имя".ljust(15), u"Фамилия".ljust(10), u"Средний балл".ljust(15), u"Оценки".ljust(20))
    for student in students:
        print(student["name"].ljust(15),
              student["surname"].ljust(10),
              ("%.2f" % average_mark(student)).ljust(15),
              str(student["marks"]).ljust(20))


if __name__ == "__main__":
    print(u"Все студенты группы:")
    print_students(groupmates)

    print()
    min_average = float(input(u"Введите средний балл для фильтрации: "))

    filtered = filter_students_by_average(groupmates, min_average)

    print()
    if filtered:
        print(u"Студенты со средним баллом выше %.2f:" % min_average)
        print_students_with_average(filtered)
    else:
        print(u"Студентов со средним баллом выше %.2f не найдено." % min_average)

    print()
    print(u"Всего в списке: %d, прошло фильтрацию: %d" % (len(groupmates), len(filtered)))
