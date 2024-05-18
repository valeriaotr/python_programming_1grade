from scraputils import get_news
from sqlalchemy import Column, Integer, String, create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore


def create_db(lst):
    """Adding news to database"""
    session_ = session()  # создается объект сеанса базы данных
    needed_information = {  # создается словарь, который содержит значения по умолчанию для полей новости,
        # если эти поля отсутствуют в словаре из списка lst.
        "title": "None",
        "url": "None",
        "author": "None",
        "points": 0,
        "comments": 0,
    }
    for dictionary in lst:  # цикл, который проходит по каждому словарю dictionary в списке lst.
        if dictionary != needed_information:  # выполняется проверка, чтобы убедиться, что словарь dictionary не равен
            # Needed_information.
            # Это делается для того, чтобы исключить добавление записей новостей с пустыми значениями в базу данных.
            news_ = News(  # создается объект News (модель новости), используя класс News,
                # который представляет таблицу в базе данных.
                # Значения полей новости берутся из соответствующих ключей словаря dictionary.
                # Если значение отсутствует, то используется значение по умолчанию из needed_information.
                title=dictionary["title"],
                author=dictionary["author"],
                url=dictionary["url"],
                comments=dictionary["comments"],
                points=dictionary["points"],
            )
            session_.add(news_)  # вызывается метод add объекта сеанса session_,
            # чтобы добавить созданный объект news_ в базу данных.
            session_.commit()  # вызывается метод commit объекта сеанса session_,
            # чтобы сохранить изменения в базе данных.


Base = declarative_base()  # создается базовый класс Base с помощью функции declarative_base()
# из модуля sqlalchemy.ext.declarative.
# Этот класс будет использоваться для создания моделей (классов, соответствующих таблицам) базы данных.
engine = create_engine("sqlite:///news.db")  # создается объект engine с помощью функции create_engine()
# из модуля sqlalchemy, engine представляет собой движок базы данных, который управляет подключением и взаимодействием
# с базой данных. В данном случае используется движок SQLite, и база данных будет храниться в файле news.db
# (если файл не существует, он будет создан).
session = sessionmaker(bind=engine)  # представляет собой класс-фабрику для создания сеансов базы данных.
# Аргумент bind=engine указывает sessionmaker использовать созданный ранее объект engine для установления соединения
# с базой данных.


class News(Base):  # type: ignore
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    url = "https://news.ycombinator.com/"
    news_list = get_news(url, number_of_pages=1)
    create_db(news_list)