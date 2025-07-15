#!/usr/bin/env python3
"""
Generate Signature Event #1 field using the events database.
"""

import sqlite3
from pathlib import Path

def get_signature_event_1_field():
    """Generate the field for Signature Event #1 based on qualification criteria."""
    
    db_path = Path("greenbook/data/events.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    field = set()  # Use set to avoid duplicates
    
    print("Generating Signature Event #1 field...")
    
    # Priority 1: Winners of all events from Season 10
    print("\nPriority 1: Season 10 event winners")
    cursor.execute("""
        SELECT event_name, "1" as winner 
        FROM events 
        WHERE season = 10 
        ORDER BY season_event
    """)
    season_10_winners = cursor.fetchall()
    print(f"Found {len(season_10_winners)} Season 10 events")
    
    for event_name, winner in season_10_winners:
        field.add(winner)
        print(f"  {event_name}: {winner}")
    
    print(f"Priority 1 total: {len(field)} players")
    
    # Priority 2: Top 5 from Season 10 final standings
    print("\nPriority 2: Season 10 final standings top 5")
    cursor.execute("""
        SELECT "1", "2", "3", "4", "5" 
        FROM season_standings 
        WHERE season = 10
    """)
    season_10_top5 = cursor.fetchone()
    
    if season_10_top5:
        for player in season_10_top5:
            field.add(player)
        print(f"Season 10 top 5: {season_10_top5}")
        print(f"Priority 2 total: {len(field)} players")
    
    # Priority 3: Winners of majors and continental championships from seasons 6-9
    print("\nPriority 3: Major and Continental winners from seasons 6-9")
    cursor.execute("""
        SELECT season, event_name, "1" as winner 
        FROM events 
        WHERE (type = 'Major' OR type = 'Mini Major') 
        AND season BETWEEN 6 AND 9
        ORDER BY season, season_event
    """)
    major_continental_winners = cursor.fetchall()
    
    for season, event_name, winner in major_continental_winners:
        field.add(winner)
        print(f"  Season {season} {event_name}: {winner}")
    
    print(f"Priority 3 total: {len(field)} players")
    
    # Priority 4: Past Signature Event #1 winners (seasons 1-9)
    print("\nPriority 4: Past Signature Event #1 winners")
    cursor.execute("""
        SELECT season, "1" as winner 
        FROM events 
        WHERE event_code = 'SIG_1' AND season BETWEEN 1 AND 9
        ORDER BY season
    """)
    past_signature_winners = cursor.fetchall()
    
    for season, winner in past_signature_winners:
        field.add(winner)
        print(f"  Season {season}: {winner}")
    
    print(f"Priority 4 total: {len(field)} players")
    
    # Priority 5: Top players from Season 10 standings (fill remaining spots)
    print("\nPriority 5: Top players from Season 10 standings")
    cursor.execute("""
        SELECT "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
               "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
               "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
               "31", "32", "33", "34", "35", "36", "37", "38", "39", "40",
               "41", "42", "43", "44", "45", "46", "47", "48", "49", "50",
               "51", "52", "53", "54", "55", "56", "57", "58", "59", "60",
               "61", "62", "63", "64", "65", "66", "67", "68", "69", "70",
               "71", "72", "73", "74", "75"
        FROM season_standings 
        WHERE season = 10
    """)
    season_10_top75 = cursor.fetchone()
    
    if season_10_top75:
        for player in season_10_top75:
            if len(field) >= 75:  # Cap at 75 players
                break
            field.add(player)
    
    print(f"Final field size: {len(field)} players")
    
    # Convert to sorted list (sorted by last name)
    field_list = sorted(list(field), key=lambda name: name.split()[-1] if name else '')
    
    conn.close()
    
    return field_list

def print_field(field):
    """Print the field in a formatted way."""
    print(f"\nSignature Event #1 Field ({len(field)} players):")
    print("=" * 50)
    
    for i, player in enumerate(field, 1):
        print(f"{i:2d}. {player}")
    
    print("=" * 50)

if __name__ == "__main__":
    field = get_signature_event_1_field()
    print_field(field) 