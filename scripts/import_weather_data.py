#!/usr/bin/env python3
"""
Script to import weather data from CSV files into the golf_courses.db database.
This creates a new table for monthly weather data and links it to existing courses.
"""
import sqlite3
import csv
import os
from pathlib import Path

# Database and CSV file paths
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/golf_courses.db')
CSV_DIR = os.path.join(os.path.dirname(__file__), '../data')

# CSV file names
CLOUD_CSV = 'course_cloud_averages.csv'
WIND_CSV = 'course_wind_averages.csv'
RAIN_CSV = 'course_rain_averages.csv'
HUMIDITY_CSV = 'course_humidity_averages.csv'
TEMP_CSV = 'course_temp_averages.csv'

def create_weather_table():
    """Create the course_monthly_weather table if it doesn't exist, and add temp columns if missing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course_monthly_weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            month INTEGER NOT NULL, -- 1-12 for Jan-Dec
            cloud_cover REAL, -- percentage of cloudy days (0.0-1.0)
            wind_speed REAL, -- average wind speed in mph
            rain_probability REAL, -- percentage of rainy days (0.0-1.0)
            humidity REAL, -- average relative humidity (0.0-1.0)
            min_temp REAL, -- min temperature (F)
            mean_temp REAL, -- mean temperature (F)
            max_temp REAL, -- max temperature (F)
            FOREIGN KEY(course_id) REFERENCES courses(id),
            UNIQUE(course_id, month)
        )
    ''')
    # Add columns if missing (for upgrades)
    for col in ['min_temp', 'mean_temp', 'max_temp']:
        try:
            cursor.execute(f"ALTER TABLE course_monthly_weather ADD COLUMN {col} REAL")
        except sqlite3.OperationalError:
            pass  # Already exists
    conn.commit()
    conn.close()
    print("✅ Created/updated course_monthly_weather table")

def get_course_id_mapping():
    """Get a mapping of course names to their database IDs."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, name FROM courses')
    courses = cursor.fetchall()
    conn.close()
    
    # Create mapping with some name normalization
    course_map = {}
    for course_id, name in courses:
        # Store original name
        course_map[name] = course_id
        
        # Also store without "Golf Club", "Country Club", etc.
        normalized_name = name.replace(' Golf Club', '').replace(' Country Club', '').replace(' National', '').replace(' Resort', '').replace(' Park', '').strip()
        if normalized_name != name:
            course_map[normalized_name] = course_id
            
        # Handle the special case with parentheses
        if '(Championship)' in name:
            clean_name = name.replace(' (Championship)', '')
            course_map[clean_name] = course_id
            # Also handle the CSV version with closing parenthesis
            csv_name = clean_name + ' Championship)'
            course_map[csv_name] = course_id
    
    # Handle specific course name mismatches between CSV and database
    course_map['Trout Fields Country Club'] = course_map.get('Trout Fields Golf Club')
    
    return course_map

