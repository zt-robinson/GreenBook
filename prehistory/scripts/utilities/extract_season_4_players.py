#!/usr/bin/env python3
"""
Extract Season 4 players and save to CSV
"""

import sqlite3
import csv
from pathlib import Path

def extract_season_4_players():
    """Extract all Season 4 players and save to CSV"""
    db_path = Path("data/prehistory.db")
    output_dir = Path("reports/regular_seasons/season_4")
    output_file = output_dir / "season_4_new_players.csv"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT 
        id,
        name,
        age,
        nationality,
        driving_power,
        driving_accuracy,
        approach_accuracy,
        short_game,
        putting,
        composure,
        confidence,
        focus,
        risk_tolerance,
        mental_fatigue,
        consistency,
        resilience,
        current_status,
        introduction_season
    FROM players 
    WHERE name LIKE '%S4'
    ORDER BY id
    """
    cursor.execute(query)
    players = cursor.fetchall()
    headers = [
        'id', 'name', 'age', 'nationality',
        'driving_power', 'driving_accuracy', 'approach_accuracy', 'short_game', 'putting',
        'composure', 'confidence', 'focus', 'risk_tolerance', 'mental_fatigue', 'consistency', 'resilience',
        'current_status', 'introduction_season'
    ]
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(players)
    conn.close()
    print(f"✅ Extracted {len(players)} Season 4 players")
    print(f"📁 CSV saved to: {output_file}")
    print(f"\n📋 Sample Season 4 players:")
    for i, player in enumerate(players[:5]):
        print(f"  {i+1}. {player[1]} ({player[2]}, {player[3]}) - Season {player[17]}")

if __name__ == "__main__":
    extract_season_4_players() 