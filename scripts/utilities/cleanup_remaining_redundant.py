#!/usr/bin/env python3
"""
Cleanup Remaining Redundant Courses Script
Removes the remaining redundant courses identified in the screenshot.
"""

import sqlite3
import os

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

def remove_remaining_redundant_courses():
    """Remove remaining redundant courses identified in the screenshot."""
    
    # Get courses currently used in tournaments
    used_course_ids = get_courses_in_tournaments()
    print(f"✅ Found {len(used_course_ids)} courses currently in use")
    
    # Define remaining redundant courses to remove (ID: name, city)
    redundant_courses = [
        (92, "Dallas Point Golf & Tennis Club", "Dallas, TX"),
        (139, "Grand Rapids Golf Club", "Grand Rapids, MI"),
        (38, "Caldwell Golf & Tennis Club", "Caldwell, ID"),
        (174, "Buffalo Country Club", "Buffalo, NY"),
        (180, "Beckley Country Club", "Beckley, WV"),
    ]
    
    # Filter out courses that are used in tournaments
    courses_to_remove = []
    for course_id, name, city in redundant_courses:
        if course_id not in used_course_ids:
            courses_to_remove.append((course_id, name, city))
        else:
            print(f"⚠️  Keeping {name} (ID: {course_id}) - used in tournaments")
    
    if not courses_to_remove:
        print("✅ No redundant courses to remove!")
        return
    
    print(f"\n🗑️  Courses to remove ({len(courses_to_remove)}):")
    for course_id, name, city in courses_to_remove:
        print(f"   • {name} (ID: {course_id}) - {city}")
    
    # Ask for confirmation
    response = input(f"\n⚠️  Remove {len(courses_to_remove)} redundant courses? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Cleanup cancelled")
        return
    
    # Remove the courses
    conn = sqlite3.connect(COURSES_DB_PATH)
    cursor = conn.cursor()
    
    try:
        removed_count = 0
        for course_id, name, city in courses_to_remove:
            print(f"🗑️  Removing {name} (ID: {course_id})...")
            
            # Remove from courses table
            cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
            
            # Remove from course_characteristics table
            cursor.execute("DELETE FROM course_characteristics WHERE course_id = ?", (course_id,))
            
            # Remove from holes table
            cursor.execute("DELETE FROM holes WHERE course_id = ?", (course_id,))
            
            removed_count += 1
        
        conn.commit()
        print(f"\n✅ Successfully removed {removed_count} redundant courses")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error removing courses: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    print("🏌️  Remaining Redundant Course Cleanup")
    print("=" * 80)
    remove_remaining_redundant_courses() 