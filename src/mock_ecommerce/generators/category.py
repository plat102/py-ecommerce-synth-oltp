from typing import List
from mock_ecommerce.generators.base import BaseGenerator
from mock_ecommerce.database.ddl import TBL_CATEGORY
from mock_ecommerce.schemas import CategorySchema
from mock_ecommerce.database import bulk_insert, get_existing_ids
from mock_ecommerce.utils.logger import logger

class CategoryGenerator(BaseGenerator):
    def __init__(self, volume_l1: int=None, volume_l2: int=None, faker_instance=None):
        # Static list for category name
        self.category_map = {
            "Electronics": ["Mobile Phones", "Laptops", "Tablets", "Cameras", "Accessories"],
            "Fashion": ["Men Clothing", "Women Clothing", "Shoes", "Watches", "Bags"],
            "Home & Living": ["Furniture", "Decor", "Kitchenware", "Bedding", "Lighting"],
            "Beauty & Health": ["Skincare", "Makeup", "Supplements", "Personal Care"],
            "Books": ["Fiction", "Non-fiction", "Education", "Comics"],
            "Sports": ["Gym", "Running", "Team Sports", "Outdoor"],
            "Toys": ["Board Games", "Action Figures", "Dolls", "Educational"],
            "Automotive": ["Car Accessories", "Motorbike Accessories", "Oils & Fluids"]
        }
        # Calculate default vols
        max_l1 = len(self.category_map)
        self.volume_l1 = volume_l1 if volume_l1 is not None else max_l1

        if volume_l2 is not None:
            self.volume_l2 = volume_l2
        else:
            selected_keys = list(self.category_map.keys())[:self.volume_l1]
            self.volume_l2 = sum(len(self.category_map[k]) for k in selected_keys)

        total_volume = self.volume_l1 + self.volume_l2
        super().__init__(total_volume, faker_instance)
        self.table_name = TBL_CATEGORY


    def generate(self) -> List[CategorySchema]:
        """Gen parent category"""
        records: List[CategorySchema] = []
        main_categories = list(self.category_map.keys())

        # Limit on volume requested
        limit = min(self.volume_l1, len(main_categories))
        selected_categories = main_categories[:limit]

        for main_name in selected_categories:
            created_at = self.faker.date_time_between(start_date='-5y', end_date='-2y')

            record: CategorySchema = {
                "category_name": main_name,
                "parent_category_id": None,
                "level": 1,
                "created_at": created_at
            }
            records.append(record)

        return records

    def generate_level_2(self, parent_ids: List[int]) -> List[CategorySchema]:
        """Gen sub category
        Args:
            parent_ids: List of category_id from DB where level=1.
            parent_names: List of category_name corresponding to IDs (to map subtypes).
        """
        records: List[CategorySchema] = []
        main_categories = list(self.category_map.keys())
        sorted_parent_ids = sorted(parent_ids)
        for i, parent_id in enumerate(sorted_parent_ids):
            # round-robin map parent id to name
            parent_name = main_categories[i % len(main_categories)]
            sub_categories = list(self.category_map.get(parent_name, []))

            for sub_name in sub_categories:
                # Stop if volume reach
                if self.volume_l2 and len(records) >= self.volume_l2:
                    return records

                # Assume created < parent created_at
                created_at = self.faker.date_time_between(start_date='-2y', end_date='now')

                record: CategorySchema = {
                    "category_name": sub_name,
                    "parent_category_id": parent_id,
                    "level": 2,
                    "created_at": created_at
                }
                records.append(record)

        return records


def generate_categories_full(gen: CategoryGenerator):
    # ==============================
    # Insert level 1 (main)
    # ==============================
    logger.info("[Category] Phase 1: Generating Level 1...")
    l1_records = gen.generate()
    bulk_insert(TBL_CATEGORY, l1_records)

    # ==============================
    # Insert level 2 (full)
    # ==============================
    logger.info("[Category] Phase 2: Generating Level 2...")
    # --- fetch inserted IDs ---
    parent_ids = get_existing_ids(TBL_CATEGORY, 'category_id', force_refresh=True)
    if not parent_ids:
        logger.warning("No parent IDs found. Skipping Level 2 generation.")
        return len(l1_records)

    # --- insert ---
    l2_records = gen.generate_level_2(parent_ids)
    bulk_insert(TBL_CATEGORY, l2_records)

    total = len(l1_records) + len(l2_records)
    return total

if __name__ == "__main__":
    gen = CategoryGenerator(volume_l1=3)
    generate_categories_full(gen)
