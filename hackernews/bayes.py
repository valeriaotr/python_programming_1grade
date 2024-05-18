import csv
import string
from collections import defaultdict
from math import log

from db import News, session


class NaiveBayesClassifier:
    def __init__(
        self,
    ):
        self.number = 1
        self.set_of_words = set()  # хранение уникальных слов
        self.counters = defaultdict(lambda: defaultdict(int))  # словарь =0 для подсчета слов
        self.class_counter = defaultdict(int)  # словарь =0 для подсчета элементов класса
        self.words_count = 0  # счетчик слов

    def fit(self, X, y):  # подсчет статистики на основе входных данных X и меток y.
        """Fit Naive Bayes classifier according to X, y."""
        for abscissa, ordinata in zip(X, y):  # происходит итерация по соответствующим парам элементов X и y
            self.class_counter[ordinata] += 1  # увеличивается счетчик класса ordinata в словаре class_counter
            # Если класс ordinata еще не встречался ранее, то он
            # будет добавлен в словарь с начальным значением 0.
            # Это позволяет подсчитать количество элементов каждого класса.
            for word in abscissa.split():  # Здесь итерируются слова, полученные путем разделения строки abscissa на
                # отдельные слова.
                self.counters[ordinata][word] += 1  # увеличивается счетчик слова word для класса ordinata во
                # вложенном словаре counters
                self.set_of_words.add(word)  # слово word добавляется в множество set_of_words
                self.words_count += 1  # увеличивается счетчик words_count на 1.
                # Этот счетчик используется для подсчета общего количества слов или элементов во всех входных данных.

    def predict(self, X):  # классификация для массива тестовых векторов X.
        """Perform classification on an array of test vectors X."""
        predicted = []
        for string in X:  # итерация по каждому элементу string в массиве X, который представляет тестовые векторы.
            predicted.append(self.predict_class(string))  # предсказание класса для каждого тестового вектора string
        return predicted  # полученные результаты
        # В итоге данный метод позволяет применить обученную модель классификации к новым тестовым векторам и
        # получить предсказанные классы.

    def predict_class(self, string):  # вспомогательная функция
        """Auxiliary function to perform classification on an array of test vectors X."""
        class_index = None  # переменная для хранения метки класса с наибольшей вероятностью
        elements_count = sum(self.class_counter.values())  # общее количество элементов для вычисления вероятности
        # классов
        best_value = float("-inf")  # переменная для хранения наилучшего значения вероятности класса
        for class_i in self.counters:  # итерация по классам
            current_value = log(self.class_counter[class_i] / elements_count)
            for word in string.split():
                current_word_class_counter = self.counters[class_i][word]  # количество вхождений слова word для
                # Текущего класса class_i из словаря counters.
                # Это значение используется для вычисления вероятности появления слова в классе.
                current_class_word_counter = sum(self.counters[class_i].values())  # вычисляем общее количество слов в
                # текущем классе class_i
                current_value += log(  # Логарифмированное значение вероятности класса с использованием формулы наивного
                    # Байесовского классификатора.
                    # Формула вычисляет условную вероятность класса при условии появления
                    # каждого слова в тестовом векторе.
                    (current_word_class_counter + self.number)
                    / (current_class_word_counter + self.number * len(self.set_of_words))
                )
            if best_value < current_value:  # Здесь проверяется, является ли текущее значение вероятности current_value
                # Лучше, чем текущее лучшее значение вероятности best_value
                # Если это так, то обновляются значения
                class_index = class_i
                best_value = current_value
        if class_index is None:
            raise Exception("Classifier is not fitted")
        return class_index

    def score(self, X_test, y_test):  # метод, который вычисляет среднюю точность (accuracy) на основе предсказаний
        # модели для заданного набора тестовых данных X_test и соответствующих меток y_test.
        """Returns the mean accuracy on the given test data and labels."""
        predictions = self.predict(X_test)  # вызывается метод predict, который принимает массив тестовых данных X_test
        # и возвращает предсказанные классы для каждого тестового вектора.
        # Результат сохраняется в переменной predictions.
        correct_predictions = sum(y == pred for y, pred in zip(y_test, predictions))  # используется генератор списка и
        # функция sum для подсчета количества правильных предсказаний.
        # Генератор списка итерирует пары (y, pred) из y_test и predictions с помощью zip и проверяет,
        # совпадает ли метка y с предсказанным классом pred.
        # Если метка и предсказание совпадают, то выражение y == pred будет истинным и будет учтено в суммировании.
        # В результате будет получено общее количество правильных предсказаний, которое сохраняется
        # в переменной correct_predictions.
        accuracy = correct_predictions / len(y_test)  # вычисляется точность (accuracy) путем деления количества
        # правильных предсказаний correct_predictions на общее количество тестовых меток y_test.
        return accuracy


