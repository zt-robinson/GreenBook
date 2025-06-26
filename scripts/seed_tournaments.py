import sqlite3
import os
from datetime import datetime, timedelta

def seed_tournaments():
    """Seed the tournaments database with sample tournament data"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'golf_tournaments.db')
    courses_db_path = os.path.join(os.path.dirname(__file__), 'golf_courses.db')
    
    if not os.path.exists(db_path):
        print("❌ Tournament database not found. Please run create_tournaments_db.py first.")
        return
    
    if not os.path.exists(courses_db_path):
        print("❌ Courses database not found. Please ensure golf_courses.db exists.")
        return
    
    # Connect to courses database to get course list
    courses_conn = sqlite3.connect(courses_db_path)
    courses_cur = courses_conn.cursor()
    
    # Get available courses
    courses_cur.execute('SELECT id, name FROM courses ORDER BY name')
    courses = courses_cur.fetchall()
    courses_conn.close()
    
    if not courses:
        print("❌ No courses found. Please ensure golf_courses.db exists and has courses.")
        return
    
    print(f"Found {len(courses)} courses available for tournaments")
    
    # Connect to tournaments database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Full cleanup before seeding
    cur.execute('DELETE FROM tournament_schedule')
    cur.execute('DELETE FROM payout_structure')
    cur.execute('DELETE FROM tournament_fields')
    cur.execute('DELETE FROM tournament_results')
    cur.execute('DELETE FROM tournament_odds')
    cur.execute('DELETE FROM tournaments')
    
    # Tournament templates with realistic data
    tournament_templates = [
        # Regular Tour Events
        {
            'name': 'Sony Open in Hawaii',
            'type': 'regular',
            'field_size': 156,
            'purse': 8500000,
            'prestige': 3.5,
            'payout_structure': [
                (1, 1530000, 18.0, 500), (2, 918000, 10.8, 300), (3, 578000, 6.8, 190),
                (4, 408000, 4.8, 135), (5, 340000, 4.0, 110), (6, 306000, 3.6, 100),
                (7, 285000, 3.4, 90), (8, 264000, 3.1, 85), (9, 247000, 2.9, 80),
                (10, 230000, 2.7, 75)
            ]
        },
        {
            'name': 'The American Express',
            'type': 'regular',
            'field_size': 156,
            'purse': 8900000,
            'prestige': 3.0,
            'payout_structure': [
                (1, 1602000, 18.0, 500), (2, 961200, 10.8, 300), (3, 605200, 6.8, 190),
                (4, 427200, 4.8, 135), (5, 356000, 4.0, 110), (6, 320400, 3.6, 100),
                (7, 298000, 3.4, 90), (8, 275600, 3.1, 85), (9, 258100, 2.9, 80),
                (10, 240600, 2.7, 75)
            ]
        },
        {
            'name': 'Farmers Insurance Open',
            'type': 'regular',
            'field_size': 156,
            'purse': 9200000,
            'prestige': 4.0,
            'payout_structure': [
                (1, 1656000, 18.0, 500), (2, 993600, 10.8, 300), (3, 625600, 6.8, 190),
                (4, 441600, 4.8, 135), (5, 368000, 4.0, 110), (6, 331200, 3.6, 100),
                (7, 308000, 3.4, 90), (8, 285200, 3.1, 85), (9, 266800, 2.9, 80),
                (10, 248400, 2.7, 75)
            ]
        },
        
        # Opens
        {
            'name': 'U.S. Open Championship',
            'type': 'open',
            'field_size': 156,
            'purse': 20000000,
            'prestige': 9.5,
            'payout_structure': [
                (1, 3600000, 18.0, 600), (2, 2160000, 10.8, 330), (3, 1360000, 6.8, 210),
                (4, 960000, 4.8, 150), (5, 800000, 4.0, 120), (6, 720000, 3.6, 110),
                (7, 670000, 3.4, 100), (8, 620000, 3.1, 95), (9, 580000, 2.9, 90),
                (10, 540000, 2.7, 85)
            ]
        },
        {
            'name': 'The Open Championship',
            'type': 'open',
            'field_size': 156,
            'purse': 16000000,
            'prestige': 9.0,
            'payout_structure': [
                (1, 2880000, 18.0, 600), (2, 1728000, 10.8, 330), (3, 1088000, 6.8, 210),
                (4, 768000, 4.8, 150), (5, 640000, 4.0, 120), (6, 576000, 3.6, 110),
                (7, 536000, 3.4, 100), (8, 496000, 3.1, 95), (9, 464000, 2.9, 90),
                (10, 432000, 2.7, 85)
            ]
        },
        
        # Invitationals
        {
            'name': 'The Masters Tournament',
            'type': 'invitational',
            'field_size': 90,
            'purse': 18000000,
            'prestige': 10.0,
            'payout_structure': [
                (1, 3240000, 18.0, 600), (2, 1944000, 10.8, 330), (3, 1224000, 6.8, 210),
                (4, 864000, 4.8, 150), (5, 720000, 4.0, 120), (6, 648000, 3.6, 110),
                (7, 603000, 3.4, 100), (8, 558000, 3.1, 95), (9, 522000, 2.9, 90),
                (10, 486000, 2.7, 85)
            ]
        },
        {
            'name': 'The Memorial Tournament',
            'type': 'invitational',
            'field_size': 78,
            'purse': 12000000,
            'prestige': 6.5,
            'payout_structure': [
                (1, 2160000, 18.0, 550), (2, 1296000, 10.8, 315), (3, 816000, 6.8, 200),
                (4, 576000, 4.8, 140), (5, 480000, 4.0, 115), (6, 432000, 3.6, 105),
                (7, 402000, 3.4, 95), (8, 372000, 3.1, 90), (9, 348000, 2.9, 85),
                (10, 324000, 2.7, 80)
            ]
        },
        
        # Majors
        {
            'name': 'PGA Championship',
            'type': 'major',
            'field_size': 156,
            'purse': 17000000,
            'prestige': 9.0,
            'payout_structure': [
                (1, 3060000, 18.0, 600), (2, 1836000, 10.8, 330), (3, 1156000, 6.8, 210),
                (4, 816000, 4.8, 150), (5, 680000, 4.0, 120), (6, 612000, 3.6, 110),
                (7, 569000, 3.4, 100), (8, 527000, 3.1, 95), (9, 493000, 2.9, 90),
                (10, 459000, 2.7, 85)
            ]
        }
    ]
    
    # Create tournaments for Season 0 (first season)
    season_number = 0
    week_number = 1
    
    # Start on July 4, 2025
    base_date = datetime(2025, 7, 4)
    days_between_events = 2
    
    for idx, template in enumerate(tournament_templates):
        # Select a course (cycling through available courses)
        course_id = courses[week_number % len(courses)][0]
        
        # Insert tournament
        cur.execute('''
            INSERT INTO tournaments (name, tournament_type, course_id, field_size, purse_amount, prestige_level, season_number, week_number, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            template['name'],
            template['type'],
            course_id,
            template['field_size'],
            template['purse'],
            template['prestige'],
            season_number,
            week_number,
            'scheduled'
        ))
        
        tournament_id = cur.lastrowid
        
        # Insert payout structure
        for position, amount, percentage, points in template['payout_structure']:
            cur.execute('''
                INSERT INTO payout_structure (tournament_id, finish_position, payout_amount, payout_percentage, tour_points)
                VALUES (?, ?, ?, ?, ?)
            ''', (tournament_id, position, amount, percentage, points))
        
        # Schedule: each event is 2 days after the previous
        tournament_date = base_date + timedelta(days=(idx * days_between_events))
        
        cur.execute('''
            INSERT INTO tournament_schedule (tournament_id, start_date, start_time, round_1_start, round_2_start, round_3_start, round_4_start)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            tournament_id,
            tournament_date.strftime('%Y-%m-%d'),
            '09:00',
            '09:00',
            '12:30',
            '16:00',
            '19:30'
        ))
        
        print(f"✅ Created tournament: {template['name']} (Event {idx+1} on {tournament_date.strftime('%B %d, %Y')})")
        week_number += 1
    
    conn.commit()
    conn.close()
    
    print(f"\n🎉 Successfully seeded {len(tournament_templates)} tournaments for Season {season_number}")
    print("   -> Tournament database is ready for use!")

if __name__ == "__main__":
    seed_tournaments() 