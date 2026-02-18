from datetime import date, datetime, timedelta
from typing import List
from decimal import Decimal
import random

from mock_ecommerce.database import get_existing_ids
from mock_ecommerce.database.ddl import TBL_ORDER, TBL_SELLER
from mock_ecommerce.generators.base import BaseGenerator
from mock_ecommerce.schemas import OrderSchema
from mock_ecommerce.config import settings
from mock_ecommerce.utils.logger import logger

class OrderGenerator(BaseGenerator):

    def __init__(self, volume: int, faker_instance=None):
        super().__init__(volume, faker_instance)
        self.table_name = TBL_ORDER

        # cache seller
        self.seller_ids = get_existing_ids(TBL_SELLER, 'seller_id')
        if not self.seller_ids:
            logger.warning('No seller_ids found.')

        # prepare date data
        self.start_date = datetime.combine(settings.ORDER_START_DATE, datetime.min.time())
        self.end_date = datetime.combine(settings.ORDER_END_DATE, datetime.max.time())
        self.date_range_seconds = int(
            (self.end_date - self.start_date).total_seconds()
        )

        # config weight & status
        self.status_opts = settings.ORDER_STATUS
        self.status_weights = settings.ORDER_STATUS_WEIGHTS

    def generate(self) -> List[OrderSchema]:
        if not self.seller_ids:
            return []
        data: List[OrderSchema] = []

        # Pre-calculate constants
        seller_ids = self.seller_ids
        status_opts = self.status_opts
        status_weights = self.status_weights
        start_date = self.start_date
        sec_range = self.date_range_seconds

        for _ in range(self.volume):
            # Random date
            random_sec = random.randint(0, sec_range)
            order_date = start_date + timedelta(seconds=random_sec)

            # Random status
            status = random.choices(status_opts, weights=status_weights, k=1)[0]

            # Create record
            record: OrderSchema = {
                "order_date": order_date,
                "seller_id": random.choice(seller_ids),
                "status": status,
                "total_amount": Decimal(0),
                "created_at": order_date
            }
            data.append(record)

        return data

if __name__ == "__main__":
    # Test generation logic (Dry run)
    try:
        # Test 10 records
        gen = OrderGenerator(volume=10)
        records = gen.generate()
        print(f"--- Sample Orders ({len(records)}) ---")
        for r in records[:5]:
            print(r)
    except Exception as e:
        print(f"Test failed: {e}")
