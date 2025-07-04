#!/usr/bin/env python3
"""
Import courses from CSV file into the golf courses database.
This script reads the CSV file with course data and weather information,
calculates weather factors, and inserts the data into the database.
"""

import csv
import sqlite3
import os
import sys
from datetime import datetime
import random

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')

def calculate_elevation_factor(elevation_str):
    """Convert elevation in feet to elevation_factor (0.0-1.0 scale)."""
    try:
        if elevation_str and elevation_str.strip() and elevation_str.strip() != "###":
            elevation_feet = float(elevation_str.strip())
            # Convert to 0-1 scale: elevation_factor = elevation_feet / 7724
            elevation_factor = elevation_feet / 7724.0
            # Clamp to 0-1 range
            return max(0.0, min(1.0, elevation_factor))
        else:
            return 0.3  # Default elevation factor
    except (ValueError, TypeError):
        return 0.3  # Default on error

def calculate_temp_factor(temp_values):
    """Calculate temperature factor from monthly average temperatures."""
    try:
        # Convert to float and filter out invalid values
        temps = [float(t) for t in temp_values if t and t.strip() and t.strip() != "###"]
        if not temps:
            return 0.5  # Default if no valid data
        
        avg_temp = sum(temps) / len(temps)
        # Normalize: 32°F = 0.0, 100°F = 1.0
        temp_factor = (avg_temp - 32) / 68.0
        return max(0.0, min(1.0, temp_factor))
    except (ValueError, TypeError):
        return 0.5

def calculate_humidity_factor(humidity_values):
    """Calculate humidity factor from monthly average humidity."""
    try:
        # Convert to float and filter out invalid values
        humidities = [float(h) for h in humidity_values if h and h.strip() and h.strip() != "###"]
        if not humidities:
            return 0.5  # Default if no valid data
        
        avg_humidity = sum(humidities) / len(humidities)
        # Direct percentage to 0-1 scale
        humidity_factor = avg_humidity / 100.0
        return max(0.0, min(1.0, humidity_factor))
    except (ValueError, TypeError):
        return 0.5

def calculate_wind_factor(wind_values):
    """Calculate wind factor from monthly average wind speeds."""
    try:
        # Convert to float and filter out invalid values
        winds = [float(w) for w in wind_values if w and w.strip() and w.strip() != "###"]
        if not winds:
            return 0.3  # Default if no valid data
        
        avg_wind = sum(winds) / len(winds)
        # Normalize: 0 mph = 0.0, 30+ mph = 1.0
        wind_factor = avg_wind / 30.0
        return max(0.0, min(1.0, wind_factor))
    except (ValueError, TypeError):
        return 0.3

def calculate_rain_factor(rain_values):
    """Calculate rain factor from monthly rain probabilities."""
    try:
        # Convert to float and filter out invalid values
        rains = [float(r) for r in rain_values if r and r.strip() and r.strip() != "###"]
        if not rains:
            return 0.2  # Default if no valid data
        
        avg_rain = sum(rains) / len(rains)
        # Direct percentage to 0-1 scale
        rain_factor = avg_rain / 100.0
        return max(0.0, min(1.0, rain_factor))
    except (ValueError, TypeError):
        return 0.2

def calculate_cloud_factor(cloud_values):
    """Calculate cloud factor from monthly average cloud cover."""
    try:
        # Convert to float and filter out invalid values
        clouds = [float(c) for c in cloud_values if c and c.strip() and c.strip() != "###"]
        if not clouds:
            return 0.5  # Default if no valid data
        
        avg_cloud = sum(clouds) / len(clouds)
        # Direct percentage to 0-1 scale
        cloud_factor = avg_cloud / 100.0
        return max(0.0, min(1.0, cloud_factor))
    except (ValueError, TypeError):
        return 0.5

