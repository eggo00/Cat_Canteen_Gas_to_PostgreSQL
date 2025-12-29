"""
資料庫初始化腳本
建立所有資料表
"""
import sys
import os

# 加入專案根目錄到 Python 路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine, Base
from app.models.order import Order
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """初始化資料庫"""
    try:
        logger.info("開始建立資料表...")

        # 建立所有資料表
        Base.metadata.create_all(bind=engine)

        logger.info("✅ 資料表建立成功！")
        logger.info("已建立的資料表：")
        logger.info("  - orders (訂單)")

    except Exception as e:
        logger.error(f"❌ 建立資料表失敗：{e}")
        raise


if __name__ == "__main__":
    init_database()
