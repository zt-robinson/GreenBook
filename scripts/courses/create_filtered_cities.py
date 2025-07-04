#!/usr/bin/env python3
"""
Create Filtered Cities List
Filters top20_cities_per_state.csv to only include cities with weather data
"""

import pandas as pd
import os

# Data paths
CITIES_DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/top20_cities_per_state.csv')
WEATHER_DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/visual_crossing_monthly_2024_complete.csv')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '../../data/cities_with_weather.csv')

def create_filtered_cities():
    """Create a filtered list of cities that have weather data"""
    
    print("🔍 Creating filtered cities list...")
    
    # Load data
    try:
        cities_df = pd.read_csv(CITIES_DATA_PATH)
        weather_df = pd.read_csv(WEATHER_DATA_PATH)
        print(f"✅ Loaded {len(cities_df)} cities from top20_cities_per_state.csv")
        print(f"✅ Loaded weather data for {len(weather_df)} records")
    except FileNotFoundError as e:
        print(f"❌ Data file not found: {e}")
        return None
    
    # Get unique cities from weather data
    weather_cities = weather_df[['city', 'state']].drop_duplicates()
    print(f"✅ Found {len(weather_cities)} unique cities with weather data")
    
    # Create a key for matching (city + state)
    weather_cities['city_state_key'] = weather_cities['city'] + '_' + weather_cities['state']
    cities_df['city_state_key'] = cities_df['city'] + '_' + cities_df['state_id']
    
    # Filter cities to only those with weather data
    filtered_cities = cities_df[cities_df['city_state_key'].isin(weather_cities['city_state_key'])]
    
    # Remove the temporary key column
    filtered_cities = filtered_cities.drop('city_state_key', axis=1)
    
    print(f"✅ Filtered to {len(filtered_cities)} cities with weather data")
    
    # Show distribution by state
    state_counts = filtered_cities.groupby('state_id').size().sort_values(ascending=False)
    print(f"\n📊 Cities per state (top 10):")
    print(state_counts.head(10))
    
    # Show states with no cities
    all_states = set(cities_df['state_id'].unique())
    filtered_states = set(filtered_cities['state_id'].unique())
    missing_states = all_states - filtered_states
    if missing_states:
        print(f"\n⚠️  States with no weather data: {sorted(missing_states)}")
    
    # Save filtered data
    filtered_cities.to_csv(OUTPUT_PATH, index=False)
    print(f"\n💾 Saved filtered cities to: {OUTPUT_PATH}")
    
    # Summary statistics
    print(f"\n📈 Summary:")
    print(f"Original cities: {len(cities_df)}")
    print(f"Filtered cities: {len(filtered_cities)}")
    print(f"Reduction: {len(cities_df) - len(filtered_cities)} cities removed")
    print(f"Coverage: {len(filtered_cities) / len(cities_df) * 100:.1f}%")
    
    return filtered_cities

def main():
    """Main function"""
    print("🏌️  City Filtering Script")
    print("=" * 50)
    
    filtered_cities = create_filtered_cities()
    
    if filtered_cities is not None:
        print(f"\n✅ Successfully created filtered cities list with {len(filtered_cities)} cities")
        return filtered_cities
    else:
        print("❌ Failed to create filtered cities list")
        return None

if __name__ == "__main__":
    main() 