def ensure_database_tables():
    """Ensure the database tables exist with the correct schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            city TEXT,
            state_country TEXT,
            location TEXT,
            total_par INTEGER NOT NULL,
            total_yardage INTEGER NOT NULL,
            slope_rating INTEGER,
            course_rating REAL,
            prestige_level INTEGER DEFAULT 50,
            est_year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create course_characteristics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course_characteristics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            avg_temperature REAL,
            humidity_level REAL,
            wind_factor REAL,
            rain_probability REAL,
            design_strategy REAL,
            narrowness_factor REAL,
            hazard_density REAL,
            green_speed REAL,
            turf_firmness REAL,
            rough_length REAL,
            course_age REAL,
            crowd_factor REAL,
            elevation_factor REAL,
            terrain_difficulty REAL,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            UNIQUE(course_id)
        )
    ''')
    
    # Create holes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            hole_number INTEGER NOT NULL,
            par INTEGER NOT NULL,
            yardage INTEGER NOT NULL,
            handicap INTEGER,
            difficulty_modifier REAL DEFAULT 1.0,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            UNIQUE(course_id, hole_number)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database tables ensured")

def get_weather_factors_from_csv(row):
    """
    Get the pre-calculated weather factors from the CSV columns.
    These are the values you calculated in Excel.
    """
    factors = {}
    
    # Get the pre-calculated weather factors from the CSV
    factors['temp_factor'] = float(row['temp_factor']) if row['temp_factor'] and row['temp_factor'].strip() else 0.5
    factors['wind_factor'] = float(row['wind_factor']) if row['wind_factor'] and row['wind_factor'].strip() else 0.3
    factors['rain_factor'] = float(row['rain_factor']) if row['rain_factor'] and row['rain_factor'].strip() else 0.2
    factors['humidity_factor'] = float(row['humidity_factor']) if row['humidity_factor'] and row['humidity_factor'].strip() else 0.5
    factors['cloud_factor'] = float(row['cloud_factor']) if row['cloud_factor'] and row['cloud_factor'].strip() else 0.5
    
    return factors

def insert_course_to_database(course_data, characteristics_data):
    """Insert a course and its characteristics into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Insert main course record
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
            characteristics_data.get('temp_factor', 0.5),
            characteristics_data.get('humidity_factor', 0.5),
            characteristics_data.get('wind_factor', 0.3),
            characteristics_data.get('rain_factor', 0.2),
            characteristics_data.get('design_strategy', 0.5),
            characteristics_data.get('narrowness_factor', 0.5),
            characteristics_data.get('hazard_density', 0.5),
            characteristics_data.get('green_speed', 0.7),
            characteristics_data.get('turf_firmness', 0.7),
            characteristics_data.get('rough_length', 0.5),
            characteristics_data.get('crowd_factor', 0.5),
            characteristics_data.get('elevation_factor', 0.3),
            characteristics_data.get('terrain_difficulty', 0.5)
        ))
        
        conn.commit()
        return course_id
        
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"⚠️  Course '{course_data['name']}' already exists, skipping...")
            return None
        else:
            raise e
    finally:
        conn.close()

