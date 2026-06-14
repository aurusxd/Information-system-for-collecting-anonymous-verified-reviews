from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from log import log

import os



DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", "5432")

    if not all([db_user, db_password, db_name]):
        log.exception("PostgreSQL configuration is required. Set DATABASE_URL or DB_USER, DB_PASSWORD, DB_NAME.")

    DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

if not DATABASE_URL.startswith("postgresql"):
    log.critical("DATABASE_URL must use PostgreSQL: postgresql://...")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        log.error(f"PostgreSQL недоступен: {e}")
        return False


def init_db():
    try:
        log.info("Создание таблиц")
        Base.metadata.create_all(bind=engine)
        log.info("Таблицы успешно созданы")
    except Exception as e:
        log.error(f"Ошибка создания таблиц: {e}")
        raise