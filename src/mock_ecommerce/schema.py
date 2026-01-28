from typing import TypedDict
from datetime import datetime

class BrandSchema(TypedDict):
    # brand_id: int
    brand_name: str
    country: str
    created_at: datetime
