#!/usr/bin/env python3
"""
Import both course and hole data from the main course CSV (07.02.25_new_courses.csv), inserting into courses, course_characteristics, and holes tables in one go. Does NOT delete existing courses.
"""
import sqlite3
import os
import csv
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', '07.02.25_new_courses.csv')

FRONT9_START = 2
BACK9_START = 31

def calculate_elevation_factor(elevation_str):
    try:
        if elevation_str and elevation_str.strip() and elevation_str.strip() != "###":
            elevation_feet = float(elevation_str.strip())
            elevation_factor = elevation_feet / 7724.0
            return max(0.0, min(1.0, elevation_factor))
        else:
            return 0.3
    except (ValueError, TypeError):
        return 0.3

def calculate_temp_factor(temp_values):
    try:
        temps = [float(t) for t in temp_values if t and t.strip() and t.strip() != "###"]
        if not temps:
            return 0.5
        avg_temp = sum(temps) / len(temps)
        temp_factor = (avg_temp - 32) / 68.0
        return max(0.0, min(1.0, temp_factor))
    except (ValueError, TypeError):
        return 0.5

def calculate_humidity_factor(humidity_values):
    try:
        humidities = [float(h) for h in humidity_values if h and h.strip() and h.strip() != "###"]
        if not humidities:
            return 0.5
        avg_humidity = sum(humidities) / len(humidities)
        humidity_factor = avg_humidity / 100.0
        return max(0.0, min(1.0, humidity_factor))
    except (ValueError, TypeError):
        return 0.5

def calculate_wind_factor(wind_values):
    try:
        winds = [float(w) for w in wind_values if w and w.strip() and w.strip() != "###"]
        if not winds:
            return 0.3
        avg_wind = sum(winds) / len(winds)
        wind_factor = avg_wind / 30.0
        return max(0.0, min(1.0, wind_factor))
    except (ValueError, TypeError):
        return 0.3

def calculate_rain_factor(rain_values):
    try:
        rains = [float(r) for r in rain_values if r and r.strip() and r.strip() != "###"]
        if not rains:
            return 0.2
        avg_rain = sum(rains) / len(rains)
        rain_factor = avg_rain / 100.0
        return max(0.0, min(1.0, rain_factor))
    except (ValueError, TypeError):
        return 0.2

def calculate_cloud_factor(cloud_values):
    try:
        clouds = [float(c) for c in cloud_values if c and c.strip() and c.strip() != "###"]
        if not clouds:
            return 0.5
        avg_cloud = sum(clouds) / len(clouds)
        cloud_factor = avg_cloud / 100.0
        return max(0.0, min(1.0, cloud_factor))
    except (ValueError, TypeError):
        return 0.5

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        inserted = 0
        for row in reader:
            course_name = row[0].strip()
            location = row[1].strip()
            # Parse location
            city = ""
            state_country = ""
            if ',' in location:
                parts = location.split(',', 1)
                city = parts[0].strip()
                state_country = parts[1].strip()
            else:
                city = location
                state_country = ""
            # Course data
            course_data = {
                'name': course_name,
                'city': city,
                'state_country': state_country,
                'location': location,
                'total_par': int(row[60]) if row[60] and row[60].strip() else 72,
                'total_yardage': int(row[61]) if row[61] and row[61].strip() else 7000,
                'slope_rating': round(float(row[62]), 1) if row[62] and row[62].strip() else 140.0,
                'course_rating': round(float(row[63]), 1) if row[63] and row[63].strip() else 75.0,
                'prestige_level': float(row[64]) if row[64] and row[64].strip() else 50.0,
                'est_year': int(row[65]) if row[65] and row[65].strip() else 1990
            }
            # Insert course
            cursor.execute('''
                INSERT INTO courses (
                    name, city, state_country, location, total_par, total_yardage,
                    slope_rating, course_rating, prestige_level, est_year, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course_data['name'],
                course_data['city'],
                course_data['state_country'],
                course_data['location'],
                course_data['total_par'],
                course_data['total_yardage'],
                course_data['slope_rating'],
                course_data['course_rating'],
                course_data['prestige_level'],
                course_data['est_year'],
                datetime.now().isoformat()
            ))
            course_id = cursor.lastrowid
            # Weather factors
            temp_values = [row[header.index(f'temp_avg_{m}')] for m in ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']]
            humidity_values = [row[header.index(f'humidity_avg_{m}')] for m in ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']]
            wind_values = [row[header.index(f'wind_speed_avg_{m}')] for m in ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']]
            rain_values = [row[header.index(f'rain_prop_{m}')] for m in ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']]
            cloud_values = [row[header.index(f'cloud_cover_avg_{m}')] for m in ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']]
            elevation_factor = calculate_elevation_factor(row[header.index('elevation')])
            temp_factor = calculate_temp_factor(temp_values)
            humidity_factor = calculate_humidity_factor(humidity_values)
            wind_factor = calculate_wind_factor(wind_values)
            rain_factor = calculate_rain_factor(rain_values)
            cloud_factor = calculate_cloud_factor(cloud_values)
            # Insert characteristics
            cursor.execute('''
                INSERT INTO course_characteristics (
                    course_id, temp_factor, humidity_factor, wind_factor, rain_factor,
                    design_strategy, narrowness_factor, hazard_density, green_speed,
                    turf_firmness, rough_length, crowd_factor,
                    elevation_factor, terrain_difficulty
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course_id,
                temp_factor,
                humidity_factor,
                wind_factor,
                rain_factor,
                float(row[header.index('design_strategy')]) if row[header.index('design_strategy')] else 0.5,
                float(row[header.index('narrowness_factor')]) if row[header.index('narrowness_factor')] else 0.5,
                float(row[header.index('hazard_density')]) if row[header.index('hazard_density')] else 0.5,
                float(row[header.index('green_speed')]) if row[header.index('green_speed')] else 0.7,
                float(row[header.index('turf_firmness')]) if row[header.index('turf_firmness')] else 0.7,
                float(row[header.index('rough_length')]) if row[header.index('rough_length')] else 0.5,
                float(row[header.index('crowd_factor')]) if row[header.index('crowd_factor')] else 0.5,
                elevation_factor,
                float(row[header.index('terrain_difficulty')]) if row[header.index('terrain_difficulty')] else 0.5
            ))
            # Insert holes 1-9
            for i in range(9):
                base = FRONT9_START + i * 3
                par = int(row[base])
                yardage = int(row[base + 1])
                handicap = int(row[base + 2])
                cursor.execute(
                    'INSERT INTO holes (course_id, hole_number, par, yardage, handicap, difficulty_modifier) VALUES (?, ?, ?, ?, ?, 1.0)',
                    (course_id, i + 1, par, yardage, handicap)
                )
            # Insert holes 10-18
            for i in range(9):
                base = BACK9_START + i * 3
                par = int(row[base])
                yardage = int(row[base + 1])
                handicap = int(row[base + 2])
                cursor.execute(
                    'INSERT INTO holes (course_id, hole_number, par, yardage, handicap, difficulty_modifier) VALUES (?, ?, ?, ?, ?, 1.0)',
                    (course_id, i + 10, par, yardage, handicap)
                )
            inserted += 1
        conn.commit()
    conn.close()
    print(f"✅ Imported {inserted} courses and their holes.")

if __name__ == "__main__":
    main() 