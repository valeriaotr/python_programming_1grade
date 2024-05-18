import time
import typing as tp

import requests  # type: ignore
from requests.adapters import HTTPAdapter  # type: ignore
from requests.packages.urllib3.util.retry import Retry  # type: ignore


class Session:
    """
    Сессия.
    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.base_url = base_url  # Присваивает переданное значение base_url атрибуту
        self.timeout = timeout  # Присваивает переданное значение timeout атрибуту
        self.session = requests.Session()  # Создает новый экземпляр класса из модуля requests, присваивает его атрибуту
        possible_errors = []  # пустой список
        for i in range(400, 600):  # список, содержащий числа от 400 до 599.
            # Эти числа представляют собой статусы HTTP-ответов, которые будут считаться "вынужденными" и приведут
            # к повторному выполнению запроса.
            possible_errors.append(i)

        retry_process = Retry(
            allowed_methods=["POST", "GET"],  # задает список разрешенных HTTP-методов,
            total=max_retries,  # задает максимальное количество повторных попыток
            backoff_factor=backoff_factor,  # задает коэффициент задержки между повторными попытками
            status_forcelist=possible_errors,  # задает список статусов HTTP-ответов, которые приведут к повторному
            # выполнению запроса.
        )
        http_adapter = HTTPAdapter(max_retries=retry_process)  # Создает объект HTTPAdapter из модуля requests.adapters
        # с указанным параметром max_retries, который задает количество повторных попыток для адаптера.
        self.session.mount("https://", http_adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        # выполняет GET-запрос к указанному URL с использованием экземпляра класса Session.
        if "timeout" in kwargs:  # Проверяет, есть ли в аргументах kwargs ключ "timeout".
            self.timeout = kwargs["timeout"]  # присваивает значение этого ключа атрибуту timeout экземпляра класса
        response = self.session.get(self.base_url + "/" + url, timeout=self.timeout, *args, **kwargs)
        # Выполняет GET-запрос с использованием метода get экземпляра класса Session.
        # Комбинирует базовый URL (self.base_url) и URL-путь (url) для формирования полного URL-адреса запроса.
        # Задает таймаут выполнения запроса равным значению атрибута timeout.
        # Аргументы *args и **kwargs позволяют передавать дополнительные аргументы функции get.
        return response  # Возвращает полученный ответ от сервера.

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        # выполняет POST-запрос к указанному URL с использованием экземпляра класса Session.
        if "timeout" in kwargs:  # Проверяет, содержит ли аргумент kwargs ключ "timeout".
            self.timeout = kwargs["timeout"]  # присваивает его значение атрибуту timeout экземпляра класса
        response = self.session.post(self.base_url + "/" + url, timeout=self.timeout, *args, **kwargs)
        # Выполняет POST-запрос с использованием метода post экземпляра класса Session.
        # Комбинирует базовый URL (self.base_url) и URL-путь (url) для формирования полного URL-адреса запроса.
        # Задает таймаут выполнения запроса равным значению атрибута timeout.
        # Аргументы *args и **kwargs позволяют передавать дополнительные аргументы функции post.
        return response  # Возвращает полученный ответ от сервера.
