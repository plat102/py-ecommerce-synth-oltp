from mock_ecommerce.stages import (
    setup,
    master_data,
    reference_data
)
from mock_ecommerce.utils.logger import logger

def run_pipeline(
    clean_db: bool = False,
    target_stage: str = "all"
):
    logger.info(f"STARTING PIPELINE | Stage: {target_stage} | Clean: {clean_db}")
    try:
        if target_stage == "clean":
            logger.info("clean only requested. Exiting.")
            setup.task_setup_db(clean=True)
            return

        else:
            if clean_db:
                setup.task_setup_db(clean=True)
            if target_stage in ["all", "master"]:
                master_data.run()
            if target_stage in ["all", "reference"]:
                reference_data.run()

    except Exception as e:
        logger.critical(f"🔥 Pipeline Crashed: {e}")
        raise e
