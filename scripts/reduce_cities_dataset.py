import pandas as pd
import random

# Read the full dataset
df = pd.read_csv('data/location_data_with_coords.csv')

print(f"Original dataset: {len(df)} cities")

# Option 1: Top cities by state (keep top 2-3 per state)
def get_top_cities_by_state(df, top_n=2):
    """Get top N cities from each state."""
    top_cities = []
    
    for state in df['state'].unique():
        state_cities = df[df['state'] == state].copy()
        if len(state_cities) <= top_n:
            top_cities.append(state_cities)
        else:
            # Sort by city name for consistency, take top N
            state_cities = state_cities.sort_values('city').head(top_n)
            top_cities.append(state_cities)
    
    return pd.concat(top_cities, ignore_index=True)

# Option 2: Random sample
def get_random_sample(df, n=200):
    """Get a random sample of N cities."""
    return df.sample(n=n, random_state=42)

# Option 3: Every Nth city
def get_every_nth_city(df, n=5):
    """Get every Nth city from the dataset."""
    return df.iloc[::n].copy()

# Create different reduced datasets
print("\nCreating reduced datasets...")

# Top 2 cities per state
top_cities = get_top_cities_by_state(df, top_n=2)
top_cities.to_csv('data/location_data_top_cities.csv', index=False)
print(f"Top cities by state: {len(top_cities)} cities")

# Random sample of 200 cities
random_sample = get_random_sample(df, n=200)
random_sample.to_csv('data/location_data_random_200.csv', index=False)
print(f"Random sample: {len(random_sample)} cities")

# Every 5th city
every_5th = get_every_nth_city(df, n=5)
every_5th.to_csv('data/location_data_every_5th.csv', index=False)
print(f"Every 5th city: {len(every_5th)} cities")

# Every 10th city
every_10th = get_every_nth_city(df, n=10)
every_10th.to_csv('data/location_data_every_10th.csv', index=False)
print(f"Every 10th city: {len(every_10th)} cities")

print("\nReduced datasets created:")
print("- data/location_data_top_cities.csv (recommended for testing)")
print("- data/location_data_random_200.csv")
print("- data/location_data_every_5th.csv")
print("- data/location_data_every_10th.csv") 