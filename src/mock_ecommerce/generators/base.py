from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from faker import Faker

from mock_ecommerce.utils.logger import logger
from mock_ecommerce.database import bulk_insert
from mock_ecommerce.config import settings
from .exceptions import DataValidationError

class BaseGenerator(ABC):

    def __init__(self, volume: int = 0, faker_instance: Optional[Faker] = None):
        """
        volume:
        faker_instance:
        """
        self.volume = volume
        self.faker = faker_instance or Faker(locale=settings.LOCALE)

        self.records: List[Dict[str, Any]] = []

        self.table_name = None

    @abstractmethod
    def generate(self) -> List[Dict[str, Any]]:
        pass

    def validate(self) -> bool:
        # TODO
        return True

    def insert(self, table_name: str) -> int:
        """Bulk insert records"""
        if not table_name:
            raise ValueError("Table name must be provided for insertion.")
        return bulk_insert(self.table_name, self.records)

    def run(self, table_name: str) -> int:
        """Flow: Generate -> Validate -> Insert"""
        logger.info(f"[Generator] Starting generation for table '{table_name}' (Target: {self.volume} rows)...")

        try:
            # 1. Generate
            self.records = self.generate()
            count = len(self.records)
            logger.info(f"\tGenerated {count} records in memory.")

            # 2. Validate
            if self.validate():
                # 3. Insert
                inserted_count = self.insert(table_name)
                return inserted_count

            return 0
        except Exception as e:
            logger.error(f"Generator process failed for '{table_name}': {e}")
            raise e
