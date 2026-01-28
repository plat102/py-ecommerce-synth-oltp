import random
from typing import List, Set, Tuple
from mock_ecommerce.generators.base import BaseGenerator
from mock_ecommerce.database.ddl import TBL_PROMOTION_PRODUCT, TBL_PROMOTION, TBL_PRODUCT
from mock_ecommerce.schemas import PromotionProductSchema
from mock_ecommerce.database import get_existing_ids
from mock_ecommerce.utils.logger import logger


class PromotionProductGenerator(BaseGenerator):
    def __init__(self, volume: int, faker_instance=None):
        super().__init__(volume, faker_instance)
        self.table_name = TBL_PROMOTION_PRODUCT

    def generate(self) -> List[PromotionProductSchema]:
        promotion_ids = get_existing_ids(TBL_PROMOTION, 'promotion_id')
        product_ids = get_existing_ids(TBL_PRODUCT, 'product_id')

        if not (promotion_ids and product_ids):
            logger.error("Missing Promotion or Product data. Cannot link them.")
            return []

        data: List[PromotionProductSchema] = []
        existing_pairs: Set[Tuple[int, int]] = set() # unique pair

        max_combinations = len(promotion_ids) * len(product_ids)
        target_volume = min(self.volume, max_combinations)
        attempts = 0
        max_attempts = target_volume * 5

        # Avoiding infinite loop (when generated > max combination but target is not reach)
        while len(data) < target_volume and attempts < max_attempts:
            attempts += 1

            # --- Random 1 pair ---
            promo_id = random.choice(promotion_ids)
            prod_id = random.choice(product_ids)
            pair = (promo_id, prod_id)

            # If not exist
            if pair not in existing_pairs:
                existing_pairs.add(pair)
                record: PromotionProductSchema = {
                    "promotion_id": promo_id,
                    "product_id": prod_id,
                    "created_at": self.faker.date_time_this_year()
                }
                data.append(record)

        # --- If number of unique pairs < Volume ---
        if len(data) < self.volume:
            logger.warning(
                f"Only generated {len(data)}/{self.volume} unique pairs. "
                f"Max possible combinations: {max_combinations}"
            )

        return data

if __name__ == "__main__":
    try:
        gen = PromotionProductGenerator(volume=100000000)
        records = gen.generate()
        print(f"--- Sample Promo Links ({len(records)}) ---")
        for r in records[:5]:
            print(f"Promo {r['promotion_id']} - Product {r['product_id']}")

        gen.run(TBL_PROMOTION_PRODUCT)
    except Exception as e:
        print(f"Test skipped or failed: {e}")