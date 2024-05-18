import typing as tp
from collections import defaultdict

import community as cl  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore
import pandas as pd  # type: ignore

from homework08.vkapi.friends import get_friends, get_mutual


def ego_network(
    user_id: tp.Optional[int] = None, friends: tp.Optional[tp.List[int]] = None
) -> tp.List[tp.Tuple[int, int]]:
    """
    Построить эгоцентричный граф друзей.
    :param user_id: Идентификатор пользователя, для которого строится граф друзей.
    :param friends: Идентификаторы друзей, между которыми устанавливаются связи.
    """
    coordinates = []  # пустой список, в который будут добавляться координаты друзей.
    friends_ = get_mutual(user_id, target_uids=friends, count=len(friends))  # type: ignore
    for friend in friends_:  # перебор каждого объекта в списке
        friend_id = friend.get("id")  # type: ignore
        common_friends = friend.get("common_friends")  # type: ignore
        if friend_id is not None and common_friends is not None:  # type: ignore
            for person in common_friends:  # перебираются все элементы в списке
                coordinates.append((friend_id, person))  # координаты добавляются в список coordinates.
    return coordinates


def plot_ego_network(net: tp.List[tp.Tuple[int, int]]) -> None:
    """Используется для визуализации графа без выделения групп узлов"""
    gr = nx.Graph()  # Создается пустой граф
    gr.add_edges_from(net)  # К графу добавляются ребра, заданные в переменной net
    # Это создает структуру графа, где каждое ребро представлено парой узлов.
    layout = nx.spring_layout(gr)  # Создается расположение для узлов графа
    # Расположение определяет позиции узлов на графической плоскости.
    nx.draw(gr, layout, node_size=25, node_color="black", alpha=0.2)  # происходит отрисовка графа с использованием
    # Указанного расположения. Здесь также задаются параметры отображения графа, такие как размер узлов, цвет узлов
    # и прозрачность.
    plt.title("Ego Network", size=15)
    plt.show()


def plot_communities(net: tp.List[tp.Tuple[int, int]]) -> None:
    """Используется для визуализации графа с выделением групп узлов"""
    gr = nx.Graph()  # Создается пустой граф
    gr.add_edges_from(net)  # К графу добавляются ребра, заданные в переменной net
    # Это создает структуру графа, где каждое ребро представлено парой узлов.
    layout = nx.spring_layout(gr)  # Создается расположение для узлов графа
    # Расположение определяет позиции узлов на графической плоскости.
    dividing = cl.best_partition(gr)  # происходит разделение узлов графа на группы
    nx.draw(gr, layout, node_size=25, node_color=list(dividing.values()), alpha=0.8)  # происходит отрисовка графа
    # с использованием указанного расположения. Здесь также задаются параметры отображения графа: размер узлов,
    # цвет узлов, где каждая группа узлов имеет свой цвет, и прозрачность.
    plt.title("Ego Network", size=15)
    plt.show()


def get_communities(net: tp.List[tp.Tuple[int, int]]) -> tp.Dict[int, tp.List[int]]:
    """Получаем инф-ию о группах узлов в графе"""
    node_groups = defaultdict(list)  # В этом словаре будут храниться группы узлов графа.
    gr = nx.Graph()  # Создается пустой граф
    gr.add_edges_from(net)  # К графу добавляются ребра, заданные в переменной net
    # Это создает структуру графа, где каждое ребро представлено парой узлов.
    dividing = cl.best_partition(gr)  # происходит разделение узлов графа на группы
    for uid, cluster in dividing.items():  # перебираются элементы пар (uid, cluster) в словаре
        node_groups[cluster].append(uid)  # Для каждого узла uid и его соответствующего кластера происходит добавление
        # uid в список сообщества с ключом cluster в словаре.
    return node_groups


def describe_communities(
    clusters: tp.Dict[int, tp.List[int]],  # словарь, где каждый ключ представляет собой номер
    # кластера, а значение - список идентификаторов пользователей в этом кластере
    friends: tp.List[tp.Dict[str, tp.Any]],  # список словарей с информацией о друзьях
    fields: tp.Optional[tp.List[str]] = None,  # опциональный список полей, по умолчанию равен None
) -> pd.DataFrame:
    """Описание групп узлов в графе"""
    if fields is None:  # Если равен None, то присваивается значение ["first_name", "last_name"].
        fields = ["first_name", "last_name"]
    inf_w_data = []  # пустой список, в который будут добавляться данные о кластерах и соответствующих им пользователях.
    for cluster_number, cluster_users in clusters.items():  # перебираются элементы пар
        for uid in cluster_users:  # Если идентификатор пользователя присутствует в кластере
            for friend in friends:  # перебираются друзья
                if uid == friend["id"]:
                    inf_w_data.append(
                        [cluster_number] + [friend.get(field) for field in fields]
                    )  # Создается список, в котором
                    # первым элементом является номер кластера, а остальные элементы - значения полей "first_name" и
                    # "last_name" из словаря friend. Полученный список добавляется в список data.
                    break
    return pd.DataFrame(data=inf_w_data, columns=["cluster"] + fields)


if __name__ == "__main__":
    friends_response = get_friends(user_id=239843379, fields=["nickname"])
    active_users = [user["id"] for user in friends_response.items if not user.get("deactivated")]  # type: ignore
    net = ego_network(user_id=239843379, friends=active_users)
    print(net)
    plot_communities(net)
    communities = get_communities(net)
    df = describe_communities(communities, friends_response.items, fields=["first_name", "last_name"])  # type: ignore
    df.to_csv('output.csv', index=False)
