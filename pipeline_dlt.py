import dlt
import requests
from datetime import datetime

@dlt.resource(name="weather_raw", write_disposition="append")
def get_weather_data():
    locations = [
        {"city": "Sao Paulo", "lat": -23.55, "lon": -46.63},
        {"city": "Rio de Janeiro", "lat": -22.90, "lon": -43.20},
        {"city": "Curitiba", "lat": -25.42, "lon": -49.27}
    ]
    
    for loc in locations:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data.get("current", {})
        
        yield {
            "timestamp_ingestion": datetime.utcnow().isoformat(),
            "city": loc["city"],
            "latitude": loc["lat"],
            "longitude": loc["lon"],
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "weather_code": current.get("weather_code")
        }

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="weather_streaming_pipeline",
        destination="duckdb",
        dataset_name="raw_staging"
    )
    pipeline.run(get_weather_data())
