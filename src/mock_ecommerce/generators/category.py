from typing import List, Dict
from mock_ecommerce.generators.base import BaseGenerator
from mock_ecommerce.database.ddl import TBL_CATEGORY
from mock_ecommerce.schemas import CategorySchema
from mock_ecommerce.database import bulk_insert, get_db_connection
from mock_ecommerce.utils.logger import logger
from mock_ecommerce.config import settings

class CategoryGenerator(BaseGenerator):
    def __init__(self, volume_l1: int=None, volume_l2: int=None, faker_instance=None):
        # Static list for category name
        self.category_map = settings.CATEGORY_MAP
        # Calculate default vols
        max_l1 = len(self.category_map)
        self.volume_l1 = volume_l1 if volume_l1 is not None else max_l1

        if volume_l2 is not None:
            self.volume_l2 = volume_l2
        else:
            selected_keys = list(self.category_map.keys())[:self.volume_l1]
            self.volume_l2 = sum(len(self.category_map[k]) for k in selected_keys)

        if volume_l1 > len(self.category_map):
            logger.warning(
                f"Requested volume_l1={volume_l1} but only "
                f"{len(self.category_map)} main categories available to use."
            )

        total_volume = self.volume_l1 + self.volume_l2
        super().__init__(total_volume, faker_instance)
        self.table_name = TBL_CATEGORY


    def generate(self, specific_names: List[str] = None) -> List[CategorySchema]:
        """Gen parent category"""
        records: List[CategorySchema] = []

        if specific_names is not None:
            target_names = specific_names
        else:
            all_names = list(self.category_map.keys())
            limit = min(self.volume_l1, len(all_names))
            target_names = all_names[:limit]

        for main_name in target_names:
            record: CategorySchema = {
                "category_name": main_name,
                "parent_category_id": None,
                "level": 1,
                "created_at": self.faker.date_time_between(start_date='-5y', end_date='-2y')
            }
            records.append(record)

        return records

    def generate_level_2(self, parent_map: Dict[str, int]) -> List[CategorySchema]:
        """Gen sub category
        Args:
            parent_ids: List of category_id from DB where level=1.
            parent_names: List of category_name corresponding to IDs (to map subtypes).
        """
        records: List[CategorySchema] = []

        for main_name, parent_id in parent_map.items():
            sub_list = self.category_map.get(main_name, [])
            for sub_name in sub_list:
                if 0 < self.volume_l2 <= len(records):
                    return records

                record: CategorySchema = {
                    "category_name": sub_name,
                    "parent_category_id": parent_id,
                    "level": 2,
                    "created_at": self.faker.date_time_between(start_date='-2y', end_date='now')
                }
                records.append(record)
        return records

def generate_categories_full(gen: CategoryGenerator):
    # ==============================
    # Fetch current data
    # ==============================
    existing_l1 = set()
    existing_l2 = set()
    parent_map = {} # {name: id}

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Load L1
            cur.execute(f"SELECT category_name, category_id FROM {TBL_CATEGORY} WHERE level = 1")
            for row in cur.fetchall():
                existing_l1.add(row[0])
                parent_map[row[0]] = row[1]
            # Load L2
            cur.execute(f"SELECT category_name FROM {TBL_CATEGORY} WHERE level = 2")
            existing_l2 = {row[0] for row in cur.fetchall()}

    # ==============================
    # Insert level 1 (main)
    # ==============================
    target_l1 = list(gen.category_map.keys())[:gen.volume_l1]
    missing_l1 = [n for n in target_l1 if n not in existing_l1]

    if missing_l1:
        logger.info(f"[Category] Generating {len(missing_l1)} Level 1...")
        bulk_insert(TBL_CATEGORY, gen.generate(specific_names=missing_l1))
        # Refresh parent_map
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT category_name, category_id FROM {TBL_CATEGORY} WHERE level = 1")
                parent_map = {row[0]: row[1] for row in cur.fetchall()}

    # ==============================
    # Insert level 2
    # ==============================
    l2_candidates = gen.generate_level_2(parent_map)
    new_l2 = [r for r in l2_candidates if r['category_name'] not in existing_l2]

    if new_l2:
        logger.info(f"[Category] Generating {len(new_l2)} NEW Level 2...")
        bulk_insert(TBL_CATEGORY, new_l2)

    total = len(missing_l1) + len(new_l2)
    logger.info(f"[Category] Finished. New records: {total}")
    return total

if __name__ == "__main__":
    gen = CategoryGenerator(volume_l1=3)
    generate_categories_full(gen)
