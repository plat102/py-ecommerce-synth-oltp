import argparse
from mock_ecommerce.pipelines.generate_ecom_data import run_pipeline

def main():
    parser = argparse.ArgumentParser(description="E-commerce Synthetic Data Generator")

    parser.add_argument(
        "--clean",
        action="store_true",
        help="Wipe database (TRUNCATE CASCADE) before generating."
    )
    parser.add_argument(
        "--stage",
        type=str,
        default="all",
        choices=["all", "master", "reference", "clean"],
        help="Select stage to run. Default: all"
    )
    args = parser.parse_args()

    # run
    run_pipeline(clean_db=args.clean, target_stage=args.stage)

if __name__ == "__main__":
    main()
