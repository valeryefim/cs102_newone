import typing as tp  # type: ignore
from collections import defaultdict  # type: ignore

import community as community_louvain  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import networkx as nx  # type: ignore
import pandas as pd  # type: ignore
from vkapi.friends import get_friends, get_mutual  # type: ignore


def ego_network(
    user_id: tp.Optional[int] = None, friends: tp.Optional[tp.List[int]] = None
) -> tp.List[tp.Tuple[int, int]]:
    """
    Построить эгоцентричный граф друзей.

    :param user_id: Идентификатор пользователя, для которого строится граф друзей.
    :param friends: Идентификаторы друзей, между которыми устанавливаются связи.
    """

    # Если список друзей не задан, получаем всех друзей пользователя.
    if friends is None:
        friends = get_friends(user_id)

    # Создаем список для хранения ребер графа.
    edges = []

    # Для каждого друга в списке друзей:
    for friend_id in friends:
        # Добавляем ребро между пользователем и другом.
        edges.append((user_id, friend_id))

        try:
            # Получаем список общих друзей между пользователем и текущим другом.
            mutual_friends = get_mutual(source_uid=user_id, target_uid=friend_id)
        except:
            continue

        # Для каждого общего друга:
        for mutual_friend_id in mutual_friends:
            # Добавляем ребро между другом и общим другом.
            edges.append((friend_id, mutual_friend_id))

    return edges


def plot_ego_network(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    nx.draw(graph, layout, node_size=10, node_color="black", alpha=0.5)
    plt.title("Ego Network", size=15)
    plt.show()


def plot_communities(net: tp.List[tp.Tuple[int, int]]) -> None:
    graph = nx.Graph()
    graph.add_edges_from(net)
    layout = nx.spring_layout(graph)
    partition = community_louvain.best_partition(graph)
    nx.draw(graph, layout, node_size=25, node_color=list(partition.values()), alpha=0.8)
    plt.title("Ego Network", size=15)
    plt.show()


def get_communities(net: tp.List[tp.Tuple[int, int]]) -> tp.Dict[int, tp.List[int]]:
    communities = defaultdict(list)
    graph = nx.Graph()
    graph.add_edges_from(net)
    partition = community_louvain.best_partition(graph)
    for uid, cluster in partition.items():
        communities[cluster].append(uid)
    return communities


def describe_communities(
    clusters: tp.Dict[int, tp.List[int]],
    friends: tp.List[tp.Dict[str, tp.Any]],
    fields: tp.Optional[tp.List[str]] = None,
) -> pd.DataFrame:
    if fields is None:
        fields = ["first_name", "last_name"]

    data = []
    for cluster_n, cluster_users in clusters.items():
        for uid in cluster_users:
            for friend in friends:
                if uid == friend["id"]:
                    data.append([cluster_n] + [friend.get(field) for field in fields])  # type: ignore
                    break
    return pd.DataFrame(data=data, columns=["cluster"] + fields)


net = ego_network(user_id=227409851)
plot_communities(net)
