import random
from typing import List, Dict, Any
from mock_ecommerce.generators.base import BaseGenerator
from mock_ecommerce.database.ddl import TBL_BRAND
from mock_ecommerce.schema import BrandSchema

class BrandGenerator(BaseGenerator):
    def __init__(self, volume: int, faker_instance=None):
        super().__init__(volume, faker_instance)
        self.table_name = TBL_BRAND

    def generate(self) -> List[BrandSchema]:
        data: List[BrandSchema] = []

        # Countries
        countries = ['Vietnam', 'China', 'USA', 'Korea', 'Japan', 'Germany']
        weights = [40, 25, 15, 10, 5, 5]  # sum: 100%

        for _ in range(self.volume):
            record: BrandSchema = {
                "brand_name": self.faker.company(),
                # "country": random.choices(countries, weights=weights, k=1)[0],
                "country": self.faker.country(),
                "created_at": self.faker.date_time_this_decade()
            }
            data.append(record)

        return data

if __name__ == "__main__":
    # Test dry run
    gen = BrandGenerator(volume=5)
    print("--- Sample Records ---")
    for r in gen.generate():
        print(r)
    # gen.run(table_name='brand')
