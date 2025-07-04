#!/usr/bin/env python3
"""
Create and store The AGA Championship major
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
import random

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.tournament_logic import tournament_logic
from core.event_types import event_type_manager

def get_last_event_date_and_week(season_number):
    """Get the start date of the last event in the season and its week number"""
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_tournaments.db')
    
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
    """Get the next event date and week number - either prompt user or auto-schedule 2 days after last event"""
    last_date, last_week = get_last_event_date_and_week(season_number)
    
    if last_date is None:
        # First event in season - prompt for start date
        while True:
            try:
                start_date = input("Enter start date for this event (YYYY-MM-DD): ").strip()
                # Basic validation
                datetime.strptime(start_date, '%Y-%m-%d')
                return start_date, 1
            except ValueError:
                print("❌ Please enter a valid date in YYYY-MM-DD format")
            except KeyboardInterrupt:
                print("\n\n❌ Date selection cancelled")
                return None, None
    else:
        # Subsequent event - auto-schedule 2 days after last event
        last_datetime = datetime.strptime(last_date, '%Y-%m-%d')
        next_datetime = last_datetime + timedelta(days=2)
        next_date = next_datetime.strftime('%Y-%m-%d')
        print(f"📅 Auto-scheduled for {next_date} (2 days after last event)")
        return next_date, last_week + 1

def get_available_courses_for_season(season_number):
    """Get list of available US courses for the season (exclude already used)"""
    courses_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_tournaments.db')
    
    if not os.path.exists(courses_db_path):
        print("❌ Courses database not found.")
        return []
    
    conn = sqlite3.connect(courses_db_path)
    cur = conn.cursor()
    # Only US courses for The AGA Championship
    cur.execute("SELECT id, name, state_country FROM courses WHERE state_country LIKE '%US%' OR state_country LIKE '%USA%' OR location LIKE '%US%' OR location LIKE '%USA%' ORDER BY name")
    all_courses = cur.fetchall()
    conn.close()

    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    cur.execute('SELECT course_id FROM tournaments WHERE season_number = ?', (season_number,))
    used_course_ids = set(row[0] for row in cur.fetchall())
    conn.close()

    return [c for c in all_courses if c[0] not in used_course_ids]

def select_course(courses):
    """Let user select a course from the available options"""
    print(f"\n📋 Available US Courses ({len(courses)} total):")
    print("-" * 60)
    
    for idx, (course_id, course_name, state_country) in enumerate(courses, 1):
        print(f"{idx:2d}. {course_name} ({state_country}) (ID: {course_id})")
    
    print("-" * 60)
    
    while True:
        try:
            choice = input(f"Select course (1-{len(courses)}): ").strip()
            course_index = int(choice) - 1
            
            if 0 <= course_index < len(courses):
                selected_course = courses[course_index]
                print(f"\n✅ Selected: {selected_course[1]} ({selected_course[2]}) (ID: {selected_course[0]})")
                return selected_course
            else:
                print(f"❌ Please enter a number between 1 and {len(courses)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n❌ Course selection cancelled")
            return None

def create_aga_championship(course_id: int, start_date: str, season_number: int, week_number: int):
    """Create The AGA Championship major"""
    
    print(f"🎯 Creating The AGA Championship")
    print("=" * 50)
    
    try:
        # Generate random purse ($21M–$25M, rounded to $1M)
        purse_base = random.choice([x for x in range(21000000, 25000001, 1000000)])
        overrides = {
            'field_size': 156,
            'cut_line': {
                'type': 'position',
                'value': 70,
                'description': 'Top 70 and ties advance to weekend'
            },
            'purse_base': purse_base,
            'prestige': 1.0,
            'points_to_winner': 750
        }
        tournament_id = tournament_logic.create_tournament(
            tournament_name="The AGA Championship",
            course_id=course_id,
            start_date=start_date,
            season_number=season_number,
            week_number=week_number,
            event_type="major",
            overrides=overrides
        )
        
        print(f"\n✅ The AGA Championship created successfully!")
        print(f"   Tournament ID: {tournament_id}")
        print(f"   Event Type: major")
        print(f"   Course ID: {course_id}")
        print(f"   Start Date: {start_date}")
        print(f"   Season: {season_number}, Week: {week_number}")
        
        return tournament_id
        
    except Exception as e:
        print(f"❌ Error creating The AGA Championship: {e}")
        return None

def main():
    """Main function to create The AGA Championship"""
    
    print("🏆 The AGA Championship Creator")
    print("=" * 40)
    
    # Get season number from user
    while True:
        try:
            season_number = int(input("Enter season number: ").strip())
            break
        except ValueError:
            print("❌ Please enter a valid season number")
        except KeyboardInterrupt:
            print("\n\n❌ Season selection cancelled")
            return
    
    # Get available courses for this season (exclude already used)
    courses = get_available_courses_for_season(season_number)
    if not courses:
        print(f"❌ No available US courses left for season {season_number}")
        return
    
    print(f"📋 Found {len(courses)} available US courses for season {season_number}")
    
    # Let user select a course
    selected_course = select_course(courses)
    if not selected_course:
        return
    
    course_id, course_name, state_country = selected_course
    
    # Get the next event date and week
    start_date, week_number = get_next_event_date_and_week(season_number)
    if start_date is None:
        return
    
    print(f"\n📝 Creating The AGA Championship with parameters:")
    print(f"   Name: The AGA Championship")
    print(f"   Course: {course_name} ({state_country})")
    print(f"   Date: {start_date}")
    print(f"   Season: {season_number}, Week: {week_number}")
    
    # Create the major
    tournament_id = create_aga_championship(
        course_id=course_id,
        start_date=start_date,
        season_number=season_number,
        week_number=week_number
    )
    
    if tournament_id:
        print(f"\n🎉 The AGA Championship created successfully!")
        print(f"   Ready to be used in tournament simulation")
    else:
        print(f"\n❌ Failed to create The AGA Championship")

if __name__ == "__main__":
    main() 