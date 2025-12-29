"""
資料庫連線設定
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

# 建立資料庫引擎
# SQLite 需要特殊設定
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug   # 開發模式顯示 SQL
)

# 建立 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 建立 Base class
Base = declarative_base()


def get_db():
    """
    取得資料庫 session（依賴注入用）
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
