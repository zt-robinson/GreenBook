#!/usr/bin/env python3
"""
Show Course Variety Script
Displays courses grouped by city to show the variety of naming patterns.
"""

import sqlite3
import os
from collections import defaultdict

# Database path
COURSES_DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_courses.db')

def show_course_variety():
    """Show courses grouped by city to demonstrate naming variety."""
    try:
        conn = sqlite3.connect(COURSES_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT city, state_country, name, id 
            FROM courses 
            ORDER BY city, name
        """)
        
        courses = cursor.fetchall()
        conn.close()
        
        # Group by city
        city_courses = defaultdict(list)
        for course in courses:
            city_key = f"{course[0]}, {course[1]}"
            city_courses[city_key].append({
                'name': course[2],
                'id': course[3]
            })
        
        print("🏌️  Course Variety by City")
        print("=" * 80)
        
        # Show cities with multiple courses
        multi_course_cities = {city: courses for city, courses in city_courses.items() if len(courses) > 1}
        
        print(f"📊 Found {len(multi_course_cities)} cities with multiple courses:")
        print()
        
        for city, course_list in sorted(multi_course_cities.items()):
            print(f"🏙️  {city} ({len(course_list)} courses):")
            for course in course_list:
                print(f"   • {course['name']} (ID: {course['id']})")
            print()
        
        # Show some single-course cities for comparison
        single_course_cities = {city: courses for city, courses in city_courses.items() if len(courses) == 1}
        print(f"📊 Found {len(single_course_cities)} cities with single courses")
        print()
        
        # Show a few examples of single-course cities
        print("🏙️  Examples of single-course cities:")
        for i, (city, course_list) in enumerate(sorted(single_course_cities.items())):
            if i >= 10:  # Show first 10
                break
            course = course_list[0]
            print(f"   • {city}: {course['name']} (ID: {course['id']})")
        
        if len(single_course_cities) > 10:
            print(f"   ... and {len(single_course_cities) - 10} more")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    show_course_variety() 