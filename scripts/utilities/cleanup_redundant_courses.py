#!/usr/bin/env python3
"""
Cleanup Redundant Courses Script
Identifies and removes redundant courses in the same city while preserving
courses that are currently assigned to tournaments.
"""

import sqlite3
import os
from collections import defaultdict

# Database paths
COURSES_DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_courses.db')
TOURNAMENTS_DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_tournaments.db')

def get_courses_in_tournaments():
    """Get list of course IDs that are currently assigned to tournaments."""
    try:
        conn = sqlite3.connect(TOURNAMENTS_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT course_id FROM tournaments WHERE course_id IS NOT NULL")
        used_course_ids = {row[0] for row in cursor.fetchall()}
        conn.close()
        return used_course_ids
    except Exception as e:
        print(f"❌ Error getting courses in tournaments: {e}")
        return set()

def get_all_courses():
    """Get all courses with their details."""
    try:
        conn = sqlite3.connect(COURSES_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, city, state_country FROM courses ORDER BY city, name")
        courses = []
        for row in cursor.fetchall():
            courses.append({
                'id': row[0],
                'name': row[1],
                'city': row[2],
                'state_country': row[3]
            })
        conn.close()
        return courses
    except Exception as e:
        print(f"❌ Error getting all courses: {e}")
        return []

def extract_city_from_name(name):
    """Extract city name from course name by removing common suffixes."""
    suffixes = [
        ' golf club', ' country club', ' hunt club', ' golf & country club',
        ' cricket club', ' athletic club', ' club', ' national golf club',
        ' golf & hunt club', ' golf & tennis club', ' polo club', ' hunt & country club'
    ]
    
    name_lower = name.lower()
    for suffix in suffixes:
        if name_lower.endswith(suffix):
            name_lower = name_lower[:-len(suffix)]
            break
    
    return name_lower.strip()

def find_redundant_courses(courses, used_course_ids):
    """Find redundant courses in the same city."""
    # Group courses by city
    city_courses = defaultdict(list)
    for course in courses:
        city_key = f"{course['city']}, {course['state_country']}"
        city_courses[city_key].append(course)
    
    redundant_groups = []
    
    for city, city_course_list in city_courses.items():
        if len(city_course_list) <= 1:
            continue
        
        # Check for courses that start with the city name
        city_name = city_course_list[0]['city']
        courses_with_city_name = []
        
        for course in city_course_list:
            extracted_city = extract_city_from_name(course['name'])
            if extracted_city.lower() == city_name.lower():
                courses_with_city_name.append(course)
        
        # If multiple courses have city name, we have redundancy
        if len(courses_with_city_name) > 1:
            # Check which ones are used in tournaments
            used_in_city = [c for c in courses_with_city_name if c['id'] in used_course_ids]
            unused_in_city = [c for c in courses_with_city_name if c['id'] not in used_course_ids]
            
            if unused_in_city:  # Only add if there are unused ones to remove
                redundant_groups.append({
                    'city': city,
                    'city_name': city_name,
                    'all_courses': courses_with_city_name,
                    'used_courses': used_in_city,
                    'unused_courses': unused_in_city
                })
        
        # Only flag as redundant if there are MULTIPLE courses with the city name
        # This prevents removing single courses like "West Jordan Golf & Country Club"
        # when there are other courses in the city that don't use the city name
    
    return redundant_groups

def remove_redundant_courses(redundant_groups):
    """Remove redundant courses from the database."""
    conn = sqlite3.connect(COURSES_DB_PATH)
    cursor = conn.cursor()
    
    total_removed = 0
    
    try:
        for group in redundant_groups:
            print(f"\n🏙️  City: {group['city']}")
            print(f"   City name in courses: {group['city_name']}")
            
            if group['used_courses']:
                print(f"   ✅ Keeping (used in tournaments):")
                for course in group['used_courses']:
                    print(f"      - {course['name']} (ID: {course['id']})")
            
            if group['unused_courses']:
                print(f"   🗑️  Removing (redundant):")
                for course in group['unused_courses']:
                    print(f"      - {course['name']} (ID: {course['id']})")
                    
                    # Remove from courses table
                    cursor.execute("DELETE FROM courses WHERE id = ?", (course['id'],))
                    
                    # Remove from course_characteristics table
                    cursor.execute("DELETE FROM course_characteristics WHERE course_id = ?", (course['id'],))
                    
                    # Remove from holes table
                    cursor.execute("DELETE FROM holes WHERE course_id = ?", (course['id'],))
                    
                    total_removed += 1
        
        conn.commit()
        print(f"\n✅ Successfully removed {total_removed} redundant courses")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error removing courses: {e}")
        raise e
    finally:
        conn.close()
    
    return total_removed

def main():
    """Main cleanup function."""
    print("🏌️  Redundant Course Cleanup")
    print("=" * 80)
    
    # Get courses currently used in tournaments
    print("📋 Getting courses currently assigned to tournaments...")
    used_course_ids = get_courses_in_tournaments()
    print(f"✅ Found {len(used_course_ids)} courses currently in use")
    
    # Get all courses
    print("\n📋 Getting all courses from database...")
    all_courses = get_all_courses()
    print(f"✅ Found {len(all_courses)} total courses")
    
    # Find redundant courses
    print("\n🔍 Finding redundant courses...")
    redundant_groups = find_redundant_courses(all_courses, used_course_ids)
    
    if not redundant_groups:
        print("✅ No redundant courses found!")
        return
    
    print(f"⚠️  Found {len(redundant_groups)} cities with redundant courses")
    
    # Show what will be removed
    print("\n📋 Redundant courses to be removed:")
    total_to_remove = 0
    for group in redundant_groups:
        total_to_remove += len(group['unused_courses'])
        print(f"\n🏙️  {group['city']}:")
        for course in group['unused_courses']:
            print(f"   🗑️  {course['name']} (ID: {course['id']})")
    
    # Ask for confirmation
    print(f"\n⚠️  About to remove {total_to_remove} redundant courses")
    response = input("Continue? (y/N): ").strip().lower()
    
    if response != 'y':
        print("❌ Cleanup cancelled")
        return
    
    # Remove redundant courses
    print("\n🗑️  Removing redundant courses...")
    removed_count = remove_redundant_courses(redundant_groups)
    
    print(f"\n🎉 Cleanup complete! Removed {removed_count} redundant courses")
    print("✅ Preserved all courses currently assigned to tournaments")

if __name__ == "__main__":
    main() 