import os
from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.environ.get("SQLITE_PATH", "sqlite:///./data/sql_app.db")

engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={'check_same_thread': False}
)

# データベースに接続する一連の流れを作る
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
