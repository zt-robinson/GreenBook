#!/usr/bin/env python3
"""
Insert missing season_player_stats rows for players found in the leaderboard but missing from the database, using the correct stats from the leaderboard.
"""

import sqlite3
import re
from pathlib import Path

def extract_player_stats_from_leaderboard(leaderboard_file):
    player_stats = {}
    with open(leaderboard_file, 'r', encoding='utf-8') as f:
        content = f.read()
    table_match = re.search(r'\|.*\n\|.*\n((?:\|.*\n)*)', content)
    if not table_match:
        print("Could not find table in leaderboard file")
        return player_stats
    table_lines = table_match.group(1).strip().split('\n')
    for line in table_lines:
        if not line.strip():
            continue
        parts = [part.strip() for part in line.split('|')[1:-1]]
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

def main():
    db_path = Path("data/prehistory.db")
    leaderboard_path = Path("reports/season_1_leaderboard.md")
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        return
    if not leaderboard_path.exists():
        print(f"Leaderboard file not found: {leaderboard_path}")
        return
    player_stats = extract_player_stats_from_leaderboard(leaderboard_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Find missing players
    cursor.execute("SELECT p.id, p.name FROM players p WHERE p.id NOT IN (SELECT player_id FROM season_player_stats WHERE season_id = 1);")
    missing = cursor.fetchall()
    inserted = 0
    for player_id, player_name in missing:
        # Try exact match, then fallback to normalized match
        stats = player_stats.get(player_name)
        if not stats:
            for k, v in player_stats.items():
                if k.strip().lower() == player_name.strip().lower():
                    stats = v
                    break
        if not stats:
            print(f"Warning: {player_name} not found in leaderboard, skipping.")
            continue
        cursor.execute("""
            INSERT INTO season_player_stats 
            (season_id, player_id, total_season_points, final_rank, events_played, wins, top_10s, made_cuts)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            1, player_id, stats['points'], stats['rank'], stats['events'], stats['wins'], 0, 35
        ))
        print(f"Inserted stats for {player_name}: {stats['points']} points, rank {stats['rank']}")
        inserted += 1
    conn.commit()
    print(f"\nInserted stats for {inserted} missing players.")
    cursor.execute("SELECT COUNT(*) FROM season_player_stats WHERE season_id = 1")
    print(f"Total rows in season_player_stats for Season 1: {cursor.fetchone()[0]}")
    conn.close()

if __name__ == "__main__":
    main() 