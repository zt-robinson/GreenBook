import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# Load your CSV
df = pd.read_csv('data/location_data.csv')

# Set up geocoder
geolocator = Nominatim(user_agent="greenbook-geocoder")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Prepare columns
df['latitude'] = None
df['longitude'] = None

for idx, row in df.iterrows():
    location_str = f"{row['city']}, {row['state']}, USA"
    try:
        location = geocode(location_str)
        if location:
            df.at[idx, 'latitude'] = location.latitude
            df.at[idx, 'longitude'] = location.longitude
            print(f"Found: {location_str} -> ({location.latitude}, {location.longitude})")
        else:
            print(f"Not found: {location_str}")
    except Exception as e:
        print(f"Error for {location_str}: {e}")
    time.sleep(1)  # Extra delay to avoid being blocked

# Save to new CSV
df.to_csv('data/location_data_with_coords.csv', index=False)
print("Done! Saved to data/location_data_with_coords.csv")