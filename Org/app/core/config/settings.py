from pydantic import BaseSettings
from os import environ


class Setting(BaseSettings):
    title: str = "warg studio"
    description: str = "A collection of APIs to perform \
        and monitor chaos Engineering"
    DbURL: str = environ["DbURL"]
    Database_name: str = "WargDb"
    Collection_name: str = "WargCollection"
    MinioUrl: str = environ["storageUrl"]
    MinioAcessKey: str = environ["storageAccessKey"]
    MinioSecretKry: str = environ["storageSecretKey"]


_setting = Setting()
