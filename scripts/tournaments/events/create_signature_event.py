#!/usr/bin/env python3
"""
Create and store a single signature event
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta

# Add the greenbook directory to the path so we can import from core
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from core.tournament_logic import tournament_logic
from core.event_types import event_type_manager
from core.tournament_naming import generate_signature_event_name

def get_current_season_number():
    """Get the current season number - either the highest existing season or the next season if current is empty"""
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'golf_tournaments.db')
    
    if not os.path.exists(tournaments_db_path):
        # If no tournaments database exists, start with season 1
        return 1
    
    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    
    try:
        # Get the highest season number from existing tournaments
        cur.execute('SELECT MAX(season_number) FROM tournaments')
        result = cur.fetchone()
        
        if result[0] is None:
            # No tournaments exist, start with season 1
            return 1
        else:
            # Check if there are any tournaments in the current season
            cur.execute('SELECT COUNT(*) FROM tournaments WHERE season_number = ?', (result[0],))
            count = cur.fetchone()[0]
            
            if count > 0:
                # Use the current season if it has tournaments
                return result[0]
            else:
                # Use the next season if current is empty
                return result[0] + 1
    finally:
        conn.close()

def get_available_courses_for_season(season_number):
    """Get list of available courses for the season (exclude already used)"""
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
    cur.execute('SELECT id, name, state_country FROM courses ORDER BY name')
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

def select_course(courses):
    """Let user select a course from the available options"""
    print(f"\n📋 Available Courses ({len(courses)} total):")
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

def create_signature_event(tournament_name: str, course_id: int, start_date: str, 
                          season_number: int, week_number: int):
    """Create a single signature event"""
    
    print(f"🏆 Creating Signature Event: {tournament_name}")
    print("=" * 50)
    
    try:
        # Create the tournament using the tournament logic with signature event overrides
        overrides = {
            'field_size': 72,  # Fixed field size for signature events
            'cut_line': {
                'type': 'none',
                'value': None,
                'description': 'No cut - all players play all rounds'
            },
            'points_to_winner': 700  # Signature events award 700 points to winner
        }
        
        tournament_id = tournament_logic.create_tournament(
            tournament_name=tournament_name,
            course_id=course_id,
            start_date=start_date,
            season_number=season_number,
            week_number=week_number,
            event_type="signature",
            overrides=overrides
        )
        
        print(f"\n✅ Signature event '{tournament_name}' created successfully!")
        print(f"   Tournament ID: {tournament_id}")
        print(f"   Event Type: signature")
        print(f"   Course ID: {course_id}")
        print(f"   Start Date: {start_date}")
        print(f"   Season: {season_number}, Week: {week_number}")
        print(f"   Field Size: 72 players (fixed)")
        print(f"   Cut Line: No cut - all players play all rounds")
        print(f"   Winner Points: 700")
        
        return tournament_id
        
    except Exception as e:
        print(f"❌ Error creating signature event: {e}")
        return None

def get_tournament_name():
    """Get tournament name from user with confirmation"""
    while True:
        tournament_name = input("Enter tournament name: ").strip()
        if not tournament_name:
            print("❌ Tournament name cannot be empty")
            continue
            
        print(f"\n📋 Tournament Preview:")
        print(f"   Name: {tournament_name}")
        print(f"   Type: Signature Event")
        print(f"   Field Size: 72 players (fixed)")
        print(f"   Cut Line: No cut - all players play all rounds")
        print(f"   Winner Points: 700")
        print(f"   Purse: $18M-$20M (random)")
        
        confirm = input("\nConfirm this tournament? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            return tournament_name
        elif confirm in ['n', 'no']:
            print("🔄 Let's try again...")
            continue
        else:
            print("❌ Please enter 'y' or 'n'")

def main():
    """Main function to create a signature event"""
    
    print("🏆 Signature Event Creator")
    print("=" * 30)
    
    # Get tournament name from user
    tournament_name = get_tournament_name()
    if not tournament_name:
        return
    
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
        print(f"❌ No available courses left for season {season_number}")
        return
    
    print(f"📋 Found {len(courses)} available courses for season {season_number}")
    
    # Let user select a course
    selected_course = select_course(courses)
    if not selected_course:
        return
    
    course_id, course_name, state_country = selected_course
    
    # Get the next event date and week
    start_date, week_number = get_next_event_date_and_week(season_number)
    if start_date is None:
        return
    
    print(f"\n📝 Creating signature event with parameters:")
    print(f"   Name: {tournament_name}")
    print(f"   Course: {course_name} ({state_country})")
    print(f"   Date: {start_date}")
    print(f"   Season: {season_number}, Week: {week_number}")
    print(f"   Field Size: 72 players (fixed)")
    print(f"   Cut Line: No cut - all players play all rounds")
    print(f"   Winner Points: 700")
    print(f"   Purse: $18M-$20M (random)")
    
    # Create the signature event
    tournament_id = create_signature_event(
        tournament_name=tournament_name,
        course_id=course_id,
        start_date=start_date,
        season_number=season_number,
        week_number=week_number
    )
    
    if tournament_id:
        print(f"\n🎉 Signature event created successfully!")
        print(f"   Ready to be used in tournament simulation")
        print(f"   This is a premium signature event with enhanced rewards")
    else:
        print(f"\n❌ Failed to create signature event")

if __name__ == "__main__":
    main() 