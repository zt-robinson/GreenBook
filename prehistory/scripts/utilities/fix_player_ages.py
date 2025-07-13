#!/usr/bin/env python3
"""
Fix Player Ages Script for GreenBook Prehistory

Ages players correctly based on their introduction season:
- Original players (no suffix): +3 years
- S1 players: +2 years  
- S2 players: +1 year
- S3 players: +0 years (new)
"""

import sqlite3
import os
from pathlib import Path

def fix_player_ages():
    """Age players correctly based on their introduction season"""
    
    db_path = Path("data/prehistory.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🏌️  FIXING PLAYER AGES BASED ON INTRODUCTION SEASON")
        print("=" * 60)
        
        # Get current player counts and ages
        cursor.execute("SELECT COUNT(*) FROM players")
        total_players = cursor.fetchone()[0]
        
        print(f"📊 Total players in database: {total_players}")
        
        # Age original players (no suffix) by +3 years
        cursor.execute("""
            UPDATE players 
            SET age = age + 3 
            WHERE name NOT LIKE '%S1' AND name NOT LIKE '%S2' AND name NOT LIKE '%S3'
        """)
        original_updated = cursor.rowcount
        print(f"✅ Original players aged +3: {original_updated}")
        
        # Age S1 players by +2 years
        cursor.execute("UPDATE players SET age = age + 2 WHERE name LIKE '%S1'")
        s1_updated = cursor.rowcount
        print(f"✅ S1 players aged +2: {s1_updated}")
        
        # Age S2 players by +1 year
        cursor.execute("UPDATE players SET age = age + 1 WHERE name LIKE '%S2'")
        s2_updated = cursor.rowcount
        print(f"✅ S2 players aged +1: {s2_updated}")
        
        # S3 players stay the same (new)
        cursor.execute("SELECT COUNT(*) FROM players WHERE name LIKE '%S3'")
        s3_count = cursor.fetchone()[0]
        print(f"✅ S3 players unchanged: {s3_count}")
        
        conn.commit()
        
        # Show sample results
        print(f"\n📋 Sample aged players:")
        
        # Original players
        cursor.execute("""
            SELECT name, age, introduction_season 
            FROM players 
            WHERE name NOT LIKE '%S1' AND name NOT LIKE '%S2' AND name NOT LIKE '%S3'
            LIMIT 3
        """)
        for name, age, season in cursor.fetchall():
            print(f"  {name}: {age} years old (Season {season})")
        
        # S1 players
        cursor.execute("SELECT name, age, introduction_season FROM players WHERE name LIKE '%S1' LIMIT 3")
        for name, age, season in cursor.fetchall():
            print(f"  {name}: {age} years old (Season {season})")
        
        # S2 players
        cursor.execute("SELECT name, age, introduction_season FROM players WHERE name LIKE '%S2' LIMIT 3")
        for name, age, season in cursor.fetchall():
            print(f"  {name}: {age} years old (Season {season})")
        
        # S3 players
        cursor.execute("SELECT name, age, introduction_season FROM players WHERE name LIKE '%S3' LIMIT 3")
        for name, age, season in cursor.fetchall():
            print(f"  {name}: {age} years old (Season {season})")
        
        print(f"\n✅ Player ages fixed successfully!")
        print(f"   Total players processed: {total_players}")
        
    except Exception as e:
        print(f"❌ Error fixing player ages: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_player_ages() 