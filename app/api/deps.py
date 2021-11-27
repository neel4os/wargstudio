from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorCollection
from app.repositories.session import DbSession


async def get_db() -> AsyncIOMotorCollection:
    return DbSession().collection