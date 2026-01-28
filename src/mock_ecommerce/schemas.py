from typing import TypedDict, Optional
from datetime import datetime

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
