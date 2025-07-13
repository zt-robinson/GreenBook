#!/usr/bin/env python3
"""
Extract Season 3 players and save to CSV
"""

import sqlite3
import csv
import os
from pathlib import Path

def extract_season_3_players():
    """Extract all Season 3 players and save to CSV"""
    
    # Database path
    db_path = Path("data/prehistory.db")
    
    # Output directory and file
    output_dir = Path("reports/regular_seasons/season_3")
    output_file = output_dir / "season_3_new_players.csv"
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query all Season 3 players
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
    WHERE name LIKE '%S3'
    ORDER BY id
    """
    
    cursor.execute(query)
    players = cursor.fetchall()
    
    # Column headers
    headers = [
        'id', 'name', 'age', 'nationality',
        'driving_power', 'driving_accuracy', 'approach_accuracy', 'short_game', 'putting',
        'composure', 'confidence', 'focus', 'risk_tolerance', 'mental_fatigue', 'consistency', 'resilience',
        'current_status', 'introduction_season'
    ]
    
    # Write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(players)
    
    conn.close()
    
    print(f"✅ Extracted {len(players)} Season 3 players")
    print(f"📁 CSV saved to: {output_file}")
    
    # Show sample of players
    print(f"\n📋 Sample Season 3 players:")
    for i, player in enumerate(players[:5]):
        print(f"  {i+1}. {player[1]} ({player[2]}, {player[3]}) - Season {player[17]}")

if __name__ == "__main__":
    extract_season_3_players() 