import random
from typing import List
from decimal import Decimal

from mock_ecommerce.generators.base import BaseGenerator
from mock_ecommerce.database.ddl import TBL_PRODUCT, TBL_BRAND, TBL_CATEGORY, TBL_SELLER
from mock_ecommerce.schemas import ProductSchema
from mock_ecommerce.database import get_existing_ids
from mock_ecommerce.utils.logger import logger

class ProductGenerator(BaseGenerator):
    def __init__(self, volume: int, faker_instance=None):
        super().__init__(volume, faker_instance)
        self.table_name = TBL_PRODUCT

    def generate(self) -> List[ProductSchema]:
        # Get FKs
        brand_ids = get_existing_ids(TBL_BRAND, 'brand_id')
        category_ids = get_existing_ids(TBL_CATEGORY, 'category_id')
        seller_ids = get_existing_ids(TBL_SELLER, 'seller_id')

        if not (brand_ids and category_ids and seller_ids):
            logger.error('Missing required master data')
            return []

        data: List[ProductSchema] = []

        for _ in range(self.volume):
            price = Decimal(random.uniform(100000, 50000000))
            discount_price = price * Decimal(random.uniform(0.7, 1.0))

            record: ProductSchema = {
                'product_name': self.faker.catch_phrase(),

                'category_id': random.choice(category_ids),
                'brand_id': random.choice(brand_ids),
                'seller_id': random.choice(seller_ids),

                'price': price,
                'discount_price': discount_price,

                'stock_qty': random.randint(0,500),
                'rating': round(random.uniform(3,5),1),

                'created_at': self.faker.date_time_between(start_date='-3y', end_date='now'),

                # 95 active
                'is_active': random.choices([True, False], weights=[95, 5], k=1)[0],
            }
            data.append(record)

        return data


if __name__ == "__main__":
    gen = ProductGenerator(volume=5)
    records = gen.generate()

    print(f"--- Sample Product ---")
    print(records)
    gen.run(table_name=TBL_PRODUCT)
