""" Reference Data Generation.
Tasks must run sequentially
"""

from mock_ecommerce.tasks.generate_data_into_database import generate_product, generate_promotion_product
from mock_ecommerce.utils.logger import logger

def get_tasks():
    """
    Return ordered list of tasks.
    Order matters: master_data → product → promotion_product
    """
    return [
        ('generate_product', generate_product),
        ('generate_promotion_product', generate_promotion_product),
    ]

def run():
    results = {}
    for task_name, task_func in get_tasks():
        logger.info(f"\n=========== Running task: {task_name}")
        result = task_func()
        results[task_name] = result
    
    return results

if __name__ == "__main__":
    results = run()
    print(f"\nGroup results: {results}")
