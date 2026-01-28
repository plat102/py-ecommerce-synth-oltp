import random
from typing import List
from mock_ecommerce.generators.base import BaseGenerator
from mock_ecommerce.database.ddl import TBL_SELLER
from mock_ecommerce.schemas import SellerSchema
from mock_ecommerce.config import settings

class SellerGenerator(BaseGenerator):
    def __init__(self, volume: int, faker_instance=None):
        super().__init__(volume, faker_instance)
        self.table_name = TBL_SELLER

    def generate(self) -> List[SellerSchema]:
        data: List[SellerSchema] = []

        # Get seller settings
        types = settings.SELLER_TYPES
        weights = settings.SELLER_TYPE_WEIGHTS

        for _ in range(self.volume):
            type = random.choices(types, weights=weights, k=1)[0]
            rating = round(random.uniform(0, 1), 2)
            join_date = self.faker.date_between(start_date='-4y', end_date='-1M')

            record: SellerSchema = {
                "seller_name": self.faker.company(),
                "join_date": join_date,
                "seller_type": type,
                "rating": rating,
                "country": "Vietnam",
                "created_at": self.faker.date_time_between(start_date=join_date, end_date='now')
            }
            data.append(record)

        return data

if __name__ == "__main__":
    # Test dry run
    gen = SellerGenerator(volume=5)
    print("--- Sample Records ---")
    for r in gen.generate():
        print(r)
    # gen.run(table_name='seller')
