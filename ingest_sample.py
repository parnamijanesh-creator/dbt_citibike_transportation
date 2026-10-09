import argparse
import os
from download_data import download_and_extract
from load_snowflake import load_to_snowflake

DEFAULT_DATA_DIR = os.path.abspath("./data")


def main() -> None:
    parser = argparse.ArgumentParser(description="Citi Bike Data Pipeline: Download and Load into Snowflake")
    parser.add_argument(
        "--month",
        type=str,
        default="202402",
        help="Target year and month format YYYYMM (e.g., 202402)",
    )
    parser.add_argument(
        "--download-only",
        action="store_true",
        help="Only download and extract data, do not load into Snowflake",
    )
    parser.add_argument(
        "--load-only",
        action="store_true",
        help="Only load existing CSV files into Snowflake without downloading",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Re-download data even if CSV files already exist locally",
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Delete local CSV files after successful Snowflake ingestion (default: keep them)",
    )
    args = parser.parse_args()

    # Step 1: Download & Extract (skipped if --load-only or if CSVs already exist and not --force-download)
    if not args.load_only:
        download_and_extract(month=args.month, data_dir=DEFAULT_DATA_DIR, force=args.force_download)

    # Step 2: Upload & COPY INTO Snowflake (skipped if --download-only)
    if not args.download_only:
        load_to_snowflake(data_dir=DEFAULT_DATA_DIR, cleanup=args.cleanup)


if __name__ == "__main__":
    main()