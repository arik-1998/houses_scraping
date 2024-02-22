import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    'sqlite+aiosqlite:///app/houses.db'
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class BaseDBModel(DeclarativeBase):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseDBModel.metadata.drop_all)