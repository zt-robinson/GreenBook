#!/usr/bin/env python3
"""
Populate course_characteristics for each course in golf_courses.db
- Environmental variables: from climate group
- Static variables: randomized
- course_length: left NULL
"""
import sqlite3
import os
import random
import re

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

# Climate group table (as previously defined)
CLIMATE_GROUPS = {
    'Southwest Desert':     {'avg_temp': 90, 'rain_prob': 0.05, 'wind': 0.2,  'humidity': 0.2,  'elevation': 0.3},
    'Pacific Northwest':    {'avg_temp': 60, 'rain_prob': 0.6,  'wind': 0.4,  'humidity': 0.7,  'elevation': 0.2},
    'California Coast':     {'avg_temp': 68, 'rain_prob': 0.15, 'wind': 0.25, 'humidity': 0.5,  'elevation': 0.1},
    'Mountain West':        {'avg_temp': 70, 'rain_prob': 0.15, 'wind': 0.3,  'humidity': 0.3,  'elevation': 0.7},
    'Great Plains':         {'avg_temp': 72, 'rain_prob': 0.2,  'wind': 0.5,  'humidity': 0.4,  'elevation': 0.4},
    'Midwest':              {'avg_temp': 68, 'rain_prob': 0.25, 'wind': 0.35, 'humidity': 0.55, 'elevation': 0.3},
    'Northeast':            {'avg_temp': 65, 'rain_prob': 0.3,  'wind': 0.3,  'humidity': 0.6,  'elevation': 0.2},
    'Southeast':            {'avg_temp': 80, 'rain_prob': 0.4,  'wind': 0.25, 'humidity': 0.75, 'elevation': 0.1},
    'Texas':                {'avg_temp': 85, 'rain_prob': 0.2,  'wind': 0.3,  'humidity': 0.5,  'elevation': 0.2},
    'Alaska':               {'avg_temp': 55, 'rain_prob': 0.2,  'wind': 0.3,  'humidity': 0.5,  'elevation': 0.3},
    'Hawaii':               {'avg_temp': 82, 'rain_prob': 0.3,  'wind': 0.2,  'humidity': 0.8,  'elevation': 0.0},
    'Canada':               {'avg_temp': 60, 'rain_prob': 0.25, 'wind': 0.3,  'humidity': 0.6,  'elevation': 0.2},
    'British Isles':        {'avg_temp': 62, 'rain_prob': 0.4,  'wind': 0.35, 'humidity': 0.7,  'elevation': 0.1},
    'Japan':                {'avg_temp': 70, 'rain_prob': 0.3,  'wind': 0.25, 'humidity': 0.7,  'elevation': 0.1},
    'Australia':            {'avg_temp': 78, 'rain_prob': 0.15, 'wind': 0.3,  'humidity': 0.4,  'elevation': 0.2},
}

# Helper to match location string to climate group
STATE_TO_GROUP = {
    # US
    'AZ': 'Southwest Desert', 'NM': 'Southwest Desert', 'NV': 'Southwest Desert',
    'WA': 'Pacific Northwest', 'OR': 'Pacific Northwest',
    'CA': 'California Coast',
    'CO': 'Mountain West', 'UT': 'Mountain West', 'ID': 'Mountain West', 'MT': 'Mountain West', 'WY': 'Mountain West',
    'KS': 'Great Plains', 'NE': 'Great Plains', 'OK': 'Great Plains', 'SD': 'Great Plains', 'ND': 'Great Plains',
    'IL': 'Midwest', 'IN': 'Midwest', 'IA': 'Midwest', 'MI': 'Midwest', 'MN': 'Midwest', 'MO': 'Midwest', 'OH': 'Midwest', 'WI': 'Midwest',
    'NY': 'Northeast', 'NJ': 'Northeast', 'MA': 'Northeast', 'PA': 'Northeast', 'CT': 'Northeast', 'RI': 'Northeast', 'VT': 'Northeast', 'NH': 'Northeast', 'ME': 'Northeast',
    'FL': 'Southeast', 'GA': 'Southeast', 'AL': 'Southeast', 'MS': 'Southeast', 'LA': 'Southeast', 'SC': 'Southeast', 'NC': 'Southeast', 'TN': 'Southeast', 'AR': 'Southeast',
    'TX': 'Texas',
    'AK': 'Alaska',
    'HI': 'Hawaii',
    # Canada
    'BC': 'Canada', 'ON': 'Canada', 'QC': 'Canada', 'AB': 'Canada', 'MB': 'Canada', 'NS': 'Canada', 'NB': 'Canada', 'NL': 'Canada', 'PE': 'Canada', 'SK': 'Canada', 'NT': 'Canada', 'YT': 'Canada', 'NU': 'Canada',
    # UK/Ireland
    'Scotland': 'British Isles', 'England': 'British Isles', 'Ireland': 'British Isles',
    # Japan
    'Japan': 'Japan',
    # Australia
    'AUS': 'Australia',
}

# Helper to extract state/country from location string
STATE_ABBR_RE = re.compile(r', ([A-Z]{2,3}) \(')
COUNTRY_RE = re.compile(r', ([A-Za-z ]+)\)?$')

# Random static variable generator
rand = lambda a, b: round(random.uniform(a, b), 2)

def get_climate_group(location):
    # Try to extract state abbreviation
    m = STATE_ABBR_RE.search(location)
    if m:
        state = m.group(1)
        group = STATE_TO_GROUP.get(state)
        if group:
            return group
    # Try to extract country
    m = COUNTRY_RE.search(location)
    if m:
        country = m.group(1).strip()
        group = STATE_TO_GROUP.get(country)
        if group:
            return group
    # Fallback
    return 'Midwest'

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, location FROM courses')
    courses = cursor.fetchall()
    for course_id, name, location in courses:
        group = get_climate_group(location)
        env = CLIMATE_GROUPS[group]
        # Environmental
        temp_factor = env['avg_temp']
        humidity_factor = env['humidity']
        wind_factor = env['wind']
        rain_factor = env['rain_prob']
        cloud_factor = 0
        elevation_factor = env['elevation']
        # Static
        design_strategy = rand(0.2, 0.9)
        narrowness_factor = rand(0.2, 0.9)
        hazard_density = rand(0.2, 0.9)
        green_speed = rand(0.3, 1.0)
        turf_firmness = rand(0.3, 1.0)
        rough_length = rand(0.2, 0.9)
        prestige_level = rand(0.2, 1.0)
        crowd_factor = rand(0.2, 1.0)
        terrain_difficulty = rand(0.1, 0.9)
        # Insert or replace
        cursor.execute('''
            INSERT OR REPLACE INTO course_characteristics (
                course_id, temp_factor, humidity_factor, wind_factor, rain_factor, cloud_factor,
                design_strategy, narrowness_factor, hazard_density, green_speed,
                turf_firmness, rough_length, prestige_level, crowd_factor,
                elevation_factor, terrain_difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            course_id, temp_factor, humidity_factor, wind_factor, rain_factor, cloud_factor,
            design_strategy, narrowness_factor, hazard_density, green_speed,
            turf_firmness, rough_length, prestige_level, crowd_factor,
            elevation_factor, terrain_difficulty
        ))
        print(f"Seeded characteristics for {name} (group: {group})")
    conn.commit()
    conn.close()
    print("Done populating course_characteristics.")

if __name__ == "__main__":
    main() 