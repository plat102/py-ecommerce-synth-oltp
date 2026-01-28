from mock_ecommerce.config import settings
from mock_ecommerce.generators import (
    BrandGenerator,
    CategoryGenerator, generate_categories_full,
    SellerGenerator,
    PromotionGenerator,
    ProductGenerator,
    PromotionProductGenerator
)
from mock_ecommerce.database import get_existing_ids
from mock_ecommerce.database.ddl import TBL_BRAND, TBL_SELLER, TBL_CATEGORY, TBL_PROMOTION, TBL_PRODUCT
from mock_ecommerce.utils.logger import logger

def generate_brand():
    logger.info(f'[Task] Generating brands (target: {settings.NUM_BRANDS}')

    gen = BrandGenerator(volume=settings.NUM_BRANDS)
    inserted = gen.run()
    return inserted

def generate_category():
    logger.info(f'[Task] Generating categories (target: {settings.NUM_CATEGORIES})')

    gen = CategoryGenerator(volume_l1=settings.NUM_CATEGORIES)
    inserted = generate_categories_full(gen)
    return inserted

def generate_seller():
    logger.info(f'[Task] Generating sellers (target: {settings.NUM_SELLERS}')

    gen = SellerGenerator(volume=settings.NUM_SELLERS)
    inserted = gen.run()
    return inserted

def generate_promotion():
    volume = settings.NUM_PROMOTIONS
    logger.info(f"[Task] Generating Promotions (Target: {volume})...")

    gen = PromotionGenerator(volume=volume)
    inserted = gen.run()
    return inserted

def generate_product():
    volume = settings.NUM_PRODUCTS
    logger.info(f"[Task] Generating Products (Target: {volume})...")

    # Refresh Cache ID
    logger.info("Refreshing FK Cache for Product dependencies...")
    get_existing_ids(TBL_BRAND, 'brand_id', force_refresh=True)
    get_existing_ids(TBL_CATEGORY, 'category_id', force_refresh=True)
    get_existing_ids(TBL_SELLER, 'seller_id', force_refresh=True)

    gen = ProductGenerator(volume=volume)
    inserted = gen.run()
    return inserted

def generate_promotion_product():
    volume = settings.NUM_PROMO_PRODUCTS
    logger.info(f"[Task] Generating Promotion-Product (Target: {volume})...")

    logger.info("Refreshing FK Cache...")
    get_existing_ids(TBL_PROMOTION, 'promotion_id', force_refresh=True)
    get_existing_ids(TBL_PRODUCT, 'product_id', force_refresh=True)

    gen = PromotionProductGenerator(volume=volume)
    inserted = gen.run()
    return inserted
