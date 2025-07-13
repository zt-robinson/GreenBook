#!/usr/bin/env python3
"""
Fix Season 1 stats for players missing from season_player_stats table.
Extracts actual season totals from the Season 1 leaderboard.
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

def insert_missing_season_stats(conn, player_stats):
    """Insert missing season stats for players."""
    cursor = conn.cursor()
    
    # List of players that were missing from season_player_stats
    missing_player_ids = [1262, 1264, 1304, 1334, 1361, 1373, 1390, 1392, 1449, 1490, 1495, 1522, 1537, 1591, 1619, 1714, 1765, 1852, 1856, 1859, 1863, 1868, 1870, 1875, 1880, 1884, 1885, 1889, 1890, 1891, 1895, 1896, 1898, 1899]
    
    inserted_count = 0
    
    for player_id in missing_player_ids:
        # Get player name from database
        cursor.execute("SELECT name FROM players WHERE id = ?", (player_id,))
        result = cursor.fetchone()
        if not result:
            print(f"Player ID {player_id} not found in database")
            continue
        player_name = result[0]
        # Try exact match, then fallback to normalized match
        stats = player_stats.get(player_name)
        if not stats:
            # Try stripping whitespace and case-insensitive match
            for k, v in player_stats.items():
                if k.strip().lower() == player_name.strip().lower():
                    stats = v
                    break
        if not stats and player_name == "Andrew Newman S1":
            # Fallback: hardcode from leaderboard
            stats = {'rank': 150, 'points': 380, 'events': 35, 'wins': 0}
            print(f"Hardcoded stats for Andrew Newman S1: {stats}")
        if not stats:
            print(f"Player {player_name} not found in leaderboard")
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
    
    # Connect to database and insert missing stats
    conn = sqlite3.connect(db_path)
    try:
        print("\nInserting missing season stats...")
        insert_missing_season_stats(conn, player_stats)
        
        # Verify the fix
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT player_id) FROM season_player_stats WHERE season_id = 1")
        count = cursor.fetchone()[0]
        print(f"\nTotal players with Season 1 stats: {count}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main() 