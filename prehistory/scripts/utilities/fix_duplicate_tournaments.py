#!/usr/bin/env python3
"""
Fix Duplicate Tournaments Script for GreenBook Prehistory

This script removes duplicate tournament records and fixes the database.
"""

import sqlite3
import os
from datetime import datetime

def fix_duplicate_tournaments():
    """Remove duplicate tournament records and clean up the database"""
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
    print("🔧 FIXING DUPLICATE TOURNAMENTS")
    print("=" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current state
        cursor.execute("SELECT COUNT(*) FROM tournaments WHERE season_number = 1")
        total_season_1_tournaments = cursor.fetchone()[0]
        print(f"📊 Current Season 1 tournaments: {total_season_1_tournaments}")
        
        # Get unique events
        cursor.execute("""
            SELECT season_number, event_number, COUNT(*) 
            FROM tournaments 
            WHERE season_number = 1 
            GROUP BY season_number, event_number 
            ORDER BY event_number
        """)
        event_counts = cursor.fetchall()
        
        print(f"📋 Season 1 events: {len(event_counts)}")
        print("Event breakdown:")
        for season, event, count in event_counts:
            print(f"  Event {event}: {count} records")
        
        # Find tournaments to keep (keep the first one for each event)
        cursor.execute("""
            SELECT MIN(id) as keep_id, season_number, event_number
            FROM tournaments 
            WHERE season_number = 1 
            GROUP BY season_number, event_number
        """)
        tournaments_to_keep = {row[0] for row in cursor.fetchall()}
        
        # Find tournaments to delete
        cursor.execute("SELECT id FROM tournaments WHERE season_number = 1")
        all_season_1_ids = {row[0] for row in cursor.fetchall()}
        tournaments_to_delete = all_season_1_ids - tournaments_to_keep
        
        print(f"\n🗑️  About to delete {len(tournaments_to_delete)} duplicate tournament records")
        print(f"📊 Will keep {len(tournaments_to_keep)} unique tournament records")
        
        # Delete duplicate tournaments
        if tournaments_to_delete:
            placeholders = ','.join(['?' for _ in tournaments_to_delete])
            cursor.execute(f"DELETE FROM tournaments WHERE id IN ({placeholders})", list(tournaments_to_delete))
            
            # Also delete associated tournament results
            cursor.execute(f"DELETE FROM tournament_results WHERE tournament_id IN ({placeholders})", list(tournaments_to_delete))
            
            conn.commit()
            print(f"✅ Deleted {len(tournaments_to_delete)} duplicate tournament records")
        else:
            print("✅ No duplicates found")
        
        # Verify the fix
        cursor.execute("SELECT COUNT(*) FROM tournaments WHERE season_number = 1")
        final_count = cursor.fetchone()[0]
        print(f"📊 Final Season 1 tournaments: {final_count}")
        
        # Check tournament results
        cursor.execute("SELECT COUNT(*) FROM tournament_results tr JOIN tournaments t ON tr.tournament_id = t.id WHERE t.season_number = 1")
        results_count = cursor.fetchone()[0]
        print(f"📊 Season 1 tournament results: {results_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing duplicates: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_simulation_state():
    """Update simulation state to reflect post-Season 1 status"""
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE simulation_state 
            SET current_phase = ?, current_season = ?, current_event = ?, 
                total_players = ?, active_players = ?, last_updated = ?
            WHERE id = 1
        """, (
            'regular_season_1_complete',  # Phase
            1,                            # Season
            35,                           # Event (last event of Season 1)
            150,                          # Total players
            100,                          # Active players (after culling)
            datetime.now().isoformat()     # Last updated
        ))
        
        conn.commit()
        print("✅ Simulation state updated to post-Season 1")
        
        # Verify the update
        cursor.execute("SELECT * FROM simulation_state WHERE id = 1")
        state = cursor.fetchone()
        print(f"📊 New simulation state:")
        print(f"  Phase: {state[1]}")
        print(f"  Season: {state[2]}")
        print(f"  Event: {state[3]}")
        print(f"  Total players: {state[4]}")
        print(f"  Active players: {state[5]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating simulation state: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("🏌️  Database Cleanup and State Fix")
    print("=" * 50)
    
    # Fix duplicate tournaments
    success1 = fix_duplicate_tournaments()
    
    if success1:
        # Update simulation state
        success2 = update_simulation_state()
        
        if success2:
            print("\n🎉 Database cleanup and state fix complete!")
            print("✅ Duplicate tournaments removed")
            print("✅ Simulation state updated to post-Season 1")
        else:
            print("\n❌ Failed to update simulation state!")
    else:
        print("\n❌ Failed to fix duplicate tournaments!") 