import sqlalchemy  # type: ignore
from bayes import NaiveBayesClassifier, label_news
from bottle import redirect, request, route, run, template  # type: ignore
from db import News, session
from scraputils import get_news


@route("/all")
def all_news():
    session_ = session()  # создается объект сеанса базы данных
    rows = session_.query(News).all()  # Запрос запрашивает все записи из таблицы News.
    # Метод all() возвращает все найденные записи в виде списка объектов.
    return template("news_template_2", rows=session_.query(News).order_by(News.label).all())  # возвращает результат
    # выполнения шаблона news_template_2
    # с передачей списка всех записей новостей в качестве переменной rows.


@route("/news")
def news_list():
    session_ = session()
    rows = session_.query(News).filter(News.label == None).all()  # запрашивает все записи из таблицы News,
    # где поле label равно None (то есть неразмеченные новости).
    # Метод filter применяет условие фильтрации к результатам запроса.
    # Метод all() возвращает все найденные записи в виде списка объектов.
    return template("news_template", rows=rows)


@route("/add_label/", method="GET")
def add_label():
    session_ = session()
    label_gotten = request.GET.get("label", "")  # извлекается значение параметра label из GET-запроса.
    # GET-параметры представляются в виде строки запроса URL,
    # и данная строка предоставляет значение метки для добавления.
    id_gotten = int(request.GET.get("id", ""))  # извлекается значение параметра id из GET-запроса.
    # GET-параметры представляются в виде строки запроса URL, и данная строка предоставляет идентификатор записи
    # новости, к которой нужно добавить метку.
    row = session_.query(News).filter(News.id == id_gotten).one()  # запрашивает единственную запись из таблицы News,
    # Где поле id соответствует полученному идентификатору.
    # Метод one() возвращает найденную запись или вызывает исключение, если нет записей или найдено более одной записи.
    row.label = label_gotten  # устанавливается значение поля label найденной записи равным полученной метке.
    session_.add(row)  # вызывается метод add объекта сеанса session_, чтобы добавить измененную запись в базу данных.
    session_.commit()  # сохранить изменения в базе данных.
    redirect("/all")  # перенаправление пользователя на другую страницу (в данном случае на страницу /all).
    return row  #  возвращается объект row, представляющий измененную запись новости.


@route("/update")
def update_news():
    session_ = session()
    url = "https://news.ycombinator.com/"  # задается URL-адрес, с которого нужно получить новости для
    # обновления базы данных.
    lst = get_news(url)  # ызывается функция get_news, которая получает новости с указанного URL-адреса.
    # Результат сохраняется в переменной в виде списка словарей, где каждый словарь представляет одну новость
    # с соответствующими полями (название, автор, URL, комментарии, очки и т.д.).
    for dictionary in lst:  # итерация по каждому словарю в списке
        try:
            row = session_.query(News).filter(News.title == dictionary["title"]).one()  # запрашивает единственную
            # запись из таблицы News, где поле title равно названию новости из текущего словаря.
            # Если запись не найдена, возникает исключение NoResultFound.
        except sqlalchemy.exc.NoResultFound:  #  если в базе данных не найдена запись с указанным названием новости.
            new = News(  # создается новый объект класса News с использованием данных из текущего словаря
                title=dictionary["title"],
                author=dictionary["author"],
                url=dictionary["url"],
                comments=dictionary["comments"],
                points=dictionary["points"],
            )
            session_.add(new)
            session_.commit()
    redirect("/news")  # перенаправление пользователя на другую страницу (в данном случае на страницу /news).


@route("/classify")
def classify_news():
    label_news()
    redirect("/news")


if __name__ == "__main__":
    run(host="localhost", port=8080)