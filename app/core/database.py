from sqlalchemy import create_engine, sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# Creating da connection
pg_db = create_engine(settings.PG_DATABASE_URL)

# Creating session
session = sessionmaker(bind=pg_db, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():
    data_base = session()
    try:
        yield data_base
    finally:
        data_base.close()
