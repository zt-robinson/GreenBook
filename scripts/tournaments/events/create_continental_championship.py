#!/usr/bin/env python3
"""
Generate the Continental Championship tournament
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta

# Add the greenbook directory to the path so we can import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.tournament_logic import tournament_logic
from core.event_types import event_type_manager

def get_available_courses():
    """Get list of available courses"""
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config import COURSE_DB_PATH as courses_db_path
    
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

def get_last_event_date_and_week(season_number):
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from config import TOURNAMENT_DB_PATH as tournaments_db_path
    if not os.path.exists(tournaments_db_path):
        return None, 0
    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    try:
        cur.execute('SELECT start_date, week_number FROM tournaments WHERE season_number = ? ORDER BY start_date DESC LIMIT 1', (season_number,))
        result = cur.fetchone()
        if result:
            return result[0], result[1]
        else:
            return None, 0
    finally:
        conn.close()

def get_next_event_date_and_week(season_number):
    last_date, last_week = get_last_event_date_and_week(season_number)
    if last_date is None:
        # First event in season - prompt for start date
        while True:
            try:
                start_date = input("Enter start date for this event (YYYY-MM-DD): ").strip()
                datetime.strptime(start_date, '%Y-%m-%d')
                return start_date, 1
            except ValueError:
                print("❌ Please enter a valid date in YYYY-MM-DD format")
            except KeyboardInterrupt:
                print("\n\n❌ Date selection cancelled")
                return None, None
    else:
        last_datetime = datetime.strptime(last_date, '%Y-%m-%d')
        next_datetime = last_datetime + timedelta(days=2)
        next_date = next_datetime.strftime('%Y-%m-%d')
        print(f"📅 Auto-scheduled for {next_date} (2 days after last event)")
        return next_date, last_week + 1

def create_continental_championship(course_id: int, start_date: str, 
                                  season_number: int, week_number: int):
    """Create the Continental Championship tournament"""
    
    tournament_name = "The Continental Championship"
    
    print(f"🌍 Creating Continental Championship: {tournament_name}")
    print("=" * 60)
    
    try:
        # Create the tournament using the tournament logic (no event_type for continental - uses overrides)
        overrides = {
            'field_size': 162,
            'purse_base': 30000000,
            'cut_line': {
                'type': 'position',
                'value': 65,
                'description': 'Top 65 and ties advance to weekend'
            },
            'points_to_winner': 750,
            'prestige': 0.95
        }
        tournament_id = tournament_logic.create_tournament(
            tournament_name=tournament_name,
            course_id=course_id,
            start_date=start_date,
            season_number=season_number,
            week_number=week_number,
            event_type=None,  # Continental Championship uses tournament overrides, not event types
            overrides=overrides
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

def get_available_courses_for_season(season_number):
    courses_db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'golf_courses.db')
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'golf_tournaments.db')
    
    print(f"[DEBUG] courses_db_path: {courses_db_path}")
    print(f"[DEBUG] tournaments_db_path: {tournaments_db_path}")
    print(f"[DEBUG] courses_db_path exists: {os.path.exists(courses_db_path)}")
    print(f"[DEBUG] tournaments_db_path exists: {os.path.exists(tournaments_db_path)}")
    if not os.path.exists(courses_db_path):
        print("❌ Courses database not found.")
        return []
    
    conn = sqlite3.connect(courses_db_path)
    cur = conn.cursor()
    cur.execute('SELECT id, name, state_country, location FROM courses ORDER BY name')
    all_courses = cur.fetchall()
    print(f"[DEBUG] Number of courses found: {len(all_courses)}")
    conn.close()

    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    cur.execute('SELECT course_id FROM tournaments WHERE season_number = ?', (season_number,))
    used_course_ids = set(row[0] for row in cur.fetchall())
    print(f"[DEBUG] used_course_ids: {used_course_ids}")
    conn.close()

    available_courses = [c for c in all_courses if c[0] not in used_course_ids]
    print(f"[DEBUG] Number of available courses: {len(available_courses)}")
    return available_courses

def main():
    """Main function to create the Continental Championship"""
    
    print("\U0001F30D Continental Championship Generator")
    print("=" * 40)
    
    season_number = 1
    # Get available courses for the season (exclude already used)
    courses = get_available_courses_for_season(season_number)
    if not courses:
        print("❌ No courses available for tournaments")
        return
    
    print(f"📋 Found {len(courses)} available courses")
    print("\n📋 Available Courses ({} total):".format(len(courses)))
    print("-" * 60)
    for idx, (cid, cname, state_country, location) in enumerate(courses, 1):
        # Extract country from location for international courses
        if location and ',' in location:
            country = location.split(', ')[-1]  # Get the last part after the last comma
        else:
            country = state_country or 'Unknown'
        print(f" {idx}. {cname} ({country}) (ID: {cid})")
    print("-" * 60)
    while True:
        try:
            course_choice = int(input(f"Select course (1-{len(courses)}): ").strip())
            if 1 <= course_choice <= len(courses):
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(courses)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n❌ Course selection cancelled")
            return
    course_id = courses[course_choice - 1][0]
    course_name = courses[course_choice - 1][1]
    # Extract country for display
    if courses[course_choice - 1][3] and ',' in courses[course_choice - 1][3]:  # location field
        country = courses[course_choice - 1][3].split(', ')[-1]
    else:
        country = courses[course_choice - 1][2] or 'Unknown'  # state_country field
    
    print(f"\n📝 Creating Continental Championship with parameters:")
    print(f"   Name: The Continental Championship")
    print(f"   Course: {course_name} ({country})")
    print(f"   Season: {season_number}")
    print(f"   Description: Special continental championship event")
    
    # Get next event date and week
    start_date, week_number = get_next_event_date_and_week(season_number)
    
    if start_date:
        # Create the Continental Championship as a 'major' with overrides
        overrides = {
            'field_size': 162,
            'purse_base': 30000000,
            'cut_line': {
                'type': 'position',
                'value': 65,
                'description': 'Top 65 and ties advance to weekend'
            },
            'points_to_winner': 750,
            'prestige': 0.95
        }
        tournament_id = tournament_logic.create_tournament(
            tournament_name="The Continental Championship",
            course_id=course_id,
            start_date=start_date,
            season_number=season_number,
            week_number=week_number,
            event_type="major",
            overrides=overrides
        )
        
        if tournament_id:
            print(f"\n🎉 Continental Championship created successfully!")
            print(f"   Tournament ID: {tournament_id}")
            print(f"   Ready to be used in tournament simulation")
            print(f"   This is a special championship event with unique configuration")
        else:
            print(f"\n❌ Failed to create Continental Championship")
    else:
        print(f"\n❌ Date selection cancelled")

if __name__ == "__main__":
    main() 