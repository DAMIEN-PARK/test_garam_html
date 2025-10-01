from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker
import database.base as base
import psycopg2
import sqlite3

database_url = base.DATABASE_URL

engine_kwargs = {"echo": True}

if database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_connection():
    url = make_url(database_url)

    if url.drivername.startswith("sqlite"):
        return sqlite3.connect(url.database)

    return psycopg2.connect(
        host=url.host,
        dbname=url.database,
        user=url.username,
        password=url.password,
        port=url.port,
    )
