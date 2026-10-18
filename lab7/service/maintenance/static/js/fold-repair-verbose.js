// Лабораторная работа № 7. «Громоздкая» версия из методички (для сравнения):
// скрытие выполняется напрямую через style.display каждого элемента поста.
// В проекте подключена компактная версия fold-repair.js, а этот файл оставлен
// для демонстрации прямого манипулирования DOM.
var foldBtns = document.getElementsByClassName("fold-button");
for (var i = 0; i < foldBtns.length; i++) {
    foldBtns[i].addEventListener("click", function (e) {
        if (e.target.className === "fold-button folded") {
            e.target.innerHTML = "свернуть";
            e.target.className = "fold-button";
            var displayState = "block";
        } else {
            e.target.innerHTML = "развернуть";
            e.target.className = "fold-button folded";
            var displayState = "none";
        }
        e.target
            .parentElement
            .getElementsByClassName('article-author')[0]
            .style.display = displayState;
        e.target
            .parentElement
            .getElementsByClassName('article-created-date')[0]
            .style.display = displayState;
        e.target
            .parentElement
            .getElementsByClassName('article-text')[0]
            .style.display = displayState;
    });
}
