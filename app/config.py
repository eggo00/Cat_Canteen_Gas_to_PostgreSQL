"""
應用配置管理
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """應用設定"""

    # 應用基本資訊
    app_name: str = "Cat Claws 貓咪食堂"
    app_version: str = "2.0.0"
    debug: bool = False

    # 資料庫設定
    database_url: str = "postgresql://user:password@localhost:5432/cat_canteen"

    # 安全設定
    secret_key: str = "your-secret-key-change-this-in-production"

    # CORS 設定
    allowed_origins: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    """取得設定實例（使用快取）"""
    return Settings()
