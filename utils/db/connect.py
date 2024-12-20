from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from utils.db.config import psql_url
import functools
import typing


engine = create_async_engine(psql_url)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


def connect_psql(func: typing.Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            result = await func(*args, session=session, **kwargs)
        return result
    return wrapper
