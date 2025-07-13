#!/usr/bin/env python3
"""
Populate Missing Season 1 Stats Script for GreenBook Prehistory

This script populates missing Season 1 stats from the leaderboard data.
"""

import sqlite3
import os
import re
from pathlib import Path

def extract_player_stats_from_leaderboard(leaderboard_file):
    """Extract player stats from the Season 1 leaderboard markdown file"""
    player_stats = {}
    
    with open(leaderboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the table section
    lines = content.split('\n')
    in_table = False
    
    for line in lines:
        if '| Rank | Player | Nationality | Points | Events | Event Wins |' in line:
            in_table = True
            continue
        elif in_table and line.strip() == '':
            break
        elif in_table and line.startswith('|'):
            # Parse table row
            parts = [part.strip() for part in line.split('|')[1:-1]]  # Remove empty first/last parts
            if len(parts) >= 4 and parts[0].isdigit():
                rank = int(parts[0])
                name = parts[1]
                nationality = parts[2]
                points = int(parts[3])
                events = int(parts[4])
                wins = int(parts[5])
                
                player_stats[name] = {
                    'rank': rank,
                    'points': points,
                    'events': events,
                    'wins': wins,
                    'nationality': nationality
                }
    
    return player_stats

def get_player_id_by_name(conn, player_name):
    """Get player ID by name from the database"""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE name = ?", (player_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def populate_missing_season_1_stats():
    """Populate missing Season 1 stats from leaderboard data"""
    db_path = Path("data/prehistory.db")
    leaderboard_path = Path("reports/season_1_leaderboard.md")
    
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return False
    
    if not leaderboard_path.exists():
        print(f"Leaderboard file not found: {leaderboard_path}")
        return False
    
    # Extract player stats from leaderboard
    print("Extracting player stats from Season 1 leaderboard...")
    player_stats = extract_player_stats_from_leaderboard(leaderboard_path)
    print(f"Found stats for {len(player_stats)} players")
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get existing Season 1 stats
        cursor.execute("SELECT player_id FROM season_player_stats WHERE season_id = 1")
        existing_player_ids = {row[0] for row in cursor.fetchall()}
        print(f"Players with existing Season 1 stats: {len(existing_player_ids)}")
        
        # Find missing players
        missing_players = []
        for name, stats in player_stats.items():
            player_id = get_player_id_by_name(conn, name)
            if player_id and player_id not in existing_player_ids:
                missing_players.append((player_id, name, stats))
        
        print(f"Players missing Season 1 stats: {len(missing_players)}")
        
        if not missing_players:
            print("✅ All players already have Season 1 stats!")
            return True
        
        # Insert missing stats
        inserted = 0
        for player_id, name, stats in missing_players:
            cursor.execute("""
                INSERT INTO season_player_stats 
                (season_id, player_id, total_season_points, final_rank, events_played, wins, top_10s, made_cuts)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                1, player_id, stats['points'], stats['rank'], 
                stats['events'], stats['wins'], 0, stats['events']  # All events count as made cuts
            ))
            print(f"Inserted stats for {name}: {stats['points']} points, rank {stats['rank']}")
            inserted += 1
        
        conn.commit()
        print(f"\n✅ Successfully inserted stats for {inserted} players")
        
        # Verify the results
        cursor.execute("SELECT COUNT(*) FROM season_player_stats WHERE season_id = 1")
        total_stats = cursor.fetchone()[0]
        print(f"Total Season 1 stats records: {total_stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error populating stats: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = populate_missing_season_1_stats()
    if success:
        print("\n🎉 Season 1 stats population complete!")
    else:
        print("\n❌ Failed to populate Season 1 stats!") 