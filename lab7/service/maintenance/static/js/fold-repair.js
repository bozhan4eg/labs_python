// Лабораторная работа № 7. Задание: компактная реализация сворачивания.
// Класс folded добавляется НЕ кнопке, а родителю всего поста (.one-post),
// а скрытие элементов выполняется через CSS-стили:
//   .one-post.folded .article-author { display: none; }
//   .one-post.folded .article-created-date { display: none; }
//   .one-post.folded .article-text { display: none; }
var foldBtns = document.getElementsByClassName("fold-button");
for (var i = 0; i < foldBtns.length; i++) {
    foldBtns[i].addEventListener("click", function (e) {
        var post = e.target.parentElement;          // родитель кнопки — .one-post
        var folded = post.classList.contains("folded");
        if (folded) {
            post.className = "one-post";            // убираем класс folded
            e.target.innerHTML = "свернуть";
        } else {
            post.className = "one-post folded";     // добавляем класс folded
            e.target.innerHTML = "развернуть";
        }
    });
}
