#!/usr/bin/env python3
"""
Generate all four major championships
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.tournament_logic import tournament_logic
from core.event_types import event_type_manager

def get_available_courses_for_season(season_number, used_course_ids, uk_only=False, us_only=False):
    courses_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_tournaments.db')

    conn = sqlite3.connect(courses_db_path)
    cur = conn.cursor()
    if uk_only:
        cur.execute("SELECT id, name, state_country FROM courses WHERE state_country LIKE '%UK%' OR location LIKE '%UK%' ORDER BY name")
    elif us_only:
        cur.execute("SELECT id, name, state_country FROM courses WHERE state_country LIKE '%US%' OR state_country LIKE '%USA%' OR location LIKE '%US%' OR location LIKE '%USA%' ORDER BY name")
    else:
        cur.execute('SELECT id, name, state_country FROM courses ORDER BY name')
    all_courses = cur.fetchall()
    conn.close()

    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    cur.execute('SELECT course_id FROM tournaments WHERE season_number = ?', (season_number,))
    db_used_course_ids = set(row[0] for row in cur.fetchall())
    conn.close()

    all_used = db_used_course_ids.union(used_course_ids)
    return [c for c in all_courses if c[0] not in all_used]

def select_course(courses, major_name):
    print(f"\n📋 Available Courses for {major_name} ({len(courses)} total):")
    print("-" * 60)
    for idx, (course_id, course_name, state_country) in enumerate(courses, 1):
        print(f"{idx:2d}. {course_name} ({state_country}) (ID: {course_id})")
    print("-" * 60)
    while True:
        try:
            choice = input(f"Select course for {major_name} (1-{len(courses)}): ").strip()
            course_index = int(choice) - 1
            if 0 <= course_index < len(courses):
                selected_course = courses[course_index]
                print(f"\n✅ Selected: {selected_course[1]} ({selected_course[2]}) (ID: {selected_course[0]})")
                return selected_course
            else:
                print(f"❌ Please enter a number between 1 and {len(courses)})")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n❌ Course selection cancelled")
            return None

def create_major(tournament_name: str, course_id: int, start_date: str, season_number: int, week_number: int):
    print(f"🏆 Creating Major: {tournament_name}")
    print("=" * 50)
    try:
        # Use override logic for The Sovereign Tournament
        if tournament_name == "The Sovereign Tournament":
            import random
            field_size = random.choice([x for x in range(90, 115) if x % 3 == 0])
            purse = random.randrange(21000000, 25000001, 1000000)
            prestige = 1.0
            cut_line_type = "position"
            cut_line_value = 53
            event_type = "major"
            # Points to winner from override config (default 1000 if not found)
            config = event_type_manager.get_tournament_config(tournament_name)
            points_to_winner = config.get('points_structure', {}).get('winner', 1000)
            # Compose overrides
            overrides = {
                'field_size': field_size,
                'purse_base': purse,
                'prestige': prestige,
                'cut_line_type': cut_line_type,
                'cut_line_value': cut_line_value,
                'event_type': event_type,
                'points_to_winner': points_to_winner
            }
            tournament_id = tournament_logic.create_tournament(
                tournament_name=tournament_name,
                course_id=course_id,
                start_date=start_date,
                season_number=season_number,
                week_number=week_number,
                event_type=event_type,
                overrides=overrides
            )
        else:
            # Use config/override for other majors
            tournament_id = tournament_logic.create_tournament(
                tournament_name=tournament_name,
                course_id=course_id,
                start_date=start_date,
                season_number=season_number,
                week_number=week_number,
                event_type="major"
            )
        print(f"\n✅ Major '{tournament_name}' created successfully!")
        print(f"   Tournament ID: {tournament_id}")
        print(f"   Event Type: major")
        print(f"   Course ID: {course_id}")
        print(f"   Start Date: {start_date}")
        print(f"   Season: {season_number}, Week: {week_number}")
        return tournament_id
    except Exception as e:
        print(f"❌ Error creating major: {e}")
        return None

def create_all_majors():
    print("🏆 Major Championships Generator")
    print("=" * 40)
    majors = [
        {"name": "The Sovereign Tournament"},
        {"name": "The American Open"},
        {"name": "The Royal Open"},
        {"name": "The AGA Championship"}
    ]
    base_date = datetime(2025, 7, 1)
    season_number = 1
    days_between_majors = 7
    created_majors = []
    used_course_ids = set()
    for idx, major in enumerate(majors):
        major_date = base_date + timedelta(days=(idx * days_between_majors))
        week_number = idx + 1
        # Get available courses for this season (exclude already used)
        uk_only = (major['name'] == "The Royal Open")
        us_only = (major['name'] in ["The American Open", "The AGA Championship"])
        available_courses = get_available_courses_for_season(season_number, used_course_ids, uk_only=uk_only, us_only=us_only)
        if not available_courses:
            print(f"❌ No available courses left for {major['name']} in season {season_number}")
            break
        selected_course = select_course(available_courses, major['name'])
        if not selected_course:
            break
        course_id, course_name, state_country = selected_course
        used_course_ids.add(course_id)
        print(f"\n🎯 Creating Major #{idx + 1}: {major['name']}")
        print(f"   Date: {major_date.strftime('%B %d, %Y')}")
        print(f"   Course: {course_name} ({state_country})")
        print(f"   Week: {week_number}")
        tournament_id = create_major(
            tournament_name=major['name'],
            course_id=course_id,
            start_date=major_date.strftime('%Y-%m-%d'),
            season_number=season_number,
            week_number=week_number
        )
        if tournament_id:
            created_majors.append({
                'id': tournament_id,
                'name': major['name'],
                'date': major_date.strftime('%Y-%m-%d'),
                'course': course_name,
                'week': week_number
            })
        else:
            print(f"❌ Failed to create major: {major['name']}")
    return created_majors

def main():
    created_majors = create_all_majors()
    if created_majors:
        print(f"\n🎉 Successfully created {len(created_majors)} major championships!")
        print("\n📋 Created Majors:")
        for major in created_majors:
            print(f"   • {major['name']} (Week {major['week']}, {major['date']})")
        print(f"\n✅ All majors are ready for tournament simulation")
    else:
        print(f"\n❌ Failed to create any major championships")

if __name__ == "__main__":
    main() 