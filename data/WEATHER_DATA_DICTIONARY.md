# Weather Data Dictionary

This document explains the meaning of each weather metric in `cities_with_regions.csv`, including how to interpret the min/avg/max values for each month, and how you might use them in simulation or gameplay.

---

## 1. Temperature
- **Columns:** `temp_min_X`, `temp_avg_X`, `temp_max_X` (where X is a month abbreviation, e.g., `jan`, `feb`, ...)
- **Unit:** Degrees Fahrenheit (°F)
- **Description:**
  - `temp_min_X`: Typical lowest daily high temperature for that region in that month (not the coldest night, but the lower bound of expected daytime highs).
  - `temp_avg_X`: Typical average daily high temperature for that region in that month.
  - `temp_max_X`: Typical highest daily high temperature for that region in that month (not an all-time record, but the upper bound of expected daytime highs).
- **Usage:**
  - Use `temp_avg_X` for normal conditions.
  - Use `temp_min_X`/`temp_max_X` for simulating cold/hot spells.

---

## 2. Rain Probability
- **Columns:** `rain_prop_X` (where X is a month abbreviation)
- **Unit:** Probability (0.0 to 1.0)
- **Description:**
  - Represents the average daily probability of measurable precipitation (rain or snow) in that region for that month.
- **Usage:**
  - Use as the chance of rain on any given day (e.g., 0.25 = 25% chance of rain on a day in January).

---

## 3. Wind Speed
- **Columns:** `wind_speed_min_X`, `wind_speed_avg_X`, `wind_speed_max_X`
- **Unit:** Miles per hour (mph)
- **Description:**
  - `wind_speed_min_X`: Typical lower bound of average daily wind speed for that region/month.
  - `wind_speed_avg_X`: Typical average daily wind speed for that region/month.
  - `wind_speed_max_X`: Typical upper bound of average daily wind speed for that region/month.
- **Usage:**
  - Use `wind_speed_avg_X` for normal wind.
  - Use `wind_speed_min_X`/`wind_speed_max_X` for calm/windy days.

---

## 4. Humidity
- **Columns:** `humidity_min_X`, `humidiy_avg_X`, `humidity_max_X`
- **Unit:** Percent (%)
- **Description:**
  - `humidity_min_X`: Typical lower bound of average daily relative humidity for that region/month.
  - `humidiy_avg_X`: Typical average daily relative humidity for that region/month.
  - `humidity_max_X`: Typical upper bound of average daily relative humidity for that region/month.
- **Usage:**
  - Use `humidiy_avg_X` for normal humidity.
  - Use `humidity_min_X`/`humidity_max_X` for dry/humid spells.

---

## 5. Cloud Cover
- **Columns:** `cloud_cover_min_X`, `cloud_cover_avg_X`, `cloud_cover_max_X`
- **Unit:** Fraction (0.0 = clear, 1.0 = fully overcast)
- **Description:**
  - `cloud_cover_min_X`: Typical lower bound of average daily cloud cover for that region/month.
  - `cloud_cover_avg_X`: Typical average daily cloud cover for that region/month.
  - `cloud_cover_max_X`: Typical upper bound of average daily cloud cover for that region/month.
- **Usage:**
  - Use `cloud_cover_avg_X` for normal conditions.
  - Use `cloud_cover_min_X`/`cloud_cover_max_X` for clear/overcast days.

---

## How These Values Were Generated
- **Base values** come from state-level monthly averages (NOAA and other sources).
- **Regional modifiers** (North/South/East/West/Central) adjust these values to reflect typical differences within a state.
- **Seasonal factors** adjust for the time of year.
- **min/avg/max** are not extremes, but represent a plausible range for typical daily conditions in that region and month.

---

## Example (from your data)

| City    | Month | temp_min_jan | temp_avg_jan | temp_max_jan | rain_prop_jan | wind_speed_avg_jan | humidity_avg_jan | cloud_cover_avg_jan |
|---------|-------|--------------|--------------|--------------|---------------|--------------------|------------------|---------------------|
| Auburn  | Jan   | 37.8         | 47.8         | 57.8         | 0.252         | 7.7                | 79.2             | 0.605               |

- **Auburn, AL, January:**
  - Typical daily high temps: 37.8°F (cold snap) to 57.8°F (warm spell), average 47.8°F.
  - 25.2% chance of rain on any given day.
  - Average wind: 7.7 mph.
  - Average humidity: 79.2%.
  - Average cloud cover: 0.605 (about 60% of the sky covered).

---

## How to Use for Gameplay Modifiers
- **Normalize:** Map these values to a 0-1 scale or any modifier system you want.
- **Randomize:** For a given day, pick a value between min and max, or use avg for "normal" days.
- **Events:** Use rain probability to trigger rain events, wind for movement penalties, etc. 