import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore


def extract_news(parser):  # извлекает новости с веб-страницы, используя парсер.
    """Extract news from a given web page"""
    news_list = []  # пустой список, в который будут добавляться новости.
    our_table = parser.table.findAll("table")[1]  # Из парсера извлекается таблица на веб-странице, и сохраняется
    # в переменной our_table, на веб-странице есть несколько таблиц, и выбрана вторая таблица для извлечения новостей.
    news = our_table.findAll("tr")  # Внутри таблицы извлекаются все строки (<tr> элементы), представляющие новости,
    # и сохраняются в переменной
    needed_information = {"title": "None", "url": "None", "author": "None", "points": 0}  #  словарь, в котором будут
    # Храниться данные для каждой новости.
    # Изначально словарь инициализируется значениями по умолчанию.
    for i in range(len(news) - 1):  # итерация по индексам строк новостей.
        news_1 = news[i]  # Извлекается текущая строка новости, и сохраняется в переменной news_1.

        if i % 3 == 0:  # Если текущий индекс i является кратным 3, то это означает начало новой новости.
            # В таком случае, словарь needed_information сбрасывается в значения по умолчанию.
            needed_information = {
                "title": "None",
                "url": "None",
                "author": "None",
                "points": 0,
                "comments": 0,
            }

        if news_1.attrs:  # Если у текущей строки есть атрибуты, то это означает, что она содержит заголовок новости.
            if news_1.attrs["class"][0] == "athing":
                needed_information["title"] = news_1.find("span", class_="titleline").find("a").string  # Заголовок
                # новости извлекается из текущей строки и сохраняется в словаре needed_information.
                link = news_1.find("span", class_="titleline").find("a").get("href")  # Получается ссылка на новость
                # из текущей строки.
                if "http" in link:  # Если ссылка начинается с "http", она считается полной ссылкой и сохраняется
                    # в словаре needed_information в поле "url".
                    needed_information["url"] = link
                elif "item" in link:  # Если ссылка содержит "item", она считается относительной ссылкой на внутреннюю
                    # страницу новости.
                    # В таком случае, полная ссылка формируется, добавляя относительную ссылку к базовому URL-адресу,
                    # и сохраняется в словаре needed_information в поле "url".
                    needed_information["url"] = "https://news.ycombinator.com/" + link

        else:  # Если ссылка не является полной ссылкой или относительной ссылкой на внутреннюю страницу новости,
            # значение "None" сохраняется в словаре needed_information в поле "url".
            if news_1.find("span", class_="subline"):  # Проверяется наличие элемента с классом "subline" в текущей
                # Строке. Это условие гарантирует, что текущая строка содержит информацию о других атрибутах новости.
                needed_information["points"] = int(
                    news_1.find("span", class_="subline").find("span", class_="score").string.split()[0]
                )  # Из текущей строки извлекается информация об очках новости.
                # Метод find ищет элемент с классом "subline", затем метод find внутри него находит элемент с классом
                # "score", а затем извлекается строка с очками.
                # Строка разбивается по пробелам, и первый элемент преобразуется в целое число и сохраняется в словаре
                # needed_information в поле "points".
                needed_information["author"] = news_1.find("span", class_="subline").find("a", class_="hnuser").string
                # Из текущей строки извлекается информация об авторе новости.
                # Метод find ищет элемент с классом "subline", а затем внутри него находит ссылку на автора с классом
                # "hnuser". Из этой ссылки извлекается текст автора, который сохраняется в словаре needed_information
                # в поле "author".
                number_of_comments = str(
                    news_1.find("span", class_="subline").findAll("a")[-1].string.split()[0]
                )  # Из текущей строки
                # Извлекается информация о количестве комментариев новости.
                # Метод find ищет элемент с классом "subline", а затем метод findAll находит все ссылки внутри этого
                # элемента. Последний элемент в списке ссылок содержит информацию о комментариях.
                # Из этого элемента извлекается строка, которая разбивается по пробелам, и первый элемент преобразуется
                # в строку.
                if number_of_comments.isdigit():
                    needed_information["comments"] = int(number_of_comments)  # преобразуется в целое число и
                    # сохраняется в словаре needed_information в поле "comments".
                else:
                    needed_information["comments"] = 0  # то количество комментариев считается равным 0.
            news_list.append(needed_information)  # После извлечения всех полей для текущей новости, словарь
            # needed_information добавляется в список news_list.

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    return parser.table.findAll("table")[1].findAll("tr")[-1].contents[2].find("a").get("href")
    #  Сначала происходит поиск таблицы, в которой содержится информация о следующей странице.
    #  Метод findAll ищет все таблицы на странице, и [1] выбирает вторую таблицу.
    # Затем в выбранной таблице ищутся все строки (<tr> элементы), и с помощью индекса [-1] выбирается последняя строка.
    #  Внутри последней строки выбирается третий элемент из содержимого строки.
    # В выбранном элементе ищется первая ссылка (<a> элемент), и из нее извлекается значение атрибута href, которое и
    # представляет собой URL следующей страницы.


def get_news(url, number_of_pages=1):
    """Collect news from a given web page"""
    news = []
    while number_of_pages:  # пока не закончатся страницы
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)  # отправляется GET-запрос по указанному URL, чтобы получить содержимое страницы.
        our_soup = BeautifulSoup(response.text, "html.parser")  # Содержимое страницы передается в BeautifulSoup для
        # Парсинга. Создается объект our_soup, который представляет структуру HTML-разметки страницы.
        list_of_news = extract_news(our_soup)  # Вызывается функция extract_news, которая извлекает новости из our_soup.
        # Возвращает список новостей.
        next_page = extract_next_page(our_soup)  # Вызывается функция extract_next_page, которая извлекает URL
        # следующей страницы из our_soup.
        url = "https://news.ycombinator.com/" + next_page  # Обновляется значение url для перехода на следующую
        # Страницу. URL следующей страницы строится путем объединения базового URL и next_page.
        news.extend(list_of_news)  # Полученные новости добавляются в общий список news
        number_of_pages -= 1  # Уменьшается счетчик
    return news  # возвращается список новостей news.


if __name__ == "__main__":
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    our_soup = BeautifulSoup(response.text, "html.parser")
    list_of_news = get_news(url, number_of_pages=1)
    for l in list_of_news:
        print(l)
    with open("my.html", "w") as file:
        file.write(our_soup.prettify())