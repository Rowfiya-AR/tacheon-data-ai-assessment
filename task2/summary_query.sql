-- Task 2: Daily weather summary for anomaly detection
-- Extracts max temp + hours above 35C per day to feed Task 1 alert logic

SELECT 
  DATE(timestamp) as forecast_date,
  city,
  MAX(temperature_c) as max_temp_c,
  MIN(temperature_c) as min_temp_c,
  ROUND(AVG(humidity), 1) as avg_humidity,
  SUM(CASE WHEN high_temp_flag = TRUE THEN 1 ELSE 0 END) as extreme_heat_hours,
  MAX(precipitation_mm) as max_rainfall_mm
FROM `dynamic-hybrid-405902.tacheon_weather.hourly_forecast`
WHERE DATE(timestamp) >= CURRENT_DATE()
GROUP BY forecast_date, city
ORDER BY forecast_date;
