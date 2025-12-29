"""
訂單資料驗證 Schema（Pydantic）
對應原本 GAS Code.gs 中的 submitOrder 驗證邏輯
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class MenuItem(BaseModel):
    """餐點項目"""
    id: str = Field(..., description="餐點 ID")
    name: str = Field(..., min_length=1, max_length=100, description="餐點名稱")
    quantity: int = Field(..., gt=0, le=99, description="數量（1-99）")
    price: int = Field(..., gt=0, description="單價")

    @field_validator('id')
    @classmethod
    def validate_item_id(cls, v):
        """驗證餐點 ID（對應 Code.gs line 82-94）"""
        valid_ids = ['m1', 'm2', 'm3', 'm4', 's1', 's2', 's3',
                     'd1', 'd2', 'd3', 'd4', 'dr1', 'dr2', 'dr3', 'dr4', 'dr5']
        if v not in valid_ids:
            raise ValueError('無效的餐點 ID')
        return v


class DrinkItem(MenuItem):
    """飲料項目（含溫度和甜度）"""
    temperature: Optional[str] = Field(None, description="溫度")
    sweetness: Optional[str] = Field(None, description="甜度")

    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v):
        """驗證溫度選項"""
        if v is not None:
            valid_temps = ['正常冰', '少冰', '微冰', '去冰', '溫', '熱']
            if v not in valid_temps:
                raise ValueError('無效的溫度選項')
        return v

    @field_validator('sweetness')
    @classmethod
    def validate_sweetness(cls, v):
        """驗證甜度選項"""
        if v is not None:
            valid_sweetness = ['正常糖', '少糖', '半糖', '微糖', '無糖']
            if v not in valid_sweetness:
                raise ValueError('無效的甜度選項')
        return v


class OrderCreate(BaseModel):
    """建立訂單的請求資料（對應 Code.gs submitOrder 的驗證）"""
    customerName: str = Field(..., min_length=1, max_length=50, alias="customerName", description="顧客姓名")
    diningOption: str = Field(..., alias="diningOption", description="取餐方式")
    note: Optional[str] = Field(None, max_length=200, description="備註")
    items: List[MenuItem] = Field(..., min_length=1, max_length=50, description="餐點項目")
    totalAmount: int = Field(..., gt=0, alias="totalAmount", description="總金額")

    @field_validator('customerName')
    @classmethod
    def sanitize_name(cls, v):
        """清理姓名（對應 Code.gs sanitizeInput）"""
        v = v.strip()
        # 移除 HTML 標籤和特殊字元
        v = v.replace('<', '&lt;').replace('>', '&gt;')
        v = v.replace('"', '&quot;').replace("'", '&#x27;')
        v = v.replace('/', '&#x2F;')
        return v

    @field_validator('diningOption')
    @classmethod
    def validate_dining_option(cls, v):
        """驗證取餐方式（對應 Code.gs line 58-65）"""
        valid_options = ['內用', '外帶']
        if v not in valid_options:
            raise ValueError('取餐方式必須是「內用」或「外帶」')
        return v

    @field_validator('note')
    @classmethod
    def sanitize_note(cls, v):
        """清理備註"""
        if v:
            v = v.strip()
            v = v.replace('<', '&lt;').replace('>', '&gt;')
            v = v.replace('"', '&quot;').replace("'", '&#x27;')
            v = v.replace('/', '&#x2F;')
        return v

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "customerName": "王小明",
                "diningOption": "內用",
                "note": "不要香菜",
                "items": [
                    {"id": "m1", "name": "貓爪咖哩飯", "quantity": 1, "price": 120},
                    {"id": "dr1", "name": "貓爪拿鐵", "quantity": 1, "price": 80, "temperature": "熱", "sweetness": "正常糖"}
                ],
                "totalAmount": 200
            }
        }
    }


class OrderResponse(BaseModel):
    """訂單回應資料"""
    id: int
    order_number: str
    customer_name: str
    pickup_method: str
    total_amount: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class OrderSuccessResponse(BaseModel):
    """訂單成功回應（對應 Code.gs line 139-143）"""
    success: bool = True
    message: str = "喵～訂單已送出！"
    orderNumber: str = Field(..., alias="orderNumber")

    model_config = {
        "populate_by_name": True
    }


class OrderErrorResponse(BaseModel):
    """訂單錯誤回應"""
    success: bool = False
    message: str
