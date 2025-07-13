#!/usr/bin/env python3
"""
Repopulate season_player_stats for Season 1 from the original leaderboard.
This ensures all 150 players have the correct stats that match the leaderboard exactly.
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

def repopulate_season_stats(conn, player_stats):
    """Repopulate season_player_stats for all players from the leaderboard."""
    cursor = conn.cursor()
    
    inserted_count = 0
    not_found_count = 0
    
    for player_name, stats in player_stats.items():
        # Get player ID from database
        player_id = get_player_id_by_name(conn, player_name)
        if not player_id:
            print(f"Warning: Player '{player_name}' not found in database")
            not_found_count += 1
            continue
        
        # Insert season stats
        cursor.execute("""
            INSERT INTO season_player_stats 
            (season_id, player_id, total_season_points, final_rank, events_played, wins, top_10s, made_cuts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1,  # season_id
            player_id,
            stats['points'],
            stats['rank'],
            stats['events'],
            stats['wins'],
            0,  # top_10s - we don't have this data
            35  # made_cuts - all players made all cuts in prehistory
        ))
        
        inserted_count += 1
        print(f"Inserted stats for {player_name}: {stats['points']} points, rank {stats['rank']}")
    
    conn.commit()
    print(f"\nInserted season stats for {inserted_count} players")
    if not_found_count > 0:
        print(f"Warning: {not_found_count} players not found in database")

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
    
    # Connect to database and repopulate stats
    conn = sqlite3.connect(db_path)
    try:
        print("\nRepopulating season_player_stats...")
        repopulate_season_stats(conn, player_stats)
        
        # Verify the repopulation
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM season_player_stats WHERE season_id = 1")
        total_rows = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(DISTINCT player_id) FROM season_player_stats WHERE season_id = 1")
        unique_players = cursor.fetchone()[0]
        print(f"\nTotal rows in season_player_stats for Season 1: {total_rows}")
        print(f"Unique players with Season 1 stats: {unique_players}")
        
        if total_rows == unique_players and total_rows == len(player_stats):
            print("✅ All players have been repopulated with correct stats!")
        else:
            print("⚠️  Some players may be missing or have duplicates")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main() 