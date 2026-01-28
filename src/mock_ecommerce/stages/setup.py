from mock_ecommerce.tasks.setup import task_setup_db
from mock_ecommerce.utils.logger import logger

def run_stage_setup(clean: bool = False):
    logger.info("==========================================")
    logger.info("STAGE: SETUP")

    task_setup_db(clean=clean)
