from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import Settings

engine = create_async_engine(Settings().DATABASE_URL)  # type: ignore

SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)


@asynccontextmanager
async def session_scope():
    session = SessionFactory()

    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
