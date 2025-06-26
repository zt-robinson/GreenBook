#!/usr/bin/env python3
import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

def parse_location_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all courses with their current location data
    cursor.execute('SELECT id, name, location FROM courses')
    courses = cursor.fetchall()
    
    updated_count = 0
    
    for course_id, name, location in courses:
        if not location:
            print(f"Skipping {name}: No location data")
            continue
            
        # Parse location format: "City, State/Province (Country)"
        # Examples: "Bathgate, Scotland (UK)", "Mesa, AZ (US)", "Vancouver, BC (CAN)"
        
        # Use regex to extract city and state/country
        match = re.match(r'^([^,]+),\s*([^(]+)\s*\(([^)]+)\)$', location.strip())
        
        if match:
            city = match.group(1).strip()
            state_province = match.group(2).strip()
            country = match.group(3).strip()
            
            # Combine state/province and country for state_country field
            state_country = f"{state_province} ({country})"
            
            # Update the database
            cursor.execute(
                'UPDATE courses SET city = ?, state_country = ? WHERE id = ?',
                (city, state_country, course_id)
            )
            
            print(f"Updated {name}: City='{city}', State/Country='{state_country}'")
            updated_count += 1
        else:
            print(f"Could not parse location for {name}: '{location}'")
    
    conn.commit()
    conn.close()
    print(f"\nUpdated {updated_count} courses with parsed location data.")

if __name__ == "__main__":
    parse_location_data() 