#!/usr/bin/env python3
"""
Fix duplicate season_player_stats rows for Season 1.
Removes duplicates and keeps only the row that matches the Season 1 leaderboard.
"""

import sqlite3
import re
from pathlib import Path

def extract_player_stats_from_leaderboard(leaderboard_file):
    """Extract player stats from the Season 1 leaderboard markdown file."""
    player_stats = {}
    
    with open(leaderboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the table section
    table_match = re.search(r'\|.*\n\|.*\n((?:\|.*\n)*)', content)
    if not table_match:
        print("Could not find table in leaderboard file")
        return player_stats
    
    table_lines = table_match.group(1).strip().split('\n')
    
    for line in table_lines:
        if not line.strip():
            continue
            
        # Parse table row: | Rank | Player | Nationality | Points | Events | Event Wins |
        parts = [part.strip() for part in line.split('|')[1:-1]]  # Remove empty first/last parts
        if len(parts) < 6:
            continue
            
        try:
            rank = int(parts[0])
            player_name = parts[1]
            points = int(parts[3])
            events = int(parts[4])
            wins = int(parts[5])
            
            player_stats[player_name] = {
                'rank': rank,
                'points': points,
                'events': events,
                'wins': wins
            }
        except (ValueError, IndexError):
            continue
    
    return player_stats

def get_player_id_by_name(conn, player_name):
    """Get player ID by name from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM players WHERE name = ?", (player_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def fix_duplicate_season_stats(conn, player_stats):
    """Remove duplicate season_player_stats rows and keep only the correct ones."""
    cursor = conn.cursor()
    
    # Get all players with season 1 stats
    cursor.execute("SELECT DISTINCT player_id FROM season_player_stats WHERE season_id = 1")
    player_ids = [row[0] for row in cursor.fetchall()]
    
    fixed_count = 0
    
    for player_id in player_ids:
        # Get player name
        cursor.execute("SELECT name FROM players WHERE id = ?", (player_id,))
        result = cursor.fetchone()
        if not result:
            print(f"Player ID {player_id} not found in database")
            continue
            
        player_name = result[0]
        
        # Get all rows for this player in season 1
        cursor.execute("SELECT * FROM season_player_stats WHERE player_id = ? AND season_id = 1", (player_id,))
        rows = cursor.fetchall()
        
        if len(rows) == 1:
            # No duplicates, skip
            continue
            
        print(f"Fixing {len(rows)} rows for {player_name} (ID: {player_id})")
        
        # Get correct stats from leaderboard
        correct_stats = None
        for k, v in player_stats.items():
            if k.strip().lower() == player_name.strip().lower():
                correct_stats = v
                break
        
        if not correct_stats:
            print(f"  Warning: {player_name} not found in leaderboard")
            # Keep the most recent row if not in leaderboard
            cursor.execute("""
                SELECT * FROM season_player_stats 
                WHERE player_id = ? AND season_id = 1 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (player_id,))
            most_recent = cursor.fetchone()
            if most_recent:
                # Delete all rows except the most recent
                cursor.execute("""
                    DELETE FROM season_player_stats 
                    WHERE player_id = ? AND season_id = 1 AND id != ?
                """, (player_id, most_recent[0]))
                print(f"  Kept most recent row (not in leaderboard)")
            continue
        
        # Find the row that matches the leaderboard stats
        matching_row = None
        for row in rows:
            row_id, season_id, p_id, points, rank, events, wins, top_10s, made_cuts, created_at = row
            if (points == correct_stats['points'] and 
                rank == correct_stats['rank'] and 
                events == correct_stats['events'] and 
                wins == correct_stats['wins']):
                matching_row = row
                break
        
        if matching_row:
            # Delete all rows except the matching one
            cursor.execute("""
                DELETE FROM season_player_stats 
                WHERE player_id = ? AND season_id = 1 AND id != ?
            """, (player_id, matching_row[0]))
            print(f"  Kept correct row: {correct_stats['points']} points, rank {correct_stats['rank']}")
        else:
            print(f"  Warning: No matching row found for {player_name}")
            # Keep the most recent row
            cursor.execute("""
                SELECT * FROM season_player_stats 
                WHERE player_id = ? AND season_id = 1 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (player_id,))
            most_recent = cursor.fetchone()
            if most_recent:
                cursor.execute("""
                    DELETE FROM season_player_stats 
                    WHERE player_id = ? AND season_id = 1 AND id != ?
                """, (player_id, most_recent[0]))
                print(f"  Kept most recent row (no match found)")
        
        fixed_count += 1
    
    conn.commit()
    print(f"\nFixed duplicates for {fixed_count} players")

def main():
    # Paths
    db_path = Path("data/prehistory.db")
    leaderboard_path = Path("reports/season_1_leaderboard.md")
    
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return
    
    if not leaderboard_path.exists():
        print(f"Leaderboard file not found: {leaderboard_path}")
        return
    
    # Extract player stats from leaderboard
    print("Extracting player stats from Season 1 leaderboard...")
    player_stats = extract_player_stats_from_leaderboard(leaderboard_path)
    print(f"Found stats for {len(player_stats)} players")
    
    # Connect to database and fix duplicates
    conn = sqlite3.connect(db_path)
    try:
        print("\nFixing duplicate season_player_stats rows...")
        fix_duplicate_season_stats(conn, player_stats)
        
        # Verify the fix
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM season_player_stats WHERE season_id = 1")
        total_rows = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT player_id) FROM season_player_stats WHERE season_id = 1")
        unique_players = cursor.fetchone()[0]
        print(f"\nTotal rows in season_player_stats for Season 1: {total_rows}")
        print(f"Unique players with Season 1 stats: {unique_players}")
        
        if total_rows == unique_players:
            print("✅ All duplicates have been removed!")
        else:
            print("⚠️  Some duplicates may still exist")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main() 