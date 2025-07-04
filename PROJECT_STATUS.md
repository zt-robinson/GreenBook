# Golf Weather Data Project - Status Report

## Project Overview
Building a system to generate golf courses at various locations and simulate weather conditions during events. The goal is to collect monthly average weather data (temperature, wind speed, precipitation, humidity, cloud cover) for approximately 1000 cities.

## Current Status
**Last Updated**: Ready to test alternative weather APIs with smaller datasets

## Key Files & Structure
```
greenbook/
├── app.py                          # Main Flask application
├── core/                           # Core business logic
├── data/
│   ├── cities_with_coordinates.csv # 981 cities with lat/lng coordinates
│   ├── top_cities_per_state.csv    # Reduced dataset (1 per state)
│   ├── random_sample_50.csv        # Random sample of 50 cities
│   └── every_10th_city.csv         # Every 10th city (98 cities)
├── scripts/
│   ├── fetch_weather_data.py       # Main weather fetching script
│   ├── reduce_city_list.py         # Script to create smaller datasets
│   └── add_coordinates_to_locations.py # Original coordinate fetching
└── config/                         # Configuration files
```

## API Journey & Challenges

### 1. NOAA API (Initial Attempt)
- **Goal**: Fetch monthly weather data from NOAA's API
- **Challenges**: 
  - Rate limits (429 errors)
  - Data availability issues
  - Slow processing for 981 cities
- **Result**: Abandoned due to rate limiting

### 2. Open-Meteo API (Second Attempt)
- **Advantages**: Free, no API key required, generous rate limits
- **Challenge**: No monthly data endpoint - only daily data available
- **Solution**: Fetch daily data and aggregate to monthly averages
- **Implementation**: Created script with rate limiting and retry logic
- **Result**: Still too slow for 981 cities due to rate limits

### 3. Current Strategy: Alternative APIs
Ready to test these APIs with smaller datasets:
- **Visual Crossing Weather API**: Paid service with free trial, supports batch requests
- **NASA POWER API**: Free, designed for renewable energy but has weather data

## Data Preparation

### City Dataset
- **Source**: 981 cities with coordinates
- **Format**: CSV with columns: city, state, country, latitude, longitude
- **Location**: `data/cities_with_coordinates.csv`

### Reduced Datasets Created
For testing APIs with smaller datasets, we created:
1. **Top Cities per State** (`top_cities_per_state.csv`): 50 cities (1 per state)
2. **Random Sample** (`random_sample_50.csv`): 50 randomly selected cities
3. **Every 10th City** (`every_10th_city.csv`): 98 cities (every 10th city)

## Key Scripts

### 1. Weather Data Fetching (`scripts/fetch_weather_data.py`)
```python
# Features:
- Rate limiting with delays
- Retry logic for failed requests
- Incremental saving of results
- Support for multiple weather APIs
- Monthly aggregation from daily data
```

### 2. Dataset Reduction (`scripts/reduce_city_list.py`)
```python
# Features:
- Creates multiple smaller datasets for testing
- Preserves original data
- Generates top cities per state
- Creates random samples
- Creates every nth city samples
```

## Weather Data Requirements
**Monthly averages for each city:**
- Temperature (min, max, average)
- Wind speed
- Precipitation
- Humidity
- Cloud cover

**Time period**: Historical data (last 5-10 years preferred)

## Next Steps

### Immediate Actions
1. **Test Visual Crossing API** with smaller datasets
   - Sign up for free trial
   - Test with `top_cities_per_state.csv` (50 cities)
   - Check rate limits and data quality

2. **Test NASA POWER API** as backup
   - Free alternative
   - Test with same smaller datasets

### API Testing Strategy
1. Start with smallest dataset (top cities per state - 50 cities)
2. Verify data quality and format
3. Test rate limits and processing speed
4. Scale up to larger datasets if successful

## Technical Notes

### Rate Limiting Strategy
- Implemented exponential backoff
- Added delays between requests
- Retry logic for failed requests
- Incremental saving to avoid data loss

### Data Storage
- Results saved as CSV files
- Incremental updates supported
- Backup of original data maintained

### Error Handling
- Network timeout handling
- API error response handling
- Graceful degradation for partial failures

## Environment Setup
- **Python**: 3.11+
- **Key Dependencies**: 
  - requests (for API calls)
  - pandas (for data manipulation)
  - geopy (for coordinate handling)
  - flask (for web interface)

## Success Criteria
- [ ] Successfully fetch weather data for 50+ cities
- [ ] Data includes all required weather parameters
- [ ] Processing time under 30 minutes for 50 cities
- [ ] Data quality verified and validated
- [ ] Ready to scale to full 981 city dataset

## Lessons Learned
1. **Rate limits are the biggest challenge** - even "free" APIs have limits
2. **Smaller datasets for testing** - always test with reduced data first
3. **Incremental saving** - crucial for long-running processes
4. **Multiple API options** - always have backups ready
5. **Data validation** - verify data quality before scaling up

## Contact & Context
This project is for generating realistic weather conditions for golf course simulations. The weather data will be used to create dynamic payout calculations and event simulations based on historical weather patterns.

---
*This document should be updated as the project progresses. Last conversation focused on creating smaller test datasets and preparing to test alternative weather APIs.* 