def process_csv_row(row):
    """Process a single CSV row and return course and characteristics data."""
    
    # Parse location to extract city and state_country
    location = row['location'].strip()
    city = ""
    state_country = ""
    
    # Parse location format: "City, State (Country)"
    if ',' in location:
        parts = location.split(',', 1)
        city = parts[0].strip()
        state_country = parts[1].strip()
    else:
        city = location
        state_country = ""
    
    # Extract course data using actual column names
    course_data = {
        'name': row['course_name'].strip(),
        'city': city,
        'state_country': state_country,
        'location': location,
        'total_par': int(row['total_par']) if row['total_par'] and row['total_par'].strip() else 72,
        'total_yardage': int(row['total_yards']) if row['total_yards'] and row['total_yards'].strip() else 7000,
        'slope_rating': round(float(row['slope_rating']), 1) if row['slope_rating'] and row['slope_rating'].strip() else 140.0,
        'course_rating': round(float(row['course_rating']), 1) if row['course_rating'] and row['course_rating'].strip() else 75.0,
        'prestige_level': float(row['prestige_level']) if row['prestige_level'] and row['prestige_level'].strip() else 50.0,
        'est_year': int(row['est_year']) if row['est_year'] and row['est_year'].strip() else 1990
    }
    
    # Calculate weather factors from raw data
    # Get monthly temperature data
    temp_values = [row.get(f'temp_avg_{month}', '') for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']]
    temp_factor = calculate_temp_factor(temp_values)
    
    # Get monthly humidity data
    humidity_values = [row.get(f'humidity_avg_{month}', '') for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']]
    humidity_factor = calculate_humidity_factor(humidity_values)
    
    # Get monthly wind data
    wind_values = [row.get(f'wind_speed_avg_{month}', '') for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']]
    wind_factor = calculate_wind_factor(wind_values)
    
    # Get monthly rain data
    rain_values = [row.get(f'rain_prop_{month}', '') for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']]
    rain_factor = calculate_rain_factor(rain_values)
    
    # Get monthly cloud data
    cloud_values = [row.get(f'cloud_cover_avg_{month}', '') for month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']]
    cloud_factor = calculate_cloud_factor(cloud_values)
    
    # Calculate elevation factor
    elevation_factor = calculate_elevation_factor(row.get('elevation', ''))
    
    # Extract characteristics data using actual column names
    characteristics_data = {
        'temp_factor': temp_factor,
        'wind_factor': wind_factor,
        'rain_factor': rain_factor,
        'humidity_factor': humidity_factor,
        'cloud_factor': cloud_factor,
        'design_strategy': float(row['design_strategy']) if row['design_strategy'] and row['design_strategy'].strip() else 0.5,
        'narrowness_factor': float(row['narrowness_factor']) if row['narrowness_factor'] and row['narrowness_factor'].strip() else 0.5,
        'hazard_density': float(row['hazard_density']) if row['hazard_density'] and row['hazard_density'].strip() else 0.5,
        'green_speed': float(row['green_speed']) if row['green_speed'] and row['green_speed'].strip() else 0.7,
        'turf_firmness': float(row['turf_firmness']) if row['turf_firmness'] and row['turf_firmness'].strip() else 0.7,
        'rough_length': float(row['rough_length']) if row['rough_length'] and row['rough_length'].strip() else 0.5,
        'crowd_factor': float(row['crowd_factor']) if row['crowd_factor'] and row['crowd_factor'].strip() else 0.5,
        'elevation_factor': elevation_factor,
        'terrain_difficulty': float(row['terrain_difficulty']) if row['terrain_difficulty'] and row['terrain_difficulty'].strip() else 0.5
    }
    
    return course_data, characteristics_data

def course_exists_in_location(city, state_country):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT 1 FROM courses WHERE city = ? AND state_country = ? LIMIT 1",
        (city, state_country)
    )
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def import_courses_from_csv(csv_file_path):
    """Import all courses from the CSV file."""
    if not os.path.exists(csv_file_path):
        print(f"❌ CSV file not found: {csv_file_path}")
        return
    
    print(f"📁 Reading CSV file: {csv_file_path}")
    
    imported_count = 0
    skipped_count = 0
    error_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is header
            try:
                # Skip empty rows
                if not row['course_name'] or not row['course_name'].strip():
                    continue
                
                course_data, characteristics_data = process_csv_row(row)
                
                # Check for duplicate location
                if course_exists_in_location(course_data['city'], course_data['state_country']):
                    print(f"⚠️  Skipping {course_data['name']} (duplicate location: {course_data['city']}, {course_data['state_country']})")
                    skipped_count += 1
                    continue
                
                course_id = insert_course_to_database(course_data, characteristics_data)
                
                if course_id:
                    imported_count += 1
                    print(f"✅ Imported: {course_data['name']} (ID: {course_id})")
                else:
                    skipped_count += 1
                    
            except Exception as e:
                error_count += 1
                print(f"❌ Error processing row {row_num}: {e}")
                print(f"   Row data: {row.get('course_name', 'N/A')}")
                continue
    
    print(f"\n📊 Import Summary:")
    print(f"   ✅ Successfully imported: {imported_count} courses")
    print(f"   ⚠️  Skipped (duplicates): {skipped_count} courses")
    print(f"   ❌ Errors: {error_count} courses")

def main():
    """Main function to run the import process."""
    print("🏌️  Golf Course CSV Import Tool")
    print("=" * 40)
    
    # Ensure database tables exist
    ensure_database_tables()
    
    # Check for command line argument
    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
    else:
        # Default CSV file path
        csv_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample courses.csv')
    
    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"❌ CSV file not found: {csv_file_path}")
        print("Please ensure the CSV file is in the correct location.")
        return
    
    # Import courses
    import_courses_from_csv(csv_file_path)
    
    print("\n🎉 Import process completed!")

if __name__ == "__main__":
    main() 