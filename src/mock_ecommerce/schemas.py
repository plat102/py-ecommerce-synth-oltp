from typing import TypedDict, Optional
from datetime import datetime, date

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
    # seller_id là SERIAL
    seller_name: str
    join_date: date
    seller_type: str
    rating: float
    country: str
    created_at: datetime
