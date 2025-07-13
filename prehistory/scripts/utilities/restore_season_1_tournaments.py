#!/usr/bin/env python3
"""
Restore Season 1 Tournaments Script for GreenBook Prehistory

This script restores Season 1 tournament data from the corrected CSV files.
"""

import sqlite3
import csv
import os
from pathlib import Path

def get_player_id_by_name(conn, player_name):
    """Get player ID by name from the database"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE name = ?", (player_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def restore_season_1_tournaments():
    """Restore Season 1 tournaments from corrected CSV data"""
    db_path = Path("data/prehistory.db")
    csv_path = Path("reports/regular_seasons/season_1/season_1_event_leaderboard.csv")
    
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return False
    
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        return False
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # First, remove any existing Season 1 tournaments to avoid duplicates
        cursor.execute("DELETE FROM tournament_results WHERE tournament_id IN (SELECT id FROM tournaments WHERE season_number = 1)")
        cursor.execute("DELETE FROM tournaments WHERE season_number = 1")
        print("Removed any existing Season 1 tournaments")
        
        # Read CSV data
        print("Reading corrected Season 1 event data from CSV...")
        tournaments_created = 0
        results_created = 0
        
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                season_event = row['season_event']
                event_type = row['event_type']
                event_name = row['event_name']
                
                # Extract event number from season_event (format: "1_X")
                event_number = int(season_event.split('_')[1])
                
                # Create tournament
                cursor.execute("""
                    INSERT INTO tournaments (season_number, event_number, name, field_size, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (1, event_number, event_name, 150, 'completed'))
                tournament_id = cursor.lastrowid
                tournaments_created += 1
                
                # Create tournament results for all 150 players
                for position in range(1, 151):
                    player_name = row[str(position)]
                    if player_name:  # Skip empty positions
                        player_id = get_player_id_by_name(conn, player_name)
                        if player_id:
                            # Calculate points (151 - position)
                            points = 151 - position
                            # Use position as total_score (simplified)
                            total_score = position
                            
                            cursor.execute("""
                                INSERT INTO tournament_results (tournament_id, player_id, position, total_score, points_earned)
                                VALUES (?, ?, ?, ?, ?)
                            """, (tournament_id, player_id, position, total_score, points))
                            results_created += 1
                
                print(f"Created tournament {event_number}: {event_name}")
        
        conn.commit()
        print(f"\n✅ Successfully restored Season 1 data:")
        print(f"   Tournaments created: {tournaments_created}")
        print(f"   Results created: {results_created}")
        
        # Verify the results
        cursor.execute("SELECT COUNT(*) FROM tournaments WHERE season_number = 1")
        total_tournaments = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM tournament_results WHERE tournament_id IN (SELECT id FROM tournaments WHERE season_number = 1)")
        total_results = cursor.fetchone()[0]
        print(f"   Total Season 1 tournaments in database: {total_tournaments}")
        print(f"   Total Season 1 results in database: {total_results}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error restoring tournaments: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = restore_season_1_tournaments()
    if success:
        print("\n🎉 Season 1 tournaments restoration complete!")
    else:
        print("\n❌ Failed to restore Season 1 tournaments!") 