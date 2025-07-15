#!/usr/bin/env python3
"""
Build events database from CSV files.
Creates tables for events and season standings with columns for finishing positions.
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path

def build_events_database():
    """Build the events database from CSV files."""
    
    # Database path
    db_path = Path("greenbook/data/events.db")
    db_path.parent.mkdir(exist_ok=True)
    
    # Remove existing database
    if db_path.exists():
        db_path.unlink()
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    
    # Read event leaderboard CSV
    events_csv = Path("greenbook/prehistory/reports/final_summary/all_seasons_event_leaderboard.csv")
    events_df = pd.read_csv(events_csv)
    
    # Read season standings CSV
    standings_csv = Path("greenbook/prehistory/reports/final_summary/all_seasons_final_rankings.csv")
    standings_df = pd.read_csv(standings_csv)
    
    print(f"Building events database at {db_path}")
    print(f"Events data: {len(events_df)} rows")
    print(f"Standings data: {len(standings_df)} rows")
    
    # Create events table
    print("Creating events table...")
    
    # Get all position columns (1-150)
    position_cols = [str(i) for i in range(1, 151)]
    
    # Create events table with all columns
    events_table_cols = ['season', 'season_event', 'type', 'event_code', 'event_name'] + position_cols
    events_table_df = events_df[events_table_cols].copy()
    
    # Write to database
    events_table_df.to_sql('events', conn, index=False, if_exists='replace')
    
    # Create season_standings table
    print("Creating season_standings table...")
    
    # Create standings table with all columns
    standings_table_cols = ['season'] + position_cols
    standings_table_df = standings_df[standings_table_cols].copy()
    
    # Write to database
    standings_table_df.to_sql('season_standings', conn, index=False, if_exists='replace')
    
    # Create indexes for better performance
    print("Creating indexes...")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_season ON events(season)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_events_event_code ON events(event_code)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_standings_season ON season_standings(season)")
    
    # Test queries
    print("\nTesting database...")
    
    # Test events table
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM events")
    event_count = cursor.fetchone()[0]
    print(f"Events table: {event_count} rows")
    
    # Test season standings table
    cursor.execute("SELECT COUNT(*) FROM season_standings")
    standings_count = cursor.fetchone()[0]
    print(f"Season standings table: {standings_count} rows")
    
    # Test query for Season 10 winners
    cursor.execute("""
        SELECT event_name, "1" as winner 
        FROM events 
        WHERE season = 10 
        ORDER BY season_event
        LIMIT 5
    """)
    season_10_winners = cursor.fetchall()
    print(f"\nSample Season 10 winners:")
    for event_name, winner in season_10_winners:
        print(f"  {event_name}: {winner}")
    
    # Test query for Season 10 top 5
    cursor.execute("""
        SELECT "1", "2", "3", "4", "5" 
        FROM season_standings 
        WHERE season = 10
    """)
    season_10_top5 = cursor.fetchone()
    print(f"\nSeason 10 top 5: {season_10_top5}")
    
    # Test query for major winners from seasons 6-9
    cursor.execute("""
        SELECT season, event_name, "1" as winner 
        FROM events 
        WHERE type = 'Major' AND season BETWEEN 6 AND 9
        ORDER BY season, season_event
    """)
    major_winners = cursor.fetchall()
    print(f"\nMajor winners from seasons 6-9:")
    for season, event_name, winner in major_winners:
        print(f"  Season {season} {event_name}: {winner}")
    
    conn.close()
    print(f"\nDatabase built successfully at {db_path}")

if __name__ == "__main__":
    build_events_database() 