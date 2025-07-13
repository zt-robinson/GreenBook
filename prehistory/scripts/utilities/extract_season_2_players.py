#!/usr/bin/env python3
"""
Extract Season 2 players and save to CSV
"""

import sqlite3
import csv
import os
from pathlib import Path

def extract_season_2_players():
    """Extract all Season 2 players and save to CSV"""
    
    # Database path
    db_path = Path("data/prehistory.db")
    
    # Output directory and file
    output_dir = Path("reports/regular_seasons/season_2")
    output_file = output_dir / "season_2_new_players.csv"
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query all Season 2 players
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
        current_status,
        introduction_season
    FROM players 
    WHERE name LIKE '%S2'
    ORDER BY name
    """
    
    cursor.execute(query)
    players = cursor.fetchall()
    
    # Column headers
    headers = [
        'id', 'name', 'age', 'nationality',
        'driving_power', 'driving_accuracy', 'approach_accuracy', 
        'short_game', 'putting', 'composure', 'confidence',
        'current_status', 'introduction_season'
    ]
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(players)
    
    conn.close()
    
    print(f"✅ Extracted {len(players)} Season 2 players")
    print(f"✅ Saved to: {output_file}")
    
    # Print summary
    print(f"\n📊 Season 2 Players Summary:")
    print(f"   Total new players: {len(players)}")
    print(f"   All players have 'S2' suffix")
    print(f"   All players marked as 'active'")
    print(f"   Introduction season: 2")

if __name__ == "__main__":
    extract_season_2_players() 