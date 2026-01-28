from mock_ecommerce.config import settings
from mock_ecommerce.generators import BrandGenerator
from mock_ecommerce.utils.logger import logger

def generate_brand():
    logger.info(f'[Task] Generating brands (target: {settings.NUM_BRANDS}')

    gen = BrandGenerator(volume=settings.NUM_BRANDS)
    gen.run()
