#!/usr/bin/env python3
"""
Generate the Continental Championship tournament
"""

import sqlite3
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.tournament_logic import tournament_logic
from core.event_types import event_type_manager

def get_available_courses():
    """Get list of available courses"""
    courses_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')
    
    if not os.path.exists(courses_db_path):
        print("❌ Courses database not found.")
        return []
    
    conn = sqlite3.connect(courses_db_path)
    cur = conn.cursor()
    
    try:
        cur.execute('SELECT id, name FROM courses ORDER BY name')
        courses = cur.fetchall()
        return courses
    finally:
        conn.close()

def create_continental_championship(course_id: int, start_date: str, 
                                  season_number: int, week_number: int):
    """Create the Continental Championship tournament"""
    
    tournament_name = "The Continental Championship"
    
    print(f"🌍 Creating Continental Championship: {tournament_name}")
    print("=" * 60)
    
    try:
        # Create the tournament using the tournament logic (no event_type for continental - uses overrides)
        tournament_id = tournament_logic.create_tournament(
            tournament_name=tournament_name,
            course_id=course_id,
            start_date=start_date,
            season_number=season_number,
            week_number=week_number,
            event_type=None  # Continental Championship uses tournament overrides, not event types
        )
        
        print(f"\n✅ Continental Championship '{tournament_name}' created successfully!")
        print(f"   Tournament ID: {tournament_id}")
        print(f"   Event Type: continental championship (uses tournament overrides)")
        print(f"   Course ID: {course_id}")
        print(f"   Start Date: {start_date}")
        print(f"   Season: {season_number}, Week: {week_number}")
        
        return tournament_id
        
    except Exception as e:
        print(f"❌ Error creating Continental Championship: {e}")
        return None

def main():
    """Main function to create the Continental Championship"""
    
    print("🌍 Continental Championship Generator")
    print("=" * 40)
    
    # Get available courses
    courses = get_available_courses()
    if not courses:
        print("❌ No courses available for tournaments")
        return
    
    print(f"📋 Found {len(courses)} available courses")
    
    # Continental Championship parameters
    tournament_name = "The Continental Championship"
    course_id = courses[0][0]  # Use first available course
    course_name = courses[0][1]
    start_date = "2025-08-01"  # After the majors
    season_number = 1
    week_number = 5  # Week after the majors
    
    print(f"\n📝 Creating Continental Championship with parameters:")
    print(f"   Name: {tournament_name}")
    print(f"   Course: {course_name}")
    print(f"   Date: {start_date}")
    print(f"   Season: {season_number}, Week: {week_number}")
    print(f"   Description: Special continental championship event")
    
    # Create the Continental Championship
    tournament_id = create_continental_championship(
        course_id=course_id,
        start_date=start_date,
        season_number=season_number,
        week_number=week_number
    )
    
    if tournament_id:
        print(f"\n🎉 Continental Championship created successfully!")
        print(f"   Tournament ID: {tournament_id}")
        print(f"   Ready to be used in tournament simulation")
        print(f"   This is a special championship event with unique configuration")
    else:
        print(f"\n❌ Failed to create Continental Championship")

if __name__ == "__main__":
    main() 