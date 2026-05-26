import requests
import pandas as pd
import logging
from google.cloud import bigquery
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_weather_data():
    """Step 1+2: Fetch Open-Meteo data with error handling"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 28.6139,  # Delhi
        "longitude": 77.2090,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "forecast_days": 3
    }
    try:
        logging.info("Fetching weather data from Open-Meteo")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        logging.info("Successfully fetched weather data")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        raise

def transform_data(raw_data):
    """Step 3: Flatten JSON + add derived field for Task 2"""
    hourly = raw_data['hourly']
    df = pd.DataFrame({
        'timestamp': pd.to_datetime(hourly['time']),
        'temperature_c': hourly['temperature_2m'],
        'humidity': hourly['relative_humidity_2m'],
        'precipitation_mm': hourly['precipitation'],
        'city': 'Delhi',
        'ingested_at': datetime.utcnow()
    })
    # Derived field: flag hours above 35C for anomaly logic
    df['high_temp_flag'] = df['temperature_c'] > 35
    logging.info(f"Transformed {len(df)} rows. High temp hours: {df['high_temp_flag'].sum()}")
    return df

def load_to_bigquery(df):
    """Step 4: Load to BigQuery Sandbox"""
    client = bigquery.Client()  # Uses ADC
    table_id = f"{client.project}.tacheon_weather.hourly_forecast"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
    )
    logging.info(f"Loading data to {table_id}")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    logging.info(f"Loaded {job.output_rows} rows to {table_id}")

if __name__ == "__main__":
    try:
        raw = fetch_weather_data()
        df = transform_data(raw)
        print("Sample data:")
        print(df.head())
        load_to_bigquery(df)
        logging.info("Pipeline completed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
