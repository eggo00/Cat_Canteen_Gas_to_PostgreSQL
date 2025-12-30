"""
Analytics API Response Schemas
"""
from pydantic import BaseModel, Field
from typing import List
from datetime import date as DateType


# ========== Revenue Analysis Schemas ==========

class RevenueDataPoint(BaseModel):
    """Single revenue data point"""
    date: DateType = Field(..., description="日期")
    revenue: int = Field(..., description="總營收 (NT$)")
    order_count: int = Field(..., description="訂單數量")


class RevenueResponse(BaseModel):
    """Revenue analysis response"""
    period: str = Field(..., description="時間週期: daily/weekly/monthly")
    start_date: DateType = Field(..., description="開始日期")
    end_date: DateType = Field(..., description="結束日期")
    data: List[RevenueDataPoint] = Field(..., description="營收資料點列表")
    total_revenue: int = Field(..., description="總營收 (NT$)")
    total_orders: int = Field(..., description="總訂單數")


class AverageOrderValueResponse(BaseModel):
    """Average order value response"""
    start_date: DateType = Field(..., description="開始日期")
    end_date: DateType = Field(..., description="結束日期")
    average_order_value: float = Field(..., description="平均客單價 (NT$)")
    total_orders: int = Field(..., description="總訂單數")
    total_revenue: int = Field(..., description="總營收 (NT$)")


# ========== Popular Items Schemas ==========

class PopularItem(BaseModel):
    """Popular item data"""
    item_id: str = Field(..., description="商品ID")
    item_name: str = Field(..., description="商品名稱")
    total_quantity: int = Field(..., description="總銷售數量")
    total_revenue: int = Field(..., description="總營收 (NT$)")
    order_count: int = Field(..., description="出現在幾筆訂單中")


class PopularItemsResponse(BaseModel):
    """Popular items ranking response"""
    category: str = Field(..., description="類別: dishes/drinks")
    start_date: DateType = Field(..., description="開始日期")
    end_date: DateType = Field(..., description="結束日期")
    items: List[PopularItem] = Field(..., description="熱門商品列表")


# ========== Customer Behavior Schemas ==========

class PickupMethodStats(BaseModel):
    """Pickup method statistics"""
    pickup_method: str = Field(..., description="取餐方式: 內用/外帶")
    count: int = Field(..., description="訂單數量")
    percentage: float = Field(..., description="佔總訂單百分比")
    revenue: int = Field(..., description="總營收 (NT$)")


class PickupMethodRatioResponse(BaseModel):
    """Pickup method ratio response"""
    start_date: DateType = Field(..., description="開始日期")
    end_date: DateType = Field(..., description="結束日期")
    total_orders: int = Field(..., description="總訂單數")
    stats: List[PickupMethodStats] = Field(..., description="取餐方式統計")


class PeakHourData(BaseModel):
    """Peak hour statistics"""
    hour: int = Field(..., ge=0, le=23, description="小時 (0-23)")
    order_count: int = Field(..., description="訂單數量")
    revenue: int = Field(..., description="營收 (NT$)")


class PeakHoursResponse(BaseModel):
    """Peak hours analysis response"""
    start_date: DateType = Field(..., description="開始日期")
    end_date: DateType = Field(..., description="結束日期")
    hourly_data: List[PeakHourData] = Field(..., description="每小時資料")
    peak_hour: int = Field(..., description="尖峰時段 (小時)")
    peak_hour_orders: int = Field(..., description="尖峰時段訂單數")


# ========== Beverage Preference Schemas ==========

class PreferenceStats(BaseModel):
    """Preference statistics"""
    option: str = Field(..., description="偏好選項")
    count: int = Field(..., description="數量")
    percentage: float = Field(..., description="佔總數百分比")


class BeveragePreferenceResponse(BaseModel):
    """Beverage preference response"""
    preference_type: str = Field(..., description="偏好類型: ice_level/sweetness")
    start_date: DateType = Field(..., description="開始日期")
    end_date: DateType = Field(..., description="結束日期")
    total_drinks: int = Field(..., description="總飲料數")
    preferences: List[PreferenceStats] = Field(..., description="偏好統計")
    most_popular: str = Field(..., description="最受歡迎的選項")
