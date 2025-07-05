#!/usr/bin/env python3
"""
Comprehensive Data Deletion Tool
Allows deletion of single or all courses, players, and tournaments with confirmation.
"""

import sqlite3
import os
import sys

# Database paths
COURSE_DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_courses.db')
PLAYER_DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_players.db')
TOURNAMENT_DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_tournaments.db')

def get_course_list():
    """Get list of all courses with IDs"""
    conn = sqlite3.connect(COURSE_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, city, state_country FROM courses ORDER BY id")
    courses = cursor.fetchall()
    conn.close()
    return courses

def get_player_list():
    """Get list of all players with IDs"""
    conn = sqlite3.connect(PLAYER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, country FROM players ORDER BY id")
    players = cursor.fetchall()
    conn.close()
    return players

def get_tournament_list():
    """Get list of all tournaments with IDs"""
    conn = sqlite3.connect(TOURNAMENT_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, course_id FROM tournaments ORDER BY id")
    tournaments = cursor.fetchall()
    conn.close()
    return tournaments

def delete_single_course(course_id):
    """Delete a single course and all related data"""
    conn = sqlite3.connect(COURSE_DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get course name for confirmation
        cursor.execute("SELECT name FROM courses WHERE id = ?", (course_id,))
        course = cursor.fetchone()
        if not course:
            print(f"❌ Course with ID {course_id} not found.")
            return False
        
        course_name = course[0]
        print(f"🗑️  Deleting course: {course_name} (ID: {course_id})")
        
        # Delete related data
        cursor.execute("DELETE FROM holes WHERE course_id = ?", (course_id,))
        cursor.execute("DELETE FROM course_characteristics WHERE course_id = ?", (course_id,))
        cursor.execute("DELETE FROM courses WHERE id = ?", (course_id,))
        
        conn.commit()
        print(f"✅ Successfully deleted course: {course_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error deleting course: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_all_courses():
    """Delete all courses and reset counters"""
    conn = sqlite3.connect(COURSE_DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get count
        cursor.execute("SELECT COUNT(*) FROM courses")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("✅ No courses to delete.")
            return True
        
        print(f"🗑️  Deleting {count} courses and all related data...")
        
        # Delete all data
        cursor.execute("DELETE FROM holes")
        cursor.execute("DELETE FROM course_characteristics")
        cursor.execute("DELETE FROM courses")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='courses'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='course_characteristics'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='holes'")
        
        conn.commit()
        print(f"✅ Successfully deleted {count} courses. Counters reset.")
        return True
        
    except Exception as e:
        print(f"❌ Error deleting courses: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_single_player(player_id):
    """Delete a single player"""
    conn = sqlite3.connect(PLAYER_DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Get player name for confirmation
        cursor.execute("SELECT name FROM players WHERE id = ?", (player_id,))
        player = cursor.fetchone()
        if not player:
            print(f"❌ Player with ID {player_id} not found.")
            return False
        
        player_name = player[0]
        print(f"🗑️  Deleting player: {player_name} (ID: {player_id})")
        
        cursor.execute("DELETE FROM players WHERE id = ?", (player_id,))
        conn.commit()
        print(f"✅ Successfully deleted player: {player_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error deleting player: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_all_players():
    """Delete all players and reset counter"""
    conn = sqlite3.connect(PLAYER_DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM players")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("✅ No players to delete.")
            return True
        
        print(f"🗑️  Deleting {count} players...")
        
        cursor.execute("DELETE FROM players")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='players'")
        
        conn.commit()
        print(f"✅ Successfully deleted {count} players. Counter reset.")
        return True
        
    except Exception as e:
        print(f"❌ Error deleting players: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_single_tournament(tournament_id):
    """Delete a single tournament"""
    conn = sqlite3.connect(TOURNAMENT_DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT name FROM tournaments WHERE id = ?", (tournament_id,))
        tournament = cursor.fetchone()
        if not tournament:
            print(f"❌ Tournament with ID {tournament_id} not found.")
            return False
        
        tournament_name = tournament[0]
        print(f"🗑️  Deleting tournament: {tournament_name} (ID: {tournament_id})")
        
        cursor.execute("DELETE FROM tournaments WHERE id = ?", (tournament_id,))
        conn.commit()
        print(f"✅ Successfully deleted tournament: {tournament_name}")
        return True
        
    except Exception as e:
        print(f"❌ Error deleting tournament: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_all_tournaments():
    """Delete all tournaments and reset counter"""
    conn = sqlite3.connect(TOURNAMENT_DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM tournaments")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("✅ No tournaments to delete.")
            return True
        
        print(f"🗑️  Deleting {count} tournaments...")
        
        cursor.execute("DELETE FROM tournaments")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='tournaments'")
        
        conn.commit()
        print(f"✅ Successfully deleted {count} tournaments. Counter reset.")
        return True
        
    except Exception as e:
        print(f"❌ Error deleting tournaments: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def show_menu():
    """Show the main menu"""
    print("\n🗑️  Data Deletion Tool")
    print("=" * 50)
    print("1. Delete a single course")
    print("2. Delete all courses")
    print("3. Delete a single player")
    print("4. Delete all players")
    print("5. Delete a single tournament")
    print("6. Delete all tournaments")
    print("7. Exit")
    print("=" * 50)

def handle_course_deletion():
    """Handle course deletion options"""
    courses = get_course_list()
    
    if not courses:
        print("✅ No courses found.")
        return
    
    print("\n📋 Available courses:")
    for course_id, name, city, state in courses:
        print(f"  {course_id}: {name} ({city}, {state})")
    
    try:
        choice = input("\nEnter course ID to delete (or 'all' for all courses): ").strip()
        
        if choice.lower() == 'all':
            confirm = input("⚠️  Are you sure you want to delete ALL courses? (y/N): ")
            if confirm.lower() in ['y', 'yes']:
                delete_all_courses()
            else:
                print("❌ Operation cancelled.")
        else:
            course_id = int(choice)
            confirm = input(f"⚠️  Are you sure you want to delete course ID {course_id}? (y/N): ")
            if confirm.lower() in ['y', 'yes']:
                delete_single_course(course_id)
            else:
                print("❌ Operation cancelled.")
                
    except ValueError:
        print("❌ Invalid input. Please enter a number or 'all'.")
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")

def handle_player_deletion():
    """Handle player deletion options"""
    players = get_player_list()
    
    if not players:
        print("✅ No players found.")
        return
    
    print("\n📋 Available players:")
    for player_id, name, country in players:
        print(f"  {player_id}: {name} ({country})")
    
    try:
        choice = input("\nEnter player ID to delete (or 'all' for all players): ").strip()
        
        if choice.lower() == 'all':
            confirm = input("⚠️  Are you sure you want to delete ALL players? (y/N): ")
            if confirm.lower() in ['y', 'yes']:
                delete_all_players()
            else:
                print("❌ Operation cancelled.")
        else:
            player_id = int(choice)
            confirm = input(f"⚠️  Are you sure you want to delete player ID {player_id}? (y/N): ")
            if confirm.lower() in ['y', 'yes']:
                delete_single_player(player_id)
            else:
                print("❌ Operation cancelled.")
                
    except ValueError:
        print("❌ Invalid input. Please enter a number or 'all'.")
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")

def handle_tournament_deletion():
    """Handle tournament deletion options"""
    tournaments = get_tournament_list()
    
    if not tournaments:
        print("✅ No tournaments found.")
        return
    
    print("\n📋 Available tournaments:")
    for tournament_id, name, course_id in tournaments:
        print(f"  {tournament_id}: {name} (Course ID: {course_id})")
    
    try:
        choice = input("\nEnter tournament ID to delete (or 'all' for all tournaments): ").strip()
        
        if choice.lower() == 'all':
            confirm = input("⚠️  Are you sure you want to delete ALL tournaments? (y/N): ")
            if confirm.lower() in ['y', 'yes']:
                delete_all_tournaments()
            else:
                print("❌ Operation cancelled.")
        else:
            tournament_id = int(choice)
            confirm = input(f"⚠️  Are you sure you want to delete tournament ID {tournament_id}? (y/N): ")
            if confirm.lower() in ['y', 'yes']:
                delete_single_tournament(tournament_id)
            else:
                print("❌ Operation cancelled.")
                
    except ValueError:
        print("❌ Invalid input. Please enter a number or 'all'.")
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled.")

def main():
    """Main function"""
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                handle_course_deletion()
            elif choice == '2':
                confirm = input("⚠️  Are you sure you want to delete ALL courses? (y/N): ")
                if confirm.lower() in ['y', 'yes']:
                    delete_all_courses()
                else:
                    print("❌ Operation cancelled.")
            elif choice == '3':
                handle_player_deletion()
            elif choice == '4':
                confirm = input("⚠️  Are you sure you want to delete ALL players? (y/N): ")
                if confirm.lower() in ['y', 'yes']:
                    delete_all_players()
                else:
                    print("❌ Operation cancelled.")
            elif choice == '5':
                handle_tournament_deletion()
            elif choice == '6':
                confirm = input("⚠️  Are you sure you want to delete ALL tournaments? (y/N): ")
                if confirm.lower() in ['y', 'yes']:
                    delete_all_tournaments()
                else:
                    print("❌ Operation cancelled.")
            elif choice == '7':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-7.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 