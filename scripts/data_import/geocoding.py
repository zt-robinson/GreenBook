import requests
import time
import os
import csv
from dotenv import load_dotenv

load_dotenv()

OPENCAGE_API_KEY = os.environ.get('OPENCAGE_API_KEY')
if not OPENCAGE_API_KEY:
    raise ValueError("Missing OpenCage API key. Set it in your .env file.")

def get_coordinates(city):
    url = f'https://api.opencagedata.com/geocode/v1/json?q={city}&key={OPENCAGE_API_KEY}&no_annotations=1&limit=1'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        geometry = data['results'][0]['geometry']
        return geometry['lat'], geometry['lng']
    return None, None

def get_elevation(lat, lon):
    url = f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}'
    response = requests.get(url)
    data = response.json()
    if data and 'results' in data:
        return data['results'][0]['elevation']
    return None

def main():
    input_file = os.path.join(os.path.dirname(__file__), "gbi_cities.txt")
    output_file = "gbi_city_geodata.csv"

    with open(input_file, "r", encoding="utf-8") as f:
        cities = [line.strip() for line in f if line.strip()]

    rows = []

    for city_line in cities:
        print(f"Processing: {city_line}")
        try:
            city, country = map(str.strip, city_line.split(","))
        except ValueError:
            print(f"Invalid line format: {city_line} — skipping")
            continue

        lat, lon = get_coordinates(city_line)
        if lat is not None and lon is not None:
            elevation_m = get_elevation(lat, lon)
            elevation_ft = round(elevation_m * 3.28084, 1) if elevation_m is not None else None
            rows.append([city, country, round(lat, 4), round(lon, 4), round(elevation_m, 1), elevation_ft])
        else:
            rows.append([city, country, None, None, None, None])

        time.sleep(1)  # API rate limit safety

    with open(output_file, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["city", "country", "lat", "lng", "elevation_m", "elevation_ft"])
        writer.writerows(rows)

    print(f"\n✅ Done. Output written to {output_file}")

if __name__ == "__main__":
    main()
