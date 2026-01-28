"""
Task Group: Master Data Generation.
Tasks in this group can run in parallel.
"""
from mock_ecommerce.tasks.generate_data_into_database import (
    generate_brand, generate_seller, generate_promotion,
    generate_category
)
from mock_ecommerce.utils.logger import logger

def get_tasks():
    """Return list of tasks in this group.
    """
    return [
        ('generate_brand', generate_brand),
        ('generate_seller', generate_seller),
        ('generate_promotion', generate_promotion),
        ('generate_category', generate_category)
    ]

def run():
    results = {}

    for task_name, task_func in get_tasks():
        logger.info(f"\nRunning task: {task_name}")
        result = task_func()
        results[task_name] = result
    logger.info(f"\n=========== Results: {results}")

    return results

if __name__ == "__main__":
    results = run()
    print(f"\nGroup results: {results}")
