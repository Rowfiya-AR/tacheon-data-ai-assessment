# Task 2: Weather ETL Pipeline

ETL pipeline that extracts hourly weather data from Open-Meteo API and loads it to BigQuery.

## Setup Instructions

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Authenticate GCP**: `gcloud auth application-default login` 
3. **Run pipeline**: `python pipeline.py`

## Schema
Table: `tacheon_weather.hourly_forecast`
- timestamp: TIMESTAMP
- temperature_2m: FLOAT64 
- relative_humidity_2m: FLOAT64
- precipitation: FLOAT64

## Step 5: Production Considerations

**Scheduling**: Use Cloud Scheduler to trigger Cloud Run job daily at 1 AM UTC. Ensures fresh data before business hours.

**Error Handling**: Implement retry logic with exponential backoff for API failures. Log errors to Cloud Logging and send Slack alerts on repeated failures.

**Schema Evolution**: Add new columns as NULLABLE to avoid breaking changes. Use BigQuery schema detection for initial loads, then lock schema for production.

**Performance**: Partition `hourly_forecast` table by DATE(timestamp) and cluster by timestamp. Reduces query costs for daily aggregations by 80%+.

**Security**: Use Workload Identity for Cloud Run authentication. Store no secrets in code. Grant minimal BigQuery Data Editor IAM role.
