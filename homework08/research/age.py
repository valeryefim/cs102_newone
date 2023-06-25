import datetime as dt  # type: ignore
import typing as tp  # type: ignore

import numpy as np  # type: ignore
import requests  # type: ignore

VK_CONFIG = {
    "domain": "https://api.vk.com/method",
    "access_token": "vk1.a.b93Fe3Vg5uJM_ZI8yE7tD7DpRhnEoDEBT-L-qy5-_i35l0A8pYS4nV4Wi9KduSKiIhXez2cgTJTzY6J6rUCrZu7QAKiSGE9EDchEogEKAvE1-kwmlGjyQ37F642TRA4HqMCFTyb-PQWgZUDRDQQVzjYWbRZY_DW3tCdDCAa6y-G-DcQTUdpVVA4wtTYevQgc",
    "version": "5.126",
}

domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]
user_id = 189183825
fields = "bdate"

query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
response = requests.get(query)
friends_count = response.json()["response"]["count"]


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя.

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """

    year = dt.datetime.today().year
    ages = []

    for i in range(friends_count):
        if "bdate" in response.json()["response"]["items"][i]:
            date_of_birth = response.json()["response"]["items"][i]["bdate"]
            if len(date_of_birth) == 10 or len(date_of_birth) == 9 or len(date_of_birth) == 8:
                year_of_birth = int(date_of_birth.split(".")[-1])
                age = year - year_of_birth
                ages.append(age)

    median = np.median(ages)
    print(f"Медианный возраст пользователя: {median}")


if __name__ == "__main__":
    age_predict(189183825)
