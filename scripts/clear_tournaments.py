#!/usr/bin/env python3
"""
Clear all existing tournaments and related data
"""

import sqlite3
import os

def clear_all_tournaments():
    """Clear all existing tournaments and related data"""
    
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_tournaments.db')
    
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

def main():
    print("🎯 Tournament Clearer")
    print("=" * 30)
    
    if clear_all_tournaments():
        print("\n🎉 Database cleared and ready for new tournaments!")
    else:
        print("\n❌ Failed to clear tournaments")

if __name__ == "__main__":
    main() 