from pathlib import Path
from sqlalchemy.ext.declarative import declarative_base
import core.config as config
import logging
import os


logger = logging.getLogger(__name__)

Base = declarative_base()

database = config.DB
user = config.DB_USER
pw = config.DB_PASSWORD
server = config.DB_SERVER
port = config.DB_PORT
name = config.DB_NAME


def _build_sqlite_url() -> str:
    default_path = Path(
        os.getenv(
            "SQLITE_DB_PATH",
            Path(__file__).resolve().parent.parent / "garam.sqlite3",
        )
    )
    default_path.parent.mkdir(parents=True, exist_ok=True)
    logger.warning(
        "데이터베이스 환경 변수를 찾을 수 없어 SQLite 파일(%s)을 사용합니다.",
        default_path,
    )
    return f"sqlite:///{default_path}"


def _build_database_url() -> str:
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    if all([database, user, pw, server, port, name]):
        return f"{database}://{user}:{pw}@{server}:{port}/{name}"

    return _build_sqlite_url()


DATABASE_URL = _build_database_url()

