#!/usr/bin/env python3
"""
Reactivate All Players Script for GreenBook Prehistory

This script changes all players' status from 'inactive' to 'active'.
"""

import sqlite3
import os

def reactivate_all_players():
    """Change all players' status from inactive to active"""
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
    print("🔄 REACTIVATING ALL PLAYERS")
    print("=" * 40)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Count inactive players before
        cursor.execute("SELECT COUNT(*) FROM players WHERE current_status = 'inactive'")
        inactive_count = cursor.fetchone()[0]
        print(f"📊 Found {inactive_count} inactive players")
        
        if inactive_count == 0:
            print("✅ No inactive players found. All players are already active.")
            return True
        
        # Update all inactive players to active
        cursor.execute("UPDATE players SET current_status = 'active' WHERE current_status = 'inactive'")
        updated_count = cursor.rowcount
        
        # Count active players after
        cursor.execute("SELECT COUNT(*) FROM players WHERE current_status = 'active'")
        active_count = cursor.fetchone()[0]
        
        conn.commit()
        
        print(f"✅ Successfully reactivated {updated_count} players")
        print(f"📊 Total active players: {active_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reactivating players: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    success = reactivate_all_players()
    if success:
        print("\n🎉 All players have been reactivated!")
    else:
        print("\n❌ Failed to reactivate players!") 