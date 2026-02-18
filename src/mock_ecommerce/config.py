import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import date

from mock_ecommerce.utils.logger import setup_logging
from mock_ecommerce.constants import DiscountType, PromotionType, OrderStatus

# ===================================================
# Setup env file
# ===================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env", override=True)

# ===================================================
# Setup logging
# ===================================================
env_log_dir = os.getenv("LOG_DIR", "logs")
LOG_DIR_PATH = (BASE_DIR / env_log_dir).resolve()
logger = setup_logging(log_dir=str(LOG_DIR_PATH))

# ===================================================
# Config
# ===================================================
class BaseConfig:
    """Base configuration (for all env settings)"""

    # --- System path ---
    DEFAULT_LOG_DIR = LOG_DIR_PATH

    # --- Database Config ---
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "ecommerce_synth")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # --- Faker setting ---
    LOCALE = 'vi_VN'
    RANDOM_SEED = 42

    # --- Business constants ---
    CATEGORY_MAP = {
            "Electronics": ["Mobile Phones", "Laptops", "Tablets", "Cameras", "Accessories"],
            "Fashion": ["Men Clothing", "Women Clothing", "Shoes", "Watches", "Bags"],
            "Home & Living": ["Furniture", "Decor", "Kitchenware", "Bedding", "Lighting"],
            "Beauty & Health": ["Skincare", "Makeup", "Supplements", "Personal Care"],
            "Books": ["Fiction", "Non-fiction", "Education", "Comics"],
            "Sports": ["Gym", "Running", "Team Sports", "Outdoor"],
            "Toys": ["Board Games", "Action Figures", "Dolls", "Educational"],
            "Automotive": ["Car Accessories", "Motorbike Accessories", "Oils & Fluids"]
        }
    SELLER_TYPES = ['Official', 'Marketplace']
    SELLER_TYPE_WEIGHTS = [0.3, 0.7]
    PROMOTION_TYPES = [promo_type.value for promo_type in PromotionType]
    DISCOUNT_TYPES = [DiscountType.PERCENTAGE.value, DiscountType.FIXED_AMOUNT.value]
    DISCOUNT_TYPE_WEIGHTS = [0.7, 0.3]

    # Transactional data
    ORDER_STATUS = [
        OrderStatus.PLACED.value,
        OrderStatus.PAID.value,
        OrderStatus.SHIPPED.value,
        OrderStatus.DELIVERED.value,
        OrderStatus.CANCELLED.value,
        OrderStatus.RETURNED.value
    ]
    ORDER_STATUS_WEIGHTS = [0.05, 0.04, 0.11, 0.70, 0.07, 0.03]

    ORDER_START_DATE = date(2025, 8, 1)
    ORDER_END_DATE = date(2025, 10, 31)

class DevConfig(BaseConfig):
    ENV_NAME = 'DEV'

    # --- Master Data ---
    NUM_BRANDS = 20
    NUM_CATEGORIES = 10
    NUM_SELLERS = 25

    # --- Reference Data ---
    NUM_PRODUCTS = 2000
    PRODUCT_COUNT_RANGE = (60, 100) # Avg 80/seller
    NUM_PROMOTIONS = 10
    NUM_PROMO_PRODUCTS = 100

    # --- Transaction Data--
    NUM_ORDERS = 50000
    NUM_ORDER_ITEMS_RANGE = (2, 4)

def get_config():
    env = os.getenv("ENV_NAME", "dev").upper()
    logger.info(f"Env: {env}")
    if env == "DEV":
        return DevConfig()

    return BaseConfig()

settings = get_config()
