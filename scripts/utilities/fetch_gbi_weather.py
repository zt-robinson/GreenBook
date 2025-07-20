import csv
import requests
import time
import calendar
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv
import os
import pandas as pd
from tqdm import tqdm
import logging

# Setup
load_dotenv()
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
INPUT_FILE = "data/asia_cities_with_elevation.csv"
OUTPUT_FILE = "data/visual_crossing_asia_2024.csv"
YEAR = 2024
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
LOG_FILE = "logs/fetch_gbi_weather.log"
os.makedirs("logs", exist_ok=True)

# Logging config
logging.basicConfig(filename=LOG_FILE,
                    level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

def fetch_daily_weather(lat, lon):
    url = f"{BASE_URL}/{lat},{lon}/{YEAR}-01-01/{YEAR}-12-31"
    params = {
        "unitGroup": "us",
        "key": API_KEY,
        "include": "days",
        "contentType": "json"
    }

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params)
            if response.status_code == 429:
                logging.warning("Rate limited. Sleeping 60s...")
                time.sleep(60)
                continue
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"API error (attempt {attempt+1}): {e}")
            time.sleep(5 * (attempt + 1))
    logging.error("Failed after 3 retries.")
    return None

def process_city(city_data):
    city = city_data['city']
    country = city_data['country']
    lat = city_data['lat']
    lon = city_data['lng']

    logging.info(f"Fetching data for {city}, {country}")
    weather = fetch_daily_weather(lat, lon)
    if not weather or "days" not in weather:
        logging.warning(f"No data for {city}")
        return []

    monthly_data = defaultdict(list)

    for day in weather["days"]:
        date = datetime.strptime(day["datetime"], "%Y-%m-%d")
        m = date.month
        monthly_data[m].append({
            "temp": day.get("temp", 0),
            "wind": day.get("windspeed", 0),
            "precip": day.get("precip", 0),
            "humidity": day.get("humidity", 0),
            "cloudcover": day.get("cloudcover", 0)
        })

    result_rows = []
    for month in range(1, 13):
        data = monthly_data.get(month, [])
        if not data:
            continue

        avg_temp = sum(d["temp"] for d in data) / len(data)
        avg_wind = sum(d["wind"] for d in data) / len(data)
        total_precip = sum(d["precip"] for d in data)
        avg_humidity = sum(d["humidity"] for d in data) / len(data)
        avg_cloud = sum(d["cloudcover"] for d in data) / len(data)

        result_rows.append({
            "city": city,
            "country": country,
            "month": calendar.month_name[month],
            "month_num": month,
            "temperature_2m_mean": round(avg_temp, 2),
            "windspeed_10m_mean": round(avg_wind, 2),
            "precipitation_sum": round(total_precip, 2),
            "relative_humidity_2m_mean": round(avg_humidity, 2),
            "cloudcover_mean": round(avg_cloud, 2)
        })

    return result_rows

def main():
    cities = pd.read_csv(INPUT_FILE)
    all_data = []
    call_count = 0
    max_calls = 950  # safety buffer under 1000

    for _, row in tqdm(cities.iterrows(), total=len(cities), desc="Processing Cities"):
        if call_count >= max_calls:
            logging.warning("API call limit reached — halting early.")
            break

        city_data = {
            "city": row["city"],
            "country": row["country"],
            "lat": row["lat"],
            "lng": row["lng"]
        }

        result = process_city(city_data)
        if result:
            all_data.extend(result)
            call_count += 1
            time.sleep(1.2)  # politeness delay
        else:
            logging.warning(f"Skipping {city_data['city']} due to no data.")

    if all_data:
        logging.info(f"Writing {len(all_data)} rows to {OUTPUT_FILE}")
        keys = all_data[0].keys()
        with open(OUTPUT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(all_data)
    else:
        logging.error("No data collected — nothing written.")

if __name__ == "__main__":
    main()
