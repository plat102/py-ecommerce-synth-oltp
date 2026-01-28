from enum import Enum

class DiscountType(str, Enum):
    PERCENTAGE = 'percentage'
    FIXED_AMOUNT = 'fixed_amount'

class PromotionType(str, Enum):
    PRODUCT = 'product'
    CATEGORY = 'category'
    SELLER = 'seller'
    FLASH_SALE = 'flash_sale'
    SEASONAL = 'seasonal'

class OrderStatus(str, Enum):
    PLACED = 'PLACED'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    DELIVERED = 'DELIVERED'
    CANCELLED = 'CANCELLED'
    RETURNED = 'RETURNED'
