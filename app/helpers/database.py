# import datetime

# from sqlalchemy import Column, DateTime, create_engine
# from sqlalchemy.orm import Session, declarative_base, sessionmaker

# from app.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine = create_engine(DATABASE_URL)

# Base = declarative_base()

# SessionLocal = sessionmaker(bind=engine)


# def get_db() -> Session:
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# class BaseDBModel(Base):
#     __abstract__ = True

#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow)

# def create_database():
#     Base.metadata.create_all(bind=engine)


import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, future=True)

async_session = async_sessionmaker(bind=engine)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


class BaseDBModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

def create_database():
    Base.metadata.create_all(bind=engine)