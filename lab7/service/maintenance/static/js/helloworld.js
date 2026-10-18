// Лабораторная работа № 7. Первый скрипт на JavaScript.
// Список студентов с полями: имя, фамилия, группа, оценки.
var groupmates = [
    {
        "name": "Александр",
        "surname": "Иванов",
        "group": "БПИ2101",
        "marks": [5, 4, 5]
    },
    {
        "name": "Иван",
        "surname": "Петров",
        "group": "БПИ2102",
        "marks": [4, 4, 4]
    },
    {
        "name": "Кирилл",
        "surname": "Смирнов",
        "group": "БАП2101",
        "marks": [5, 5, 5]
    },
    {
        "name": "Дарья",
        "surname": "Кузнецова",
        "group": "БПИ2101",
        "marks": [4, 5, 4]
    },
    {
        "name": "Павел",
        "surname": "Соколов",
        "group": "БПИ2102",
        "marks": [3, 3, 4]
    },
    {
        "name": "Анна",
        "surname": "Попова",
        "group": "БАП2101",
        "marks": [4, 4, 5]
    }
];

// js не поддерживает добавление нужного количества символов
// справа от строки, т. е. аналога ljust из Python здесь нет
var rpad = function (str, length) {
    str = str.toString();              // преобразование в строку
    while (str.length < length)
        str = str + ' ';               // добавление пробела в конец строки
    return str;                        // когда все пробелы добавлены, возвратить строку
};

var averageMark = function (student) {
    var sum = 0;
    for (var i = 0; i < student.marks.length; i++)
        sum += student.marks[i];
    return sum / student.marks.length;
};

// Вывод списка студентов в виде таблицы (как в лабораторной работе № 1)
var printStudents = function (students) {
    console.log(
        rpad("Имя", 15),
        rpad("Фамилия", 15),
        rpad("Группа", 8),
        rpad("Оценки", 20)
    );
    for (var i = 0; i <= students.length - 1; i++) {
        console.log(
            rpad(students[i]['name'], 15),
            rpad(students[i]['surname'], 15),
            rpad(students[i]['group'], 8),
            rpad(students[i]['marks'], 20)
        );
    }
    console.log('\n');
};

// Задание 1: фильтрация студентов по группе
var filterByGroup = function (students, groupName) {
    var result = [];
    for (var i = 0; i < students.length; i++) {
        if (students[i]['group'] === groupName)
            result.push(students[i]);
    }
    return result;
};

// Задание 2: фильтрация студентов по средней оценке
var filterByAverage = function (students, minAverage) {
    var result = [];
    for (var i = 0; i < students.length; i++) {
        if (averageMark(students[i]) > minAverage)
            result.push(students[i]);
    }
    return result;
};

console.log(groupmates);
printStudents(groupmates);

// Наименование группы и средний балл вводятся пользователем с клавиатуры
var groupName = prompt("Введите наименование группы для фильтрации:");
if (groupName === null) {
    console.log("Фильтрация по группе отменена пользователем.");
} else {
    console.log("Студенты группы " + groupName + ":");
    printStudents(filterByGroup(groupmates, groupName));
}

var minAverage = parseFloat(prompt("Введите средний балл для фильтрации:"));
if (isNaN(minAverage)) {
    console.log("Фильтрация по среднему баллу отменена пользователем.");
} else {
    console.log("Студенты со средним баллом выше " + minAverage + ":");
    printStudents(filterByAverage(groupmates, minAverage));
}
