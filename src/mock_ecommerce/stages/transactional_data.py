from mock_ecommerce.tasks.generate_data_into_database import (
    generate_order,
    generate_order_item,
    update_order_total
)
from mock_ecommerce.utils.logger import logger

def get_tasks():
    """
    Return ordered list of tasks.
    Order -> Order Item -> Order Total
    """
    return [
        ('generate_order', generate_order),
        ('generate_order_item', generate_order_item),
        ('update_order_total', update_order_total),
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
