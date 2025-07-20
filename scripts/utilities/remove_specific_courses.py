#!/usr/bin/env python3
"""
Remove Specific Courses Script
Removes the three specific courses requested by the user.
"""

import sqlite3
import os

# Database path
COURSES_DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_courses.db')

def remove_specific_courses():
    """Remove the three specific courses requested."""
    
    # Define courses to remove (ID: name)
    courses_to_remove = [
        (38, "Caldwell Golf & Tennis Club"),
        (92, "Dallas Point Golf & Tennis Club"),
        (170, "PCC Grand Rapids"),
    ]
    
    print("🗑️  Courses to remove:")
    for course_id, name in courses_to_remove:
        print(f"   • {name} (ID: {course_id})")
    
    # Ask for confirmation
    response = input(f"\n⚠️  Remove these 3 courses? (y/N): ").strip().lower()
    if response != 'y':
        print("❌ Removal cancelled")
        return
    
    # Remove the courses
    conn = sqlite3.connect(COURSES_DB_PATH)
    cursor = conn.cursor()
    
    try:
        removed_count = 0
        for course_id, name in courses_to_remove:
            print(f"🗑️  Removing {name} (ID: {course_id})...")
            
            # Remove from courses table
            cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
            
            # Remove from course_characteristics table
            cursor.execute("DELETE FROM course_characteristics WHERE course_id = ?", (course_id,))
            
            # Remove from holes table
            cursor.execute("DELETE FROM holes WHERE course_id = ?", (course_id,))
            
            removed_count += 1
        
        conn.commit()
        print(f"\n✅ Successfully removed {removed_count} courses")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error removing courses: {e}")
        raise e
    finally:
        conn.close()

if __name__ == "__main__":
    print("🏌️  Remove Specific Courses")
    print("=" * 80)
    remove_specific_courses() 