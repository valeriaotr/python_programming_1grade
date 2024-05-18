import dataclasses
import time
import typing as tp

from homework08.vkapi import config
from homework08.vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(user_id: int, count: int = 5000, offset: int = 0, fields: tp.Any = None) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    domain = config.VK_CONFIG["domain"]  # извлекаются из словаря
    access_token = config.VK_CONFIG["access_token"]  # извлекаются из словаря
    version_ = config.VK_CONFIG["version"]  # извлекаются из словаря
    fields = ", ".join(fields) if fields else ""  # преобразуется в строку, объединяя элементы списка с помощью запятой
    # и пробела, если fields не является пустым списком.
    # Если fields пустой, то присваивается пустая строка.

    base = f"{domain}"
    url = (  # представляет собой строку, содержащую информацию для запроса к API VK.
        # Значения access_token, user_id, fields, offset, count и version_ вставляются в соответствующие места в строке
        f"friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&offset={offset}&count={count}&v={version_}"
    )
    session_ = Session(base)  # базовый URL для сеанса.
    get_url = session_.get(url)  # GET-запрос с помощью метода get() объекта session_, передавая ему url.
    # Результат запроса сохраняется в переменную
    try:  # обработка полученного ответа от сервера.
        # Если в ответе есть ключи "response" и "count", то создается объект FriendsResponse, используя значения этих
        # ключей. В противном случае выводится содержимое ответа в консоль с помощью print().
        response = FriendsResponse(get_url.json()["response"]["count"], get_url.json()["response"]["items"])
    except KeyError:
        response = get_url.json()
        print(response)
    return response


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    domain = config.VK_CONFIG["domain"]  # извлекается из словаря
    access_token = config.VK_CONFIG["access_token"]  # извлекается из словаря
    version_ = config.VK_CONFIG["version"]  # извлекается из словаря
    session_ = Session(domain)  # базовый URL для сеанса.
    results_of_requests = []  # пустой список, который будет содержать результаты запросов.

    if target_uids:  # если переменная target_uids не является пустой
        for i in range(((len(target_uids) - 1) // 100) + 1):  # Цикл, который выполняется для каждого значения i
            # В диапазоне от 0 до (((len(target_uids) - 1) // 100) + 1).
            # Это позволяет разделить список target_uids на группы по 100 идентификаторов (так как VK API имеет
            # ограничение на количество идентификаторов в одном запросе).
            try:
                # Формирование строки url с помощью форматирования строк (f-строки). В этой строке указываются
                # параметры для API-запроса friends.getMutual, такие как access_token, source_uid, target_uid, count,
                # offset и version_. Значения этих параметров подставляются в строку с помощью фигурных скобок и
                # переменных.
                url = f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uids={','.join(list(map(str, target_uids)))}&count={count}&offset={i * 100}&v={version_}"
                friends = session_.get(url)  # GET-запрос объекта session_, передавая ему созданный URL.
                for friend in friends.json()["response"]:  # Цикл, который перебирает каждого друга в ответе от VK API.
                    # Объекты друзей извлекаются из JSON-ответа с помощью ключа "response".
                    results_of_requests.append(  # Полученные друзья обрабатываются и добавляются в список в виде
                        # объекта MutualFriends, содержащего идентификатор друга, список общих друзей и количество общих
                        MutualFriends(
                            id=friend["id"],
                            common_friends=list(map(int, friend["common_friends"])),
                            common_count=friend["common_count"],
                        )
                    )
            except KeyError:
                pass
            time.sleep(0.34)  # Задержка выполнения программы на 0.34 секунды с помощью функции sleep() из модуля time.
            # для соблюдения ограничений VK API на частоту запросов.
        return results_of_requests
    try:
        # Формирование строки url с помощью форматирования строк (f-строки). В этой строке указываются параметры для
        # API-запроса friends.getMutual, такие как access_token, source_uid, target_uid, count, offset и version_.
        # Значения этих параметров подставляются в строку с помощью фигурных скобок и переменных.
        url = f"friends.getMutual?access_token={access_token}&source_uid={source_uid}&target_uid={target_uid}&count={count}&offset={offset}&v={version_}"
        friends = session_.get(url)  # Выполнение HTTP-запроса с помощью метода get объекта session_.
        # Запрос отправляется на URL, указанный в переменной url, и результат сохраняется в переменной friends.
        results_of_requests.extend(friends.json()["response"])  # Извлечение данных из JSON-ответа на запрос.
        # Метод json() возвращает JSON-ответ в виде словаря, и с помощью ключа "response" извлекаются данные общ. друзей
        # Затем метод extend() используется для добавления данных в список results_of_requests.
    except:
        pass
    return results_of_requests


if __name__ == "__main__":
    friends_response = get_friends(user_id=239843379, fields=["nickname"])
    active_users = [user["id"] for user in friends_response.items if not user.get("deactivated")]  # type: ignore
    print("Number of active friends is:", len(active_users))
    mutual_friends = get_mutual(source_uid=239843379, target_uid=269738261, count=len(active_users))
    print("Number of mutual friends is:", len(mutual_friends))
    print("List of IDs of mutual friends is:", mutual_friends)
