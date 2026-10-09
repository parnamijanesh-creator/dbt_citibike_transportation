import io
import os
import re
import shutil
import zipfile
import requests
from tqdm import tqdm

DEFAULT_MONTH = "202402"
BASE_URL_TEMPLATE = "https://s3.amazonaws.com/tripdata/{month}-citibike-tripdata.zip"
DEFAULT_URL = BASE_URL_TEMPLATE.format(month=DEFAULT_MONTH)
DEFAULT_DATA_DIR = os.path.abspath("./data")


def get_citibike_url(month: str) -> str:
    """Returns the Citi Bike S3 zip URL for a given month in YYYYMM format."""
    cleaned_month = month.replace("-", "").strip()
    return BASE_URL_TEMPLATE.format(month=cleaned_month)


def download_and_extract(
    month: str = DEFAULT_MONTH,
    data_dir: str = DEFAULT_DATA_DIR,
    force: bool = False,
    url: str | None = None,
) -> list[str]:
    """Downloads citibike zip file and extracts CSV partitions.

    Accepts a dynamic month string in YYYYMM format (e.g. '202402', '202403').
    If CSV files for the month already exist in data_dir and force=False, skips download.
    """
    os.makedirs(data_dir, exist_ok=True)

    # Resolve URL and month identifier
    if month.startswith("http://") or month.startswith("https://"):
        url = month
        m = re.search(r"(\d{6})-citibike", month)
        month_str = m.group(1) if m else ""
    else:
        month_str = month.replace("-", "").strip()
        if url is None:
            url = get_citibike_url(month_str)

    # 1. Cache check: check if CSVs for the specified month are already extracted
    existing_csvs = [
        os.path.join(data_dir, f)
        for f in os.listdir(data_dir)
        if f.endswith(".csv")
        and not f.startswith("__MACOSX")
        and (not month_str or month_str in f)
    ]
    if existing_csvs and not force:
        month_label = f" for month {month_str}" if month_str else ""
        print(f"Cache hit: Found {len(existing_csvs)} CSV file(s){month_label} in {data_dir}. Skipping download.")
        return existing_csvs

    zip_filename = f"temp_tripdata_{month_str}.zip" if month_str else "temp_tripdata.zip"
    temp_zip = os.path.join(data_dir, zip_filename)

    # 2. Stream download with progress bar
    print(f"Downloading {url}...")
    try:
        with requests.get(url, stream=True) as resp:
            if resp.status_code == 404:
                raise FileNotFoundError(
                    f"Dataset not found at {url}. "
                    f"Please verify that month '{month}' (YYYYMM format) is valid and available on Citi Bike S3."
                )
            resp.raise_for_status()
            total_size = int(resp.headers.get("content-length", 0))
            with open(temp_zip, "wb") as f, tqdm(
                desc=f"Downloading {month_str or 'tripdata'}",
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in resp.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
    except Exception:
        if os.path.exists(temp_zip):
            os.remove(temp_zip)
        raise

    # 3. Extract all CSVs directly into data_dir
    extracted_files = []
    with zipfile.ZipFile(temp_zip) as z:
        all_members = [
            f for f in z.namelist() if not f.startswith("__MACOSX") and not os.path.basename(f).startswith(".")
        ]
        csv_files = [f for f in all_members if f.endswith(".csv")]
        nested_zip_files = [f for f in all_members if f.endswith(".zip")]

        if not csv_files and not nested_zip_files:
            raise FileNotFoundError("No CSV or nested ZIP files found in the downloaded archive.")

        # Extract direct CSVs
        if csv_files:
            print(f"Extracting {len(csv_files)} CSV file(s) to {data_dir}...")
            for file in csv_files:
                target_filename = os.path.basename(file)
                target_path = os.path.join(data_dir, target_filename)
                print(f"  Extracting {target_filename}...")
                with z.open(file) as zf, open(target_path, "wb") as out_f:
                    shutil.copyfileobj(zf, out_f)
                extracted_files.append(target_path)

        # Extract CSVs from any nested ZIPs
        if nested_zip_files:
            print(f"Extracting from {len(nested_zip_files)} nested ZIP file(s)...")
            for n_zip in nested_zip_files:
                nested_data = z.read(n_zip)
                with zipfile.ZipFile(io.BytesIO(nested_data)) as nz:
                    nested_csvs = [
                        f for f in nz.namelist() if f.endswith(".csv") and not f.startswith("__MACOSX")
                    ]
                    for file in nested_csvs:
                        target_filename = os.path.basename(file)
                        target_path = os.path.join(data_dir, target_filename)
                        print(f"  Extracting {target_filename}...")
                        with nz.open(file) as nzf, open(target_path, "wb") as out_f:
                            shutil.copyfileobj(nzf, out_f)
                        extracted_files.append(target_path)

    # 4. Remove zip archive to reclaim disk space, keeping CSVs
    if os.path.exists(temp_zip):
        os.remove(temp_zip)

    print("Download and extraction complete!")
    return extracted_files


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download and extract Citi Bike trip data")
    parser.add_argument(
        "--month",
        type=str,
        default=DEFAULT_MONTH,
        help="Target year and month format YYYYMM (e.g., 202402)",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=DEFAULT_DATA_DIR,
        help="Directory to store extracted data",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force re-download even if CSV files already exist",
    )
    args = parser.parse_args()
    download_and_extract(month=args.month, data_dir=args.data_dir, force=args.force)
