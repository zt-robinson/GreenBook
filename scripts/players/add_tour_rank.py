#!/usr/bin/env python3
"""
Add tour_rank field to players database and assign random tour rankings
"""

import sqlite3
import os
import random

def add_tour_rank_field():
    """Add tour_rank field to the players table"""
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), '../../data/golf_players.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        # Check if tour_rank column already exists
        cur.execute("PRAGMA table_info(players)")
        columns = [column[1] for column in cur.fetchall()]
        
        if 'tour_rank' not in columns:
            print("📝 Adding tour_rank column to players table...")
            cur.execute('ALTER TABLE players ADD COLUMN tour_rank INTEGER')
            conn.commit()
            print("✅ tour_rank column added successfully")
        else:
            print("✅ tour_rank column already exists")
        
        # Get all players
        cur.execute('SELECT id FROM players ORDER BY id')
        player_ids = [row[0] for row in cur.fetchall()]
        
        if not player_ids:
            print("❌ No players found in database")
            return False
        
        print(f"🎯 Assigning random tour rankings to {len(player_ids)} players...")
        
        # Create a random permutation of ranks 1 to len(player_ids)
        tour_ranks = list(range(1, len(player_ids) + 1))
        random.shuffle(tour_ranks)
        
        # Update each player with a random tour rank
        for player_id, tour_rank in zip(player_ids, tour_ranks):
            cur.execute('''
                UPDATE players 
                SET tour_rank = ? 
                WHERE id = ?
            ''', (tour_rank, player_id))
        
        conn.commit()
        
        # Display some sample rankings
        cur.execute('''
            SELECT name, tour_rank, world_ranking 
            FROM players 
            ORDER BY tour_rank 
            LIMIT 10
        ''')
        
        print("\n🏆 Top 10 Tour Rankings:")
        print("-" * 60)
        print(f"{'Rank':<4} {'Name':<25} {'World Rank':<10}")
        print("-" * 60)
        
        for row in cur.fetchall():
            name, tour_rank, world_rank = row
            print(f"{tour_rank:<4} {name:<25} {world_rank or 'N/A':<10}")
        
        print(f"\n✅ Tour rankings assigned successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating tour rankings: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    add_tour_rank_field() 