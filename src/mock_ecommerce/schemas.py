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

class PromotionSchema(TypedDict):
    promotion_name: str
    promotion_type: str
    discount_type: str
    discount_value: Decimal
    start_date: date
    end_date: date
    created_at: datetime

class PromotionProduct(TypedDict):
    promo_product_id: int
    promotion_id: int
    product_id: int
    created_at: datetime

class PromotionProductSchema(TypedDict):
    promotion_id: int
    product_id: int
    created_at: datetime

class OrderSchema(TypedDict):
    order_date: datetime
    seller_id: int
    status: str
    total_amount: Decimal
    created_at: datetime

class OrderItemSchema(TypedDict):
    order_id: int
    product_id: int
    order_date: datetime
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    created_at: datetime
