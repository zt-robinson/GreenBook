#!/usr/bin/env python3
"""
Create a single tournament with specified event type parameters for testing
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

def create_tournament(tournament_name, event_type, course_id=None, start_date="2025-07-04"):
    """Create a single tournament with specified parameters"""
    
    courses = get_available_courses()
    if not courses:
        print("❌ No courses available for tournaments")
        return None
    
    # Use specified course or first available course
    if course_id is None:
        course_id = courses[0][0]
        course_name = courses[0][1]
    else:
        # Find course name for the given ID
        course_name = None
        for cid, cname in courses:
            if cid == course_id:
                course_name = cname
                break
        if course_name is None:
            print(f"❌ Course ID {course_id} not found")
            return None
    
    try:
        # Create tournament using the event type system
        tournament_id = tournament_logic.create_tournament(
            tournament_name=tournament_name,
            course_id=course_id,
            start_date=start_date,
            season_number=0,
            week_number=1,
            event_type=event_type
        )
        
        print(f"✅ Created tournament: {tournament_name}")
        print(f"   ID: {tournament_id}")
        print(f"   Event Type: {event_type}")
        print(f"   Course: {course_name}")
        print(f"   Date: {start_date}")
        
        # Get tournament summary to show the generated parameters
        summary = tournament_logic.get_tournament_summary(tournament_id)
        if summary:
            print(f"   Field Size: {summary['tournament']['field_size']}")
            print(f"   Purse: ${summary['tournament']['purse_amount']:,}")
            print(f"   Prestige: {summary['tournament']['prestige_level']}")
            print(f"   Status: {summary['tournament']['status']}")
        
        return tournament_id
        
    except Exception as e:
        print(f"❌ Error creating {tournament_name}: {e}")
        return None

def main():
    print("🎯 Single Tournament Creator")
    print("=" * 40)
    
    # Show available courses
    courses = get_available_courses()
    print(f"Available courses ({len(courses)}):")
    for i, (course_id, course_name) in enumerate(courses[:5]):  # Show first 5
        print(f"   {course_id}: {course_name}")
    if len(courses) > 5:
        print(f"   ... and {len(courses) - 5} more")
    
    print("\nAvailable event types:")
    print("   - standard (random field size 144-165, random purse $7.9M-$9.5M)")
    print("   - major (fixed field size 156, fixed purse $20M, high prestige)")
    print("   - invitational (random field size 72-90, random purse $12M-$18M)")
    print("   - special (like Continental Championship)")
    
    print("\nExample usage:")
    print("   create_tournament('Sony Open', 'standard')")
    print("   create_tournament('The Sovereign Tournament', 'major')")
    print("   create_tournament('The Memorial', 'invitational')")
    print("   create_tournament('Continental Championship', 'special')")

if __name__ == "__main__":
    main() 