import datetime as dt  # type: ignore
import typing as tp  # type: ignore

import numpy as np  # type: ignore
import requests  # type: ignore

VK_CONFIG = {
    "domain": "https://api.vk.com/method",
    "access_token": "vk1.a.Mt8OcEGXUWvqKcaiFYlqHQ7c252oz0VJtCRSjERD-PkZeeW3n3HaahmCwoxy7jj9Hgfrv7apkkLV03tmFcST9Ucu-DMu4-zaNvJErXSphQTlbZ0Hbx6uXQgw8-2Ec8SLciMNZL8D7l0IsjqFQu34WMZKFyEq_wEWbLgSGRX5a49KG2Rh6-lT2H-g9ZcDD7et",
    "version": "5.126",
}

domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]
user_id = 123
fields = "bdate"


def age_predict(user_id: int) -> float:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя.

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
    response = requests.get(query)
    try:
        friends_count = response.json()["response"]["count"]
    except:
        return 20.0

    year = dt.datetime.today().year
    ages = []

    for i in range(friends_count):
        if "bdate" in response.json()["response"]["items"][i]:
            date_of_birth = response.json()["response"]["items"][i]["bdate"]
            if len(date_of_birth) == 10 or len(date_of_birth) == 9 or len(date_of_birth) == 8:
                year_of_birth = int(date_of_birth.split(".")[-1])
                age = year - year_of_birth
                ages.append(age)
            else:
                pass
        else:
            pass

    median = float(np.median(ages))

    return median


if __name__ == "__main__":
    print(age_predict(123))
