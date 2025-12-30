"""
Analytics API Routes
提供資料分析功能的 API 端點
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    RevenueResponse,
    AverageOrderValueResponse,
    PopularItemsResponse,
    PickupMethodRatioResponse,
    PeakHoursResponse,
    BeveragePreferenceResponse
)
from datetime import date as DateType
from typing import Optional
import logging

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
logger = logging.getLogger(__name__)


# ========== Revenue Endpoints ==========

@router.get("/revenue/daily", response_model=RevenueResponse)
async def get_daily_revenue(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    取得每日營收分析

    - **start_date**: 開始日期（可選，預設為 30 天前）
    - **end_date**: 結束日期（可選，預設為今天）

    返回每日營收、訂單數量及總計
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_daily_revenue(db, start_date, end_date)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting daily revenue: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


@router.get("/revenue/weekly", response_model=RevenueResponse)
async def get_weekly_revenue(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    取得每週營收分析

    返回以週為單位的營收統計
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_weekly_revenue(db, start_date, end_date)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting weekly revenue: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


@router.get("/revenue/monthly", response_model=RevenueResponse)
async def get_monthly_revenue(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    取得每月營收分析

    返回以月為單位的營收統計
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_monthly_revenue(db, start_date, end_date)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting monthly revenue: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


@router.get("/revenue/average-order-value", response_model=AverageOrderValueResponse)
async def get_average_order_value(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    取得平均客單價

    計算指定期間的平均每筆訂單金額
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_average_order_value(db, start_date, end_date)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting average order value: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


# ========== Popular Items Endpoints ==========

@router.get("/popular-items/dishes", response_model=PopularItemsResponse)
async def get_popular_dishes(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=100, description="返回前幾名商品"),
    db: Session = Depends(get_db)
):
    """
    取得最受歡迎的餐點排行

    - **limit**: 返回前幾名（1-100，預設 10）

    依銷售數量排序，返回熱門餐點（不含飲料）
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_popular_dishes(db, start_date, end_date, limit)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting popular dishes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


@router.get("/popular-items/drinks", response_model=PopularItemsResponse)
async def get_popular_drinks(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    limit: int = Query(10, ge=1, le=100, description="返回前幾名商品"),
    db: Session = Depends(get_db)
):
    """
    取得最受歡迎的飲料排行

    - **limit**: 返回前幾名（1-100，預設 10）

    依銷售數量排序，返回熱門飲料
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_popular_drinks(db, start_date, end_date, limit)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting popular drinks: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


# ========== Customer Behavior Endpoints ==========

@router.get("/customer-behavior/pickup-method-ratio", response_model=PickupMethodRatioResponse)
async def get_pickup_method_ratio(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    分析內用與外帶比例

    返回內用、外帶的訂單數量、百分比及營收
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_pickup_method_ratio(db, start_date, end_date)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting pickup method ratio: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


@router.get("/customer-behavior/peak-hours", response_model=PeakHoursResponse)
async def get_peak_hours(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    分析尖峰時段

    返回每小時的訂單數量和營收，找出生意最好的時段
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_peak_hours(db, start_date, end_date)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting peak hours: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


# ========== Beverage Preference Endpoints ==========

@router.get("/beverage-preferences/ice-level", response_model=BeveragePreferenceResponse)
async def get_ice_level_preferences(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    分析冰度偏好

    統計顧客對飲料冰度的選擇分布（正常冰、少冰、微冰、去冰、溫、熱）
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_ice_level_preferences(db, start_date, end_date)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting ice level preferences: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")


@router.get("/beverage-preferences/sweetness", response_model=BeveragePreferenceResponse)
async def get_sweetness_preferences(
    start_date: Optional[DateType] = Query(None, description="開始日期 (YYYY-MM-DD)"),
    end_date: Optional[DateType] = Query(None, description="結束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    分析甜度偏好

    統計顧客對飲料甜度的選擇分布（正常糖、少糖、半糖、微糖、無糖）
    """
    try:
        start_date, end_date = AnalyticsService.validate_date_range(start_date, end_date)
        result = AnalyticsService.get_sweetness_preferences(db, start_date, end_date)
        return result
    except ValueError as e:
        logger.error(f"Invalid date range: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting sweetness preferences: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="系統錯誤")
