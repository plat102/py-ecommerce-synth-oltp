import random
from datetime import timedelta, date
from typing import List
from decimal import Decimal

from mock_ecommerce.generators.base import BaseGenerator
from mock_ecommerce.database.ddl import TBL_PROMOTION
from mock_ecommerce.schemas import PromotionSchema
from mock_ecommerce.config import settings
from mock_ecommerce.constants import DiscountType

class PromotionGenerator(BaseGenerator):

    def __init__(self, volume: int, faker_instance=None):
        super().__init__(volume, faker_instance)
        self.table_name = TBL_PROMOTION

    def generate(self):
        data : List[PromotionSchema] = []

        # Get static lists
        campaign_prefixes = [
            "Summer Sale", "Black Friday", "Cyber Monday", "Tet Holiday",
            "Back to School", "Flash Sale", "Mid-Month Sale", "Payday Sale",
            "Clearance", "New Arrival"
        ]
        promotion_types = settings.PROMOTION_TYPES
        discount_types = settings.DISCOUNT_TYPES
        discount_type_weights = settings.DISCOUNT_TYPE_WEIGHTS

        for _ in range(self.volume):
            promotion_name = f'{random.choice(campaign_prefixes)} {self.faker.name()}'

            start_date = self.faker.date_between(start_date="-1y", end_date="+2M")
            duration = random.randint(30, 50)
            end_date: date = start_date + timedelta(days=duration)

            discount_type = random.choices(discount_types, weights=discount_type_weights, k=1)[0]
            if discount_type == DiscountType.PERCENTAGE.value:
                val = random.randrange(5, 55, 5)
                discount_value = Decimal(val)
            elif discount_type == DiscountType.FIXED_AMOUNT.value:
                val = random.choice([10, 20, 50, 100, 200, 500]) * 1000
                discount_value = Decimal(val)
            else:
                discount_value = Decimal(0)

            record : PromotionSchema = {
                "promotion_name": promotion_name,
                "promotion_type": random.choice(promotion_types),
                "discount_type": discount_type,
                "discount_value": discount_value,
                "start_date": start_date,
                "end_date": end_date,
                "created_at": self.faker.date_time_between(
                    start_date=start_date - timedelta(days=random.randint(1, 30)),
                    end_date=start_date
                )
            }

            data.append(record)

        return data

if __name__ == "__main__":
    gen = PromotionGenerator(volume=5)
    records = gen.generate()
    print(f"--- Sample Promotions ({len(records)}) ---")
    print(records)
    gen.run(TBL_PROMOTION)
