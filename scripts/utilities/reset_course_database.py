#!/usr/bin/env python3
"""
Reset Course Database Script
Deletes all courses and resets auto-increment counters to start fresh.
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_courses.db')

def reset_course_database():
    """Delete all courses and reset auto-increment counters"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found: {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get current counts
        cursor.execute("SELECT COUNT(*) FROM courses")
        course_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM course_characteristics")
        char_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM holes")
        hole_count = cursor.fetchone()[0]
        
        print(f"📊 Current database state:")
        print(f"   Courses: {course_count}")
        print(f"   Course characteristics: {char_count}")
        print(f"   Holes: {hole_count}")
        
        if course_count == 0:
            print("✅ Database is already empty!")
            return True
        
        # Delete all data
        print("\n🗑️  Deleting all course data...")
        cursor.execute("DELETE FROM holes")
        cursor.execute("DELETE FROM course_characteristics")
        cursor.execute("DELETE FROM courses")
        
        # Reset auto-increment counters
        print("🔄 Resetting auto-increment counters...")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='courses'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='course_characteristics'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='holes'")
        
        # Commit changes
        conn.commit()
        
        # Verify reset
        cursor.execute("SELECT COUNT(*) FROM courses")
        new_course_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM course_characteristics")
        new_char_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM holes")
        new_hole_count = cursor.fetchone()[0]
        
        print(f"\n✅ Database reset complete!")
        print(f"   Courses: {new_course_count}")
        print(f"   Course characteristics: {new_char_count}")
        print(f"   Holes: {new_hole_count}")
        print(f"\n🎯 Next course will have ID: 1")
        
        return True
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def main():
    """Main function"""
    print("🏌️  Course Database Reset Tool")
    print("=" * 50)
    
    # Check if courses exist
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM courses")
    course_count = cursor.fetchone()[0]
    conn.close()
    
    if course_count == 0:
        print("✅ Database is already empty!")
        return
    
    # Ask for confirmation
    print(f"⚠️  This will delete {course_count} courses and all associated data.")
    response = input("Are you sure you want to continue? (y/N): ")
    
    if response.lower() not in ['y', 'yes']:
        print("❌ Operation cancelled.")
        return
    
    success = reset_course_database()
    
    if success:
        print("\n🎉 Database reset successful! Ready for fresh course generation.")
    else:
        print("\n❌ Database reset failed!")

if __name__ == "__main__":
    main() 