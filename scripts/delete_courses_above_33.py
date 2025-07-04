#!/usr/bin/env python3
"""
Delete all courses with IDs greater than 33, keeping courses 1-33.
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')

def delete_courses_above_33():
    """Delete courses with IDs > 33 and their associated characteristics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # First, get the course names for reporting
        cursor.execute('SELECT id, name FROM courses WHERE id > 33 ORDER BY id')
        courses_to_remove = cursor.fetchall()
        
        if not courses_to_remove:
            print("No courses found with IDs > 33")
            return
        
        print(f"Found {len(courses_to_remove)} courses to remove:")
        for course_id, name in courses_to_remove:
            print(f"  ID {course_id}: {name}")
        
        # Remove course characteristics first (due to foreign key constraint)
        cursor.execute('DELETE FROM course_characteristics WHERE course_id > 33')
        characteristics_removed = cursor.rowcount
        
        # Remove holes (if any exist for these courses)
        cursor.execute('DELETE FROM holes WHERE course_id > 33')
        holes_removed = cursor.rowcount
        
        # Remove the courses
        cursor.execute('DELETE FROM courses WHERE id > 33')
        courses_removed = cursor.rowcount
        
        # Commit the changes
        conn.commit()
        
        print(f"\n✅ Successfully removed:")
        print(f"   - {courses_removed} courses")
        print(f"   - {characteristics_removed} course characteristics")
        print(f"   - {holes_removed} holes")
        
        # Show remaining courses
        cursor.execute('SELECT COUNT(*) FROM courses')
        remaining_count = cursor.fetchone()[0]
        print(f"\n📊 Remaining courses in database: {remaining_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🗑️  Delete Courses Above ID 33")
    print("=" * 40)
    
    # Confirm with user
    response = input("Are you sure you want to delete all courses with IDs > 33? (yes/no): ").strip().lower()
    
    if response == 'yes':
        delete_courses_above_33()
    else:
        print("❌ Operation cancelled.") 