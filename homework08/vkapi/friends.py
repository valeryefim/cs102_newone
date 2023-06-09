import dataclasses  # type: ignore
import typing as tp  # type: ignore

import requests  # type: ignore
import vkapi.config  # type: ignore
from requests import Response  # type: ignore

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]

domain = vkapi.config.VK_CONFIG["domain"]
access_token = vkapi.config.VK_CONFIG["access_token"]
v = vkapi.config.VK_CONFIG["version"]
user_id = 329996033
fields = "bdate"

# query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
# response = requests.get(query)
# friends_count = response.json()["response"]["count"]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> tp.List[int]:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).
    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """

    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = requests.get(query)
    try:
        friends_count = response.json()["response"]["count"]
        # print(f"Количество друзей пользователя: {friends_count}")

        friends_ids = []
        for i in range(friends_count):
            friends_ids.append(response.json()["response"]["items"][i]["id"])

        return friends_ids
    except:
        pass


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: int = 0,
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

    if source_uid == 0:
        return [0]

    if target_uid is not None:
        source_uid_friends = get_friends(source_uid)
        target_uid_friends = get_friends(target_uid)
        mutual_friends = list(set(source_uid_friends).intersection(target_uid_friends))
        return mutual_friends

    if target_uids is not None:
        mutual = []
        source_uid_friends = get_friends(source_uid)
        for friend in target_uids:
            try:
                friend_friends = get_friends(friend)
                mutual_friends = list(set(source_uid_friends).intersection(friend_friends))
                mutual.extend(mutual_friends)
            except:
                continue
        return mutual

    return [0]
