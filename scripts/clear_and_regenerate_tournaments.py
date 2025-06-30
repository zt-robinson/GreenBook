#!/usr/bin/env python3
"""
Clear all tournaments and regenerate them with the new database columns
"""

import sqlite3
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.tournament_logic import tournament_logic

def clear_all_tournaments():
    """Clear all tournament data from the database"""
    
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_tournaments.db')
    
    if not os.path.exists(tournaments_db_path):
        print("❌ Tournament database not found")
        return False
    
    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    
    try:
        # Clear all tournament-related data
        cur.execute('DELETE FROM tournament_schedule')
        cur.execute('DELETE FROM payout_structure')
        cur.execute('DELETE FROM tournament_fields')
        cur.execute('DELETE FROM tournament_results')
        cur.execute('DELETE FROM tournament_odds')
        cur.execute('DELETE FROM tournaments')
        
        conn.commit()
        print("✅ Cleared all tournament data")
        return True
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error clearing tournaments: {e}")
        return False
    finally:
        conn.close()

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

def regenerate_tournaments():
    """Regenerate all tournaments with the new system"""
    
    print("🎯 Regenerating Tournaments with New Database Columns")
    print("=" * 60)
    
    courses = get_available_courses()
    if not courses:
        print("❌ No courses available for tournaments")
        return False
    
    # Tournament definitions with specific dates
    tournaments = [
        # Standard Events
        {"name": "Sony Open in Hawaii", "event_type": "standard", "date": "2025-07-04"},
        {"name": "The American Express", "event_type": "standard", "date": "2025-07-07"},
        {"name": "Farmers Insurance Open", "event_type": "standard", "date": "2025-07-10"},
        
        # Invitational Events
        {"name": "The Memorial Tournament", "event_type": "invitational", "date": "2025-07-13"},
        {"name": "Arnold Palmer Invitational", "event_type": "invitational", "date": "2025-07-16"},
        
        # Majors (these will use tournament overrides)
        {"name": "The Sovereign Tournament", "event_type": None, "date": "2025-07-19"},
        {"name": "The American Open", "event_type": None, "date": "2025-07-22"},
        {"name": "The Royal Open", "event_type": None, "date": "2025-07-25"},
        {"name": "The AGA Championship", "event_type": None, "date": "2025-07-28"},
        
        # Special Event (Continental Championship)
        {"name": "The Continental Championship", "event_type": None, "date": "2025-08-01"},
    ]
    
    created_tournaments = []
    
    for i, tournament in enumerate(tournaments, 1):
        print(f"\n{i}️⃣ Creating: {tournament['name']}")
        print("-" * 40)
        
        # Cycle through available courses
        course_id = courses[i % len(courses)][0]
        course_name = courses[i % len(courses)][1]
        
        try:
            tournament_id = tournament_logic.create_tournament(
                tournament_name=tournament['name'],
                course_id=course_id,
                start_date=tournament['date'],
                season_number=0,
                week_number=i,
                event_type=tournament['event_type']
            )
            
            if tournament_id:
                created_tournaments.append({
                    'id': tournament_id,
                    'name': tournament['name'],
                    'event_type': tournament['event_type'] or 'auto-determined',
                    'date': tournament['date'],
                    'course': course_name
                })
                print(f"✅ Successfully created {tournament['name']} on {course_name}")
            else:
                print(f"❌ Failed to create {tournament['name']}")
                
        except Exception as e:
            print(f"❌ Error creating {tournament['name']}: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Tournament Regeneration Summary")
    print("=" * 60)
    
    for tournament in created_tournaments:
        print(f"   {tournament['name']} (ID: {tournament['id']}) - {tournament['event_type']} - {tournament['course']}")
    
    print(f"\n✅ Created {len(created_tournaments)} out of {len(tournaments)} tournaments")
    
    if len(created_tournaments) == len(tournaments):
        print("\n🎯 All tournaments created successfully!")
        print("   -> All tournaments now have new database columns populated")
        print("   -> Prestige is on 0-1 scale")
        print("   -> Cut line and points are stored in database")
        print("   -> Event configuration is stored as JSON")
    else:
        print(f"\n⚠️ {len(tournaments) - len(created_tournaments)} tournaments failed to create")
    
    return len(created_tournaments) == len(tournaments)

def main():
    """Main function to clear and regenerate tournaments"""
    
    print("🔄 Tournament Clear and Regenerate")
    print("=" * 50)
    
    # Step 1: Clear all tournaments
    print("\n1️⃣ Clearing all existing tournaments...")
    if not clear_all_tournaments():
        print("❌ Failed to clear tournaments. Aborting.")
        return
    
    # Step 2: Regenerate tournaments
    print("\n2️⃣ Regenerating tournaments with new system...")
    success = regenerate_tournaments()
    
    if success:
        print("\n✅ Tournament regeneration complete!")
        print("   -> Run 'python3 check_tournament_details.py' to verify")
        print("   -> Start the web app to see the updated display")
    else:
        print("\n❌ Tournament regeneration failed")

if __name__ == "__main__":
    main() 