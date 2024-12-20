from utils.db.connect import connect_psql, create_async_engine, engine
from utils.db.basic import Base
from sqlalchemy.ext.asyncio import AsyncSession
from utils.db.models import StartWarsPeople


async def initial_models(engine_: create_async_engine = engine) -> None:
    async with engine_.begin() as session:
        import utils.db.models  # noqa
        await session.run_sync(Base.metadata.create_all)


@connect_psql
async def save_data_to_db(data: list[dict], session: AsyncSession) -> None:
    records = [StartWarsPeople(**d) for d in data]
    session.add_all(records)
    await session.commit()
