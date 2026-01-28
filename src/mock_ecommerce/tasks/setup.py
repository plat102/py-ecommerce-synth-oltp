from mock_ecommerce.database import create_all_tables, clean_database
from mock_ecommerce.utils.logger import logger

def task_setup_db(clean: bool = False):
    """
    - Create tables
    - Clean database (if clean=True)
    """
    logger.info('Setting up tables')
    create_all_tables()

    if clean:
        logger.info('Cleaning database')
        clean_database()
    logger.info('Setting up tables')

    logger.info("Setup Database completed.")

# task_setup_db(clean=True)