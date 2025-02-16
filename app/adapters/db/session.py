from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import config

engine = create_async_engine(
    config.SQLALCHEMY_DATABASE_URI,
    echo=config.DEBUG,  # выключите или включите при необходимости
    future=True
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
