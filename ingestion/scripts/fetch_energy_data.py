import json
import logging
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

AREA = "NO1"
DAYS_BACK = 30

RAW_DIR = Path("ingestion/raw")
RAW_FILE = RAW_DIR / "historical_energy_prices.json"


def fetch_day_prices(target_date):
    api_url = (
        f"https://www.hvakosterstrommen.no/api/v1/prices/"
        f"{target_date.year}/{target_date.month:02d}-{target_date.day:02d}_{AREA}.json"
    )

    logging.info(f"Fetching data for {target_date}")

    response = requests.get(api_url, timeout=30)
    response.raise_for_status()

    return response.json()


def fetch_historical_prices():
    all_data = []

    for i in range(DAYS_BACK):
        target_date = date.today() - timedelta(days=i)

        try:
            daily_data = fetch_day_prices(target_date)

            for row in daily_data:
                row["delivery_date"] = str(target_date)

            all_data.extend(daily_data)

        except Exception as e:
            logging.warning(f"Failed to fetch data for {target_date}: {e}")

    return all_data


def save_raw_data(data):
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    with open(RAW_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    logging.info(f"Historical raw data saved to {RAW_FILE}")


def convert_to_dataframe(data):
    df = pd.DataFrame(data)

    print("\nHistorical Electricity Data Preview:")
    print(df.head())

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nAverage NOK Price:")
    print(df["NOK_per_kWh"].mean())

    return df


def validate_dataframe(df):
    if df.empty:
        raise ValueError("Dataset is empty.")

    required_columns = [
        "NOK_per_kWh",
        "EUR_per_kWh",
        "time_start",
        "time_end",
        "delivery_date"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    logging.info("Historical data validation passed successfully.")


def main():
    try:
        logging.info("Starting historical energy ingestion pipeline.")

        data = fetch_historical_prices()

        save_raw_data(data)

        df = convert_to_dataframe(data)

        validate_dataframe(df)

        logging.info("Historical ingestion pipeline completed successfully.")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")


if __name__ == "__main__":
    main()