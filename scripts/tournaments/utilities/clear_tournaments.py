#!/usr/bin/env python3
"""
Clear all existing tournaments and related data
"""

import sqlite3
import os
import sys

def clear_all_tournaments():
    """Clear all existing tournaments and related data"""
    
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'golf_tournaments.db')
    
    if not os.path.exists(tournaments_db_path):
        print("❌ Tournament database not found. Please run create_tournaments_db.py first.")
        return False
    
    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    
    try:
        print("🗑️ Clearing all existing tournament data...")
        
        # Clear all related tables in the correct order
        cur.execute('DELETE FROM tournament_odds')
        print("   ✅ Cleared tournament_odds")
        
        cur.execute('DELETE FROM tournament_results')
        print("   ✅ Cleared tournament_results")
        
        cur.execute('DELETE FROM tournament_fields')
        print("   ✅ Cleared tournament_fields")
        
        cur.execute('DELETE FROM payout_structure')
        print("   ✅ Cleared payout_structure")
        
        cur.execute('DELETE FROM tournament_schedule')
        print("   ✅ Cleared tournament_schedule")
        
        cur.execute('DELETE FROM tournaments')
        print("   ✅ Cleared tournaments")
        
        conn.commit()
        print("\n✅ All tournament data cleared successfully!")
        print("   -> Ready to generate new tournaments one by one")
        return True
        
    except Exception as e:
        print(f"❌ Error clearing tournaments: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def list_tournaments():
    """List all tournaments with ID, name, date, and course name (from golf_courses.db)."""
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'golf_tournaments.db')
    courses_db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'golf_courses.db')
    if not os.path.exists(tournaments_db_path):
        print("❌ Tournament database not found.")
        return []
    # Build course_id to name mapping
    course_map = {}
    if os.path.exists(courses_db_path):
        conn_courses = sqlite3.connect(courses_db_path)
        cur_courses = conn_courses.cursor()
        try:
            cur_courses.execute('SELECT id, name FROM courses')
            for cid, cname in cur_courses.fetchall():
                course_map[cid] = cname
        finally:
            conn_courses.close()
    # Fetch tournaments
    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT id, name, start_date, course_id FROM tournaments ORDER BY start_date, name
        ''')
        tournaments = []
        for tid, tname, tdate, course_id in cur.fetchall():
            course_name = course_map.get(course_id, 'Unknown')
            tournaments.append((tid, tname, tdate, course_name))
        return tournaments
    finally:
        conn.close()

def table_exists(conn, table_name):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cur.fetchone() is not None

def delete_tournament_by_id(tournament_id):
    """Delete a single tournament and all related data by ID."""
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'golf_tournaments.db')
    conn = sqlite3.connect(tournaments_db_path)
    cur = conn.cursor()
    try:
        # Only delete from tables that exist
        for table, col in [
            ("tournament_schedule", "tournament_id"),
            ("payout_structure", "tournament_id"),
            ("tournament_fields", "tournament_id"),
            ("tournament_results", "tournament_id"),
            ("tournament_odds", "tournament_id")
        ]:
            if table_exists(conn, table):
                cur.execute(f'DELETE FROM {table} WHERE {col} = ?', (tournament_id,))
        cur.execute('DELETE FROM tournaments WHERE id = ?', (tournament_id,))
        conn.commit()
        print(f"\n✅ Tournament ID {tournament_id} and all related data deleted.")
    except Exception as e:
        print(f"❌ Error deleting tournament: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    print("🎯 Tournament Clearer (Selective)")
    print("=" * 30)
    while True:
        tournaments = list_tournaments()
        if not tournaments:
            print("No tournaments found. Exiting.")
            return
        print("\nAvailable tournaments:")
        print(f"{'ID':<4} {'Name':<30} {'Date':<12} {'Course':<20}")
        print("-" * 70)
        for tid, name, date, course in tournaments:
            print(f"{tid:<4} {name:<30} {date or 'N/A':<12} {course or 'N/A':<20}")
        print("\nType the ID of the tournament to delete, 'all' to delete all tournaments, or 'exit' to quit.")
        choice = input("Enter tournament ID, 'all', or 'exit': ").strip().lower()
        if choice == 'exit':
            print("Exiting without deleting any more tournaments.")
            return
        elif choice == 'all':
            confirm = input("Type 'confirm' to delete ALL tournaments: ").strip().lower()
            if confirm == 'confirm':
                if clear_all_tournaments():
                    print("\n🎉 All tournaments deleted. Exiting.")
                else:
                    print("\n❌ Failed to clear tournaments.")
                return
            else:
                print("Aborted. No tournaments deleted.")
        else:
            try:
                tid = int(choice)
                confirm = input(f"Type 'confirm' to delete tournament ID {tid}: ").strip().lower()
                if confirm == 'confirm':
                    delete_tournament_by_id(tid)
                else:
                    print("Aborted. No tournaments deleted.")
            except ValueError:
                print("Invalid input. Aborted.")

if __name__ == "__main__":
    main() 