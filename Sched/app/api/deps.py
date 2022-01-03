from rq.queue import Queue

from app.repositories.session import RedisQueue


async def get_db() -> Queue:
    return RedisQueue().queue
