#!/usr/bin/env python3
"""
Create Prehistory Database Script
Creates the comprehensive prehistory database with all required tables.
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '../../../data/prehistory.db')

def create_prehistory_database():
    """Create the prehistory database and all required tables"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Create players table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                nationality TEXT,
                -- Physical attributes
                driving_power REAL,
                driving_accuracy REAL,
                approach_accuracy REAL,
                short_game REAL,
                putting REAL,
                -- Mental attributes
                composure REAL,
                confidence REAL,
                focus REAL,
                risk_tolerance REAL,
                mental_fatigue REAL,
                consistency REAL,
                resilience REAL,
                -- Career tracking
                total_career_points INTEGER DEFAULT 0,
                career_wins INTEGER DEFAULT 0,
                seasons_played INTEGER DEFAULT 0,
                seasons_survived INTEGER DEFAULT 0,
                -- Prehistory tracking
                introduction_season INTEGER, -- 0 for gauntlet, 1-10 for regular seasons
                introduction_event INTEGER,
                current_status TEXT DEFAULT 'active', -- 'active', 'culled', 'retired'
                -- Metadata
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create tournaments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                tournament_type TEXT, -- 'gauntlet', 'signature', 'standard', 'invitational', 'major'
                season_number INTEGER, -- 0 for gauntlet, 1-10 for regular seasons
                event_number INTEGER, -- 1-10 for gauntlet, 1-35 for regular seasons
                field_size INTEGER,
                purse_amount REAL,
                prestige REAL,
                start_date TEXT,
                end_date TEXT,
                status TEXT DEFAULT 'scheduled', -- 'scheduled', 'completed'
                season_type TEXT, -- 'gauntlet' or 'regular'
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create tournament results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournament_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER,
                player_id INTEGER,
                position INTEGER,
                total_score INTEGER,
                points_earned INTEGER,
                round_1_score INTEGER,
                round_2_score INTEGER,
                round_3_score INTEGER,
                round_4_score INTEGER,
                made_cut BOOLEAN DEFAULT 1, -- always true for prehistory (no cuts)
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        ''')
        
        # Create tournament schedule table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tournament_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_id INTEGER,
                start_date TEXT,
                round_1_start TEXT,
                round_2_start TEXT,
                round_3_start TEXT,
                round_4_start TEXT,
                FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
            )
        ''')
        
        # Create seasons table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS seasons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season_number INTEGER, -- 0 for gauntlet, 1-10 for regular seasons
                season_type TEXT, -- 'gauntlet' or 'regular'
                total_events INTEGER,
                start_date TEXT,
                end_date TEXT,
                status TEXT DEFAULT 'scheduled', -- 'scheduled', 'running', 'completed'
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create season player stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS season_player_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season_id INTEGER,
                player_id INTEGER,
                total_season_points INTEGER DEFAULT 0,
                final_rank INTEGER,
                events_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                top_10s INTEGER DEFAULT 0,
                made_cuts INTEGER DEFAULT 0, -- always true for prehistory
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (season_id) REFERENCES seasons (id),
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        ''')
        
        # Create season event results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS season_event_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season_id INTEGER,
                tournament_id INTEGER,
                player_id INTEGER,
                event_rank INTEGER,
                points_earned INTEGER,
                total_score INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (season_id) REFERENCES seasons (id),
                FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
                FOREIGN KEY (player_id) REFERENCES players (id)
            )
        ''')
        
        # Create simulation state table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS simulation_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_phase TEXT, -- 'gauntlet', 'regular_season_1', etc.
                current_season INTEGER DEFAULT 0,
                current_event INTEGER DEFAULT 0,
                total_players INTEGER DEFAULT 0,
                active_players INTEGER DEFAULT 0,
                start_date TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'not_started' -- 'not_started', 'running', 'completed'
            )
        ''')
        
        # Create player pool history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_pool_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                season_number INTEGER,
                event_number INTEGER,
                players_before_culling INTEGER,
                players_after_culling INTEGER,
                new_players_added INTEGER DEFAULT 0,
                players_culled INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print("✅ Prehistory database created successfully!")
        print(f"   Database path: {DB_PATH}")
        print("   Tables created:")
        print("     - players")
        print("     - tournaments")
        print("     - tournament_results")
        print("     - tournament_schedule")
        print("     - seasons")
        print("     - season_player_stats")
        print("     - season_event_results")
        print("     - simulation_state")
        print("     - player_pool_history")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def initialize_simulation_state():
    """Initialize the simulation state"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Insert initial simulation state
        cursor.execute('''
            INSERT INTO simulation_state (
                current_phase, current_season, current_event, 
                total_players, active_players, start_date, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            'not_started', 0, 0, 0, 0, 
            'now', 'not_started'
        ))
        
        conn.commit()
        print("✅ Simulation state initialized!")
        
    except Exception as e:
        print(f"❌ Error initializing simulation state: {e}")
        conn.rollback()
    finally:
        conn.close()

def main():
    """Main function"""
    print("🏌️  Prehistory Database Initialization")
    print("=" * 50)
    
    success = create_prehistory_database()
    
    if success:
        initialize_simulation_state()
        print("\n🎉 Database initialization successful!")
        print("Ready to begin prehistory simulation!")
    else:
        print("\n❌ Database initialization failed!")

if __name__ == "__main__":
    main() 