import time  # type: ignore
import typing as tp  # type: ignore

import requests  # type: ignore
from requests.exceptions import (  # type: ignore
    ConnectionError,
    HTTPError,
    ReadTimeout,
    RetryError,
)


class Session(requests.Session):
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
        super().__init__()
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url: str, **kwargs: tp.Any) -> requests.Response:
        full_url = self.base_url + url
        retries = 0
        while True:
            try:
                response = super().get(full_url, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except (ConnectionError, HTTPError, ReadTimeout) as e:
                if retries >= self.max_retries:
                    raise RetryError("Превышено максимальное кол-во попыток") from e
                retries += 1
                delay = self.backoff_factor * (2 ** (retries - 1))
                time.sleep(delay)

    def post(self, url: str, data=None, json=None, **kwargs: tp.Any) -> requests.Response:
        full_url = self.base_url + url
        retries = 0
        while True:
            try:
                response = super().post(full_url, data=data, json=json, timeout=self.timeout, **kwargs)
                response.raise_for_status()
                return response
            except (ConnectionError, HTTPError, ReadTimeout) as e:
                if retries >= self.max_retries:
                    raise RetryError("Превышено максимальное кол-во попыток") from e
                retries += 1
                delay = self.backoff_factor * (2 ** (retries - 1))
                time.sleep(delay)


if __name__ == "__main__":
    session = Session("https://")
    print(session.get("example.com"))
