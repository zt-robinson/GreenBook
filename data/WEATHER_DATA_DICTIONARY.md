# Visual Crossing Weather Data Dictionary

This document explains the weather data collected from Visual Crossing Weather API for US cities in 2024, including the raw data structure, processing calculations, and how to interpret the values for simulation or gameplay.

---

## Data Source and Collection

**Source:** Visual Crossing Weather API  
**Time Period:** January 1, 2024 - December 31, 2024  
**Coverage:** Top cities by population for each US state (excluding Alaska)  
**Data Format:** Daily weather observations aggregated to monthly averages/sums  
**Total Records:** 7,320 monthly observations (610 cities × 12 months)

---

## Dataset Structure

The file `visual_crossing_monthly_2024_complete.csv` contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `city` | string | City name |
| `state` | string | State abbreviation (2-letter code) |
| `month` | string | Month name (January, February, etc.) |
| `month_num` | integer | Month number (1-12) |
| `temperature_2m_mean` | float | Average daily temperature (°F) |
| `windspeed_10m_mean` | float | Average daily wind speed (mph) |
| `precipitation_sum` | float | Total monthly precipitation (inches) |
| `relative_humidity_2m_mean` | float | Average daily relative humidity (%) |
| `cloudcover_mean` | float | Average daily cloud cover (%) |

---

## Raw Data Processing

### 1. Data Collection
- **API Endpoint:** `https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline`
- **Parameters:**
  - `unitGroup`: 'us' (Fahrenheit, mph, inches)
  - `include`: 'days' (daily observations)
  - `contentType`: 'json'
- **Time Range:** Full year 2024 for each city
- **Coordinates:** Used city latitude/longitude from `top20_cities_per_state.csv`

### 2. Daily to Monthly Aggregation

For each city and month, the following calculations were performed:

#### Temperature (`temperature_2m_mean`)
- **Raw Data:** Daily high temperature (°F)
- **Calculation:** `sum(daily_temps) / number_of_days_in_month`
- **Unit:** Degrees Fahrenheit (°F)
- **Example:** January in Alabaster, AL: 42.89°F average

#### Wind Speed (`windspeed_10m_mean`)
- **Raw Data:** Daily average wind speed (mph)
- **Calculation:** `sum(daily_wind_speeds) / number_of_days_in_month`
- **Unit:** Miles per hour (mph)
- **Example:** January in Alabaster, AL: 11.00 mph average

#### Precipitation (`precipitation_sum`)
- **Raw Data:** Daily precipitation (inches)
- **Calculation:** `sum(daily_precipitation)` (not averaged)
- **Unit:** Inches
- **Example:** January in Alabaster, AL: 7.60 inches total

#### Humidity (`relative_humidity_2m_mean`)
- **Raw Data:** Daily relative humidity (%)
- **Calculation:** `sum(daily_humidity) / number_of_days_in_month`
- **Unit:** Percentage (%)
- **Example:** January in Alabaster, AL: 72.73% average

#### Cloud Cover (`cloudcover_mean`)
- **Raw Data:** Daily cloud cover (%)
- **Calculation:** `sum(daily_cloud_cover) / number_of_days_in_month`
- **Unit:** Percentage (%)
- **Example:** January in Alabaster, AL: 43.37% average

---

## Data Quality and Validation

### Missing Data Handling
- Cities with invalid coordinates were skipped
- API failures were retried up to 3 times with exponential backoff
- Rate limiting (429 errors) triggered 60-second waits
- Failed cities were logged but processing continued

### Data Validation
- Temperature range: -50°F to 130°F (reasonable continental US range)
- Wind speed range: 0-100 mph (reasonable range)
- Humidity range: 0-100% (percentage constraint)
- Cloud cover range: 0-100% (percentage constraint)
- Precipitation: Non-negative values

---

## Example Data Row

```csv
city,state,month,month_num,temperature_2m_mean,windspeed_10m_mean,precipitation_sum,relative_humidity_2m_mean,cloudcover_mean
Alabaster,AL,January,1,42.89354838709677,11.003225806451612,7.595999999999999,72.72903225806452,43.37419354838709
```

**Interpretation:**
- **Alabaster, Alabama, January 2024:**
  - Average daily temperature: 42.89°F
  - Average daily wind speed: 11.00 mph
  - Total monthly precipitation: 7.60 inches
  - Average daily humidity: 72.73%
  - Average daily cloud cover: 43.37%

---

## Usage for Gameplay and Simulation

### Direct Usage
- Use monthly averages for seasonal weather patterns
- Compare cities for climate differences
- Identify weather extremes (hot/cold, wet/dry, windy/calm)

### Normalization for Game Factors
The data can be normalized to 0-1 scales for gameplay modifiers:

#### Temperature Factor
```python
# Normalize: 32°F = 0.0, 100°F = 1.0
temp_factor = (avg_temp - 32) / 68.0
temp_factor = max(0.0, min(1.0, temp_factor))
```

#### Wind Factor
```python
# Normalize: 0 mph = 0.0, 30+ mph = 1.0
wind_factor = avg_wind / 30.0
wind_factor = max(0.0, min(1.0, wind_factor))
```

#### Humidity Factor
```python
# Direct percentage to 0-1 scale
humidity_factor = avg_humidity / 100.0
```

#### Rain Factor
```python
# Convert monthly inches to probability (approximate)
# 1 inch/month ≈ 3% daily rain probability
rain_factor = (monthly_precip / 30) / 100.0
rain_factor = max(0.0, min(1.0, rain_factor))
```

#### Cloud Factor
```python
# Direct percentage to 0-1 scale
cloud_factor = avg_cloud_cover / 100.0
```

---

## Geographic Coverage

### State Coverage
- **Tier 1 (Top 5 states):** 20 cities each (CA, TX, FL, NY, PA)
- **Tier 2 (States 6-10):** 15 cities each (IL, OH, GA, NC, MI)
- **Tier 3 (States 11-40):** 10 cities each (30 states)
- **Tier 4 (States 41-50):** 8 cities each (10 smallest states)

### Total Coverage
- **610 cities** across 49 states + DC
- **7,320 monthly observations** (610 × 12 months)
- **Complete 2024 data** for all target cities

---

## Data Limitations

1. **Historical vs Forecast:** Data represents actual 2024 weather, not forecasts
2. **Single Year:** Only one year of data (2024) - not long-term averages
3. **Daily Aggregation:** Monthly values are averages of daily observations
4. **API Dependencies:** Data quality depends on Visual Crossing API accuracy
5. **Urban Bias:** Data represents city center conditions, not rural areas

---

## File Information

- **Filename:** `visual_crossing_monthly_2024_complete.csv`
- **Size:** ~720KB
- **Rows:** 7,320
- **Columns:** 9
- **Last Updated:** January 2025
- **Data Source:** Visual Crossing Weather API
- **Processing Scripts:** Custom Python scripts (now archived)

---

## Attribution

[![Weather Data Provided by Visual Crossing](visual_crossing_logo_small.png)](https://www.visualcrossing.com/)

This dataset contains historical weather data for 610 US cities throughout 2024, collected via the Visual Crossing Weather API. The data includes monthly averages for temperature, wind speed, precipitation, humidity, and cloud cover, aggregated from daily observations. 