from redis import Redis
from rq import Queue
from app.core.config.settings import _setting
from app.core.util.singleton import Singleton


class RedisQueue(metaclass=Singleton):
    def __init__(self) -> None:
        self._redis_connection = Redis(host="localhost", port=6379, db=0)
        self._queue = Queue(connection=self._redis_connection)

    @property
    def queue(self) -> Queue:
        return self._queue
