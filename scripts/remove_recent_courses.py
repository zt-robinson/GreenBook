#!/usr/bin/env python3
"""
Remove recently imported courses (IDs 558-716) to allow regeneration with proper elevation data.
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')

def remove_recent_courses():
    """Remove courses with IDs 558-716 and their associated characteristics."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # First, get the course names for reporting
        cursor.execute('SELECT id, name FROM courses WHERE id >= 558 AND id <= 716 ORDER BY id')
        courses_to_remove = cursor.fetchall()
        
        if not courses_to_remove:
            print("No courses found in the specified ID range (558-716)")
            return
        
        print(f"Found {len(courses_to_remove)} courses to remove:")
        for course_id, name in courses_to_remove:
            print(f"  ID {course_id}: {name}")
        
        # Remove course characteristics first (due to foreign key constraint)
        cursor.execute('DELETE FROM course_characteristics WHERE course_id >= 558 AND course_id <= 716')
        characteristics_removed = cursor.rowcount
        
        # Remove holes (if any exist for these courses)
        cursor.execute('DELETE FROM holes WHERE course_id >= 558 AND course_id <= 716')
        holes_removed = cursor.rowcount
        
        # Remove the courses
        cursor.execute('DELETE FROM courses WHERE id >= 558 AND id <= 716')
        courses_removed = cursor.rowcount
        
        conn.commit()
        
        print(f"\n✅ Removal completed:")
        print(f"   - {courses_removed} courses removed")
        print(f"   - {characteristics_removed} course characteristics removed")
        print(f"   - {holes_removed} holes removed")
        
    except Exception as e:
        print(f"❌ Error removing courses: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Main function to run the removal process."""
    print("🗑️  Recent Courses Removal Tool")
    print("=" * 40)
    
    # Confirm with user
    response = input("Are you sure you want to remove all courses with IDs 558-716? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Operation cancelled.")
        return
    
    remove_recent_courses()
    print("\n🎉 Removal process completed!")

if __name__ == "__main__":
    main() 