from typing import Collection
from pydantic import BaseSettings
from os import environ

class Setting(BaseSettings):
    title : str = "warg studio" 
    description: str = "A collection of APIs to perform and monitor chaos application"
    DbURL: str = environ.get("DbURL")
    Database_name : str = "WargDb"
    Collection_name: str = "WargCollection"


_setting = Setting()