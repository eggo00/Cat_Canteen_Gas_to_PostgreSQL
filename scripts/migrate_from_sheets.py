"""
從 Google Sheets 遷移資料到 PostgreSQL
（可選用，如果需要保留 Google Sheets 的歷史訂單資料）
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.models.order import Order
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate_from_sheets():
    """
    從 Google Sheets 遷移資料

    使用方式：
    1. 從 Google Sheets 匯出為 CSV
    2. 讀取 CSV 檔案
    3. 將資料寫入 PostgreSQL
    """
    logger.info("開始資料遷移...")

    # TODO: 實作資料遷移邏輯
    # 1. 讀取 Google Sheets CSV
    # 2. 解析資料
    # 3. 寫入 PostgreSQL

    logger.info("資料遷移完成！")


if __name__ == "__main__":
    migrate_from_sheets()