def clean(string_):  # очистка текстовой строки string_ от пунктуационных символов.
    """Getting rid of punctuation"""
    translator = str.maketrans("", "", string.punctuation)  # создается объект translator с помощью метода maketrans
    # из класса str, maketrans используется для создания таблицы перевода символов.
    # В данном случае, первый аргумент "" указывает, что символы не должны быть заменены,
    # а второй и третий аргументы "" и string.punctuation указывают на то, что все пунктуационные
    # символы должны быть удалены.
    return string_.translate(translator)


def label_news():  # функция, которая добавляет метки к новостям в базе данных
    """Adding labels to news"""
    session_ = session()  # создается объект сеанса базы данных

    x_train = session_.query(News.title).filter(News.label != None).all()  # выполняется запрос к базе данных,
    # чтобы получить заголовки новостей (News.title), где метка (News.label) не является пустой.
    # Результат сохраняется в переменной x_train.
    y_train = session_.query(News.label).filter(News.label != None).all()  # аналогичный запрос

    x_train = [clean(str(x)).lower() for x in x_train]  # очистка и приведение к нижнему регистру каждого элемента
    y_train = [clean(str(y)).lower() for y in y_train]  # аналогично

    model = NaiveBayesClassifier()  # создается объект модели NaiveBayesClassifier.
    model.fit(x_train, y_train)  # выполняется обучение модели model на основе обучающих данных x_train и меток y_train

    abscissa_lab = session_.query(News.title).filter(News.label == None).all()  # запрос к базе данных, чтобы получить
    # заголовки новостей
    abscissa_lab = [clean(str(xx)).lower() for xx in abscissa_lab]  # приведение к нижнему регистру каждого элемента

    ordinata_predicted = model.predict(abscissa_lab)  # предсказание меток для новых данных abscissa_lab
    # с использованием обученной модели model
    rows = session_.query(News).filter(News.label == None).all()  #  запрос к базе данных, чтобы получить все записи
    # новостей, где метка является пустой

    i = 0  # для итерации по индексам предсказанных меток ordinata_predicted.
    for row in rows:  # цикл, который проходит по каждой записи новости в переменной rows.
        row.label = ordinata_predicted[i]  # присваивается предсказанная метка новости (ordinata_predicted[i])
        # в поле метки (row.label) текущей записи новости.
        session_.add(row)  # вызывается метод add объекта сеанса session_, чтобы добавить измененную запись новости.
        session_.commit()  # вызывается метод commit объекта сеанса session_, чтобы сохранить изменения в базе данных.
        i += 1  # инкрементируется переменная i, чтобы перейти к следующему индексу в списке предсказанных меток.


if __name__ == "__main__":
    with open("data/SMSSpamCollection") as data_file:
        data = list(csv.reader(data_file, delimiter="\t"))
    X, y = [], []
    for target, msg in data:
        X.append(msg)
        y.append(target)
    X = [clean(x).lower() for x in X]
    print(X[0], "|||", y[0])
    X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    print(model.score(X_test, y_test))