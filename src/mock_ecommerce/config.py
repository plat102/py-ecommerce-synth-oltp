import os
from pathlib import Path
from dotenv import load_dotenv
from mock_ecommerce.utils.logger import setup_logging
from mock_ecommerce.constants import DiscountType, PromotionType

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
    SELLER_TYPES = ['Official', 'Marketplace']
    SELLER_TYPE_WEIGHTS = [0.3, 0.7]
    PROMOTION_TYPES = [promo_type.value for promo_type in PromotionType]
    DISCOUNT_TYPES = [DiscountType.PERCENTAGE.value, DiscountType.FIXED_AMOUNT.value]
    DISCOUNT_TYPE_WEIGHTS = [0.7, 0.3]

class DevConfig(BaseConfig):
    ENV_NAME = 'DEV'

def get_config():
    env = os.getenv("ENV_NAME", "dev").upper()
    logger.info(f"Env: {env}")
    if env == "DEV":
        return DevConfig()

    return BaseConfig()

settings = get_config()
