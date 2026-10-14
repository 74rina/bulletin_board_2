import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    pass


# TODO(p3): .envの読み込みが開発環境だけで必要か整理し、設定の責務を分かりやすくする。
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # TODO(p2): 必須のDB環境変数が不足しているときに起動時に分かりやすく知らせる。
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_name = os.getenv("DB_NAME", "bulletin_board")
    # TODO(p2): DBパスワードに記号が含まれる場合でも接続URLが壊れないようにする。
    DATABASE_URL = (
        f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

engine = create_engine(
    DATABASE_URL,
    future=True,
    # TODO(p2): DB接続が切れた後も再接続しやすいエンジン設定を調べて追加する。
    # TODO(p3): SQLログを環境変数で有効化できるようにし、ORMが発行するSQLを学べるようにする。
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
# TODO(p2): テスト時にSessionLocalを差し替えやすくし、DBを使うAPIテストを書けるようにする。