def read_csv_data(filename):
    """Read CSV data and return as a list of dictionaries."""
    filepath = os.path.join(CSV_DIR, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  Warning: {filename} not found at {filepath}")
        return []
    
    data = []
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Trim whitespace from column names and values
            cleaned_row = {}
            for key, value in row.items():
                cleaned_key = key.strip()
                cleaned_value = value.strip() if value else value
                cleaned_row[cleaned_key] = cleaned_value
            data.append(cleaned_row)
    
    return data

def import_weather_data():
    """Import all weather data from CSV files into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get course mapping
    course_map = get_course_id_mapping()
    print(f"Found {len(course_map)} courses in database")
    
    # Read all CSV data
    cloud_data = read_csv_data(CLOUD_CSV)
    wind_data = read_csv_data(WIND_CSV)
    rain_data = read_csv_data(RAIN_CSV)
    humidity_data = read_csv_data(HUMIDITY_CSV)
    temp_data = read_csv_data(TEMP_CSV)
    
    # Debug: Check what columns are in temp_data
    if temp_data:
        print(f"DEBUG: Temperature CSV columns: {list(temp_data[0].keys())}")
        print(f"DEBUG: Looking for 'max_temp_dec' in columns: {'max_temp_dec' in temp_data[0].keys()}")
    
    if not all([cloud_data, wind_data, rain_data, humidity_data, temp_data]):
        print("❌ Missing one or more CSV files. Please ensure all weather CSV files are present.")
        return
    
    # Create a combined dataset
    weather_records = []
    processed_courses = set()
    
    # Process each course
    for cloud_row in cloud_data:
        course_name = cloud_row['course']
        
        # Find matching course in database
        course_id = course_map.get(course_name)
        if not course_id:
            print(f"⚠️  Warning: Course '{course_name}' not found in database")
            continue
        
        processed_courses.add(course_name)
        
        # Find corresponding data in other CSV files
        wind_row = next((row for row in wind_data if row['course'] == course_name), None)
        rain_row = next((row for row in rain_data if row['course'] == course_name), None)
        humidity_row = next((row for row in humidity_data if row['course'] == course_name), None)
        temp_row = next((row for row in temp_data if row['course'] == course_name), None)
        
        if not all([wind_row, rain_row, humidity_row, temp_row]):
            print(f"⚠️  Warning: Incomplete data for course '{course_name}'")
            continue
        
        # Create monthly records
        for month in range(1, 13):
            month_name = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 
                         'jul', 'aug', 'sep', 'oct', 'nov', 'dec'][month - 1]
            try:
                cloud_cover = float(cloud_row[f'cloud_{month_name}'])
                wind_speed = float(wind_row[f'wind_{month_name}'])
                rain_prob = float(rain_row[f'rain_{month_name}'])
                humidity = float(humidity_row[f'humidity_{month_name}'])
                min_temp = float(temp_row[f'min_temp_{month_name}'])
                mean_temp = float(temp_row[f'mean_temp_{month_name}'])
                max_temp = float(temp_row[f'max_temp_{month_name}'])
                weather_records.append({
                    'course_id': course_id,
                    'month': month,
                    'cloud_cover': cloud_cover,
                    'wind_speed': wind_speed,
                    'rain_probability': rain_prob,
                    'humidity': humidity,
                    'min_temp': min_temp,
                    'mean_temp': mean_temp,
                    'max_temp': max_temp
                })
            except (ValueError, KeyError) as e:
                print(f"⚠️  Warning: Error processing {course_name} month {month}: {e}")
    
    # Clear existing weather data
    cursor.execute('DELETE FROM course_monthly_weather')
    
    # Insert new weather data
    for record in weather_records:
        cursor.execute('''
            INSERT INTO course_monthly_weather 
            (course_id, month, cloud_cover, wind_speed, rain_probability, humidity, min_temp, mean_temp, max_temp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record['course_id'],
            record['month'],
            record['cloud_cover'],
            record['wind_speed'],
            record['rain_probability'],
            record['humidity'],
            record['min_temp'],
            record['mean_temp'],
            record['max_temp']
        ))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Successfully imported weather data for {len(processed_courses)} courses")
    print(f"✅ Created {len(weather_records)} monthly weather records")

def verify_import():
    """Verify the imported data."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check total records
    cursor.execute('SELECT COUNT(*) FROM course_monthly_weather')
    total_records = cursor.fetchone()[0]
    
    # Check courses with weather data
    cursor.execute('SELECT COUNT(DISTINCT course_id) FROM course_monthly_weather')
    courses_with_weather = cursor.fetchone()[0]
    
    # Sample some data
    cursor.execute('''
        SELECT c.name, w.month, w.cloud_cover, w.wind_speed, w.rain_probability, w.humidity, w.min_temp, w.mean_temp, w.max_temp
        FROM course_monthly_weather w
        JOIN courses c ON w.course_id = c.id
        ORDER BY c.name, w.month
        LIMIT 10
    ''')
    sample_data = cursor.fetchall()
    
    conn.close()
    
    print(f"\n📊 Import Verification:")
    print(f"   Total weather records: {total_records}")
    print(f"   Courses with weather data: {courses_with_weather}")
    print(f"   Average records per course: {total_records / courses_with_weather:.1f}")
    
    print(f"\n📋 Sample Data:")
    for row in sample_data:
        print(f"   {row[0]} (Month {row[1]}): Cloud {row[2]:.2f}, Wind {row[3]:.1f}mph, Rain {row[4]:.2f}, Humidity {row[5]:.2f}, Min {row[6]:.1f}F, Mean {row[7]:.1f}F, Max {row[8]:.1f}F")

def main():
    """Main function to run the import process."""
    print("🌤️  Starting weather data import...")
    
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return
    
    # Create weather table
    create_weather_table()
    
    # Import data
    import_weather_data()
    
    # Verify import
    verify_import()
    
    print("\n✅ Weather data import completed!")

if __name__ == '__main__':
    main() 