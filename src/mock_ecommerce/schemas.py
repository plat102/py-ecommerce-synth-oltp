from typing import TypedDict, Optional
from datetime import datetime, date
from decimal import Decimal

class BrandSchema(TypedDict):
    # brand_id: int
    brand_name: str
    country: str
    created_at: datetime

class CategorySchema(TypedDict):
    # category_id: int
    category_name: str
    parent_category_id: Optional[int]
    level: int
    created_at: datetime

class SellerSchema(TypedDict):
    seller_name: str
    join_date: date
    seller_type: str
    rating: float
    country: str
    created_at: datetime

class ProductSchema(TypedDict):
    product_name: str
    category_id: int
    brand_id: int
    seller_id: int
    price: Decimal
    discount_price: Decimal
    stock_qty: int
    rating: float
    is_active: bool
    created_at: datetime
