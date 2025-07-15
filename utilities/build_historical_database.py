#!/usr/bin/env python3
"""
Build normalized historical database from CSV data.
Processes the comprehensive all_seasons_event_leaderboard.csv file.
"""

import csv
import sqlite3
import os
from pathlib import Path

def create_database():
    """Create the normalized database tables."""
    conn = sqlite3.connect('greenbook/data/master_tournaments.db')
    cursor = conn.cursor()
    
    # Create tournaments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            season INTEGER NOT NULL,
            season_event TEXT NOT NULL,
            type TEXT NOT NULL,
            event_code TEXT NOT NULL,
            event_name TEXT NOT NULL,
            UNIQUE(season, season_event)
        )
    ''')
    
    # Create tournament_results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournament_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            player_name TEXT NOT NULL,
            finish_position INTEGER NOT NULL,
            FOREIGN KEY (tournament_id) REFERENCES tournaments(id),
            UNIQUE(tournament_id, player_name)
        )
    ''')
    
    # Create season_standings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS season_standings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            season INTEGER NOT NULL,
            player_name TEXT NOT NULL,
            total_points INTEGER DEFAULT 0,
            events_played INTEGER DEFAULT 0,
            wins INTEGER DEFAULT 0,
            top_5s INTEGER DEFAULT 0,
            top_10s INTEGER DEFAULT 0,
            UNIQUE(season, player_name)
        )
    ''')
    
    conn.commit()
    return conn, cursor

def process_csv_data(cursor, csv_file_path):
    """Process the CSV data and populate the database."""
    tournaments_added = 0
    results_added = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        # Skip header row
        next(reader, None)
        
        for row in reader:
            if len(row) < 6:  # Skip incomplete rows
                continue
            if len(row) != 155:
                print(f"Malformed row (length {len(row)}): {row}")
                continue
                
            # Extract metadata
            season = int(row[0])
            season_event = row[1]
            event_type = row[2]
            event_code = row[3]
            event_name = row[4]
            
            # Insert tournament
            cursor.execute('''
                INSERT OR REPLACE INTO tournaments 
                (season, season_event, type, event_code, event_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (season, season_event, event_type, event_code, event_name))
            
            tournament_id = cursor.lastrowid
            tournaments_added += 1
            
            # Process player results (columns 6-155)
            for position in range(1, 151):  # 1st through 150th place
                player_name = row[4 + position]  # Column index 5 + position
                if player_name and player_name.strip():  # Skip empty names
                    cursor.execute('''
                        INSERT OR REPLACE INTO tournament_results 
                        (tournament_id, player_name, finish_position)
                        VALUES (?, ?, ?)
                    ''', (tournament_id, player_name.strip(), position))
                    results_added += 1
    
    return tournaments_added, results_added

def calculate_season_standings(cursor):
    """Calculate season standings from tournament results."""
    print("Calculating season standings...")
    
    # Get all seasons
    cursor.execute('SELECT DISTINCT season FROM tournaments ORDER BY season')
    seasons = [row[0] for row in cursor.fetchall()]
    
    for season in seasons:
        print(f"Processing season {season}...")
        
        # Get all players who participated in this season
        cursor.execute('''
            SELECT DISTINCT tr.player_name
            FROM tournament_results tr
            JOIN tournaments t ON tr.tournament_id = t.id
            WHERE t.season = ?
        ''', (season,))
        
        players = [row[0] for row in cursor.fetchall()]
        
        for player in players:
            # Calculate player stats for this season
            cursor.execute('''
                SELECT 
                    COUNT(*) as events_played,
                    SUM(CASE WHEN tr.finish_position = 1 THEN 1 ELSE 0 END) as wins,
                    SUM(CASE WHEN tr.finish_position <= 5 THEN 1 ELSE 0 END) as top_5s,
                    SUM(CASE WHEN tr.finish_position <= 10 THEN 1 ELSE 0 END) as top_10s,
                    SUM(CASE 
                        WHEN tr.finish_position = 1 THEN 25
                        WHEN tr.finish_position = 2 THEN 20
                        WHEN tr.finish_position = 3 THEN 16
                        WHEN tr.finish_position = 4 THEN 13
                        WHEN tr.finish_position = 5 THEN 11
                        WHEN tr.finish_position = 6 THEN 10
                        WHEN tr.finish_position = 7 THEN 9
                        WHEN tr.finish_position = 8 THEN 8
                        WHEN tr.finish_position = 9 THEN 7
                        WHEN tr.finish_position = 10 THEN 6
                        WHEN tr.finish_position <= 20 THEN 5
                        WHEN tr.finish_position <= 30 THEN 4
                        WHEN tr.finish_position <= 50 THEN 3
                        WHEN tr.finish_position <= 100 THEN 2
                        ELSE 1
                    END) as total_points
                FROM tournament_results tr
                JOIN tournaments t ON tr.tournament_id = t.id
                WHERE t.season = ? AND tr.player_name = ?
            ''', (season, player))
            
            stats = cursor.fetchone()
            
            # Insert or update season standings
            cursor.execute('''
                INSERT OR REPLACE INTO season_standings 
                (season, player_name, total_points, events_played, wins, top_5s, top_10s)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (season, player, stats[4], stats[0], stats[1], stats[2], stats[3]))

def main():
    """Main function to build the historical database."""
    print("Building historical database from CSV data...")
    
    # Check if CSV file exists
    csv_file = 'greenbook/prehistory/reports/regular_seasons/all_seasons_event_leaderboard.csv'
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        return
    
    # Create database
    conn, cursor = create_database()
    
    try:
        # Process CSV data
        print("Processing CSV data...")
        tournaments_added, results_added = process_csv_data(cursor, csv_file)
        
        print(f"Added {tournaments_added} tournaments")
        print(f"Added {results_added} tournament results")
        
        # Calculate season standings
        calculate_season_standings(cursor)
        
        # Commit changes
        conn.commit()
        
        # Print summary statistics
        cursor.execute('SELECT COUNT(*) FROM tournaments')
        total_tournaments = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM tournament_results')
        total_results = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM season_standings')
        total_standings = cursor.fetchone()[0]
        
        print(f"\nDatabase Summary:")
        print(f"Total tournaments: {total_tournaments}")
        print(f"Total tournament results: {total_results}")
        print(f"Total season standings entries: {total_standings}")
        
        print(f"\nHistorical database created successfully!")
        print(f"Database file: greenbook/data/master_tournaments.db")
        
    except Exception as e:
        print(f"Error processing data: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    main() 