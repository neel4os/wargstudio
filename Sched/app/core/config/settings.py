from pydantic import BaseSettings
from os import environ


class Setting(BaseSettings):
    title: str = "warg scheduler"
    description: str = "A collection of APIs to perform \
        and schedule chaos Engineering"
    redisUrl: str = environ["redisUrl"]
    MinioUrl: str = environ["storageUrl"]
    MinioAcessKey: str = environ["storageAccessKey"]
    MinioSecretKry: str = environ["storageSecretKey"]


_setting = Setting()
