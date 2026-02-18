from mock_ecommerce.stages import (
    setup,
    master_data,
    reference_data,
    transactional_data
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
            setup.run_stage_setup(clean=True)
            return

        # Always setup tables, clean if requested
        should_clean = clean_db and target_stage in ["all", "master"]
        setup.run_stage_setup(clean=should_clean)

        if target_stage in ["all", "master"]:
            master_data.run()
        if target_stage in ["all", "reference"]:
            reference_data.run()
        if target_stage in ["all", "transactional"]:
            transactional_data.run()

    except Exception as e:
        logger.critical(f"Pipeline Crashed: {e}")
        raise e