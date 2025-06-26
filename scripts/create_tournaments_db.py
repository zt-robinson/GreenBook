import sqlite3
import os

def create_tournaments_database():
    """Create the tournaments database with all necessary tables"""
    
    db_path = os.path.join(os.path.dirname(__file__), 'golf_tournaments.db')
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing golf_tournaments.db")
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Create tournaments table
    cur.execute('''
        CREATE TABLE tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tournament_type TEXT NOT NULL,  -- 'regular', 'open', 'invitational', 'major'
            course_id INTEGER NOT NULL,
            field_size INTEGER NOT NULL,
            purse_amount INTEGER NOT NULL,  -- Total purse in dollars
            prestige_level REAL DEFAULT 1.0,  -- 1.0 to 10.0 scale
            season_number INTEGER NOT NULL,
            week_number INTEGER NOT NULL,  -- Week of the season
            status TEXT DEFAULT 'scheduled',  -- 'scheduled', 'active', 'completed'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create tournament fields table (which players are in which tournaments)
    cur.execute('''
        CREATE TABLE tournament_fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            entry_method TEXT NOT NULL,  -- 'full_status', 'conditional', 'exempt', 'sponsor_exemption', etc.
            starting_position INTEGER,  -- Position in field (1-156, etc.)
            group_number INTEGER,  -- Which group they're in
            group_position INTEGER,  -- Position within group (1, 2, or 3)
            tee_time TEXT,  -- When they start (e.g., "09:00", "09:03")
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
    ''')
    
    # Create tournament results table (round-by-round scores)
    cur.execute('''
        CREATE TABLE tournament_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            round_number INTEGER NOT NULL,  -- 1, 2, 3, or 4
            hole_1 INTEGER,
            hole_2 INTEGER,
            hole_3 INTEGER,
            hole_4 INTEGER,
            hole_5 INTEGER,
            hole_6 INTEGER,
            hole_7 INTEGER,
            hole_8 INTEGER,
            hole_9 INTEGER,
            hole_10 INTEGER,
            hole_11 INTEGER,
            hole_12 INTEGER,
            hole_13 INTEGER,
            hole_14 INTEGER,
            hole_15 INTEGER,
            hole_16 INTEGER,
            hole_17 INTEGER,
            hole_18 INTEGER,
            round_total INTEGER,  -- Total score for the round
            round_position INTEGER,  -- Position after this round
            to_par INTEGER,  -- Score relative to par
            birdies INTEGER,
            eagles INTEGER,
            bogeys INTEGER,
            double_bogeys INTEGER,
            other_scores INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
    ''')
    
    # Create tournament odds table (historical odds snapshots)
    cur.execute('''
        CREATE TABLE tournament_odds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            odds_type TEXT NOT NULL,  -- 'win', 'top5', 'top10', 'top20', 'make_cut', etc.
            odds_value REAL NOT NULL,  -- Decimal odds (e.g., 5.50 for 5.5 to 1)
            probability REAL NOT NULL,  -- Implied probability (e.g., 0.18 for 18%)
            round_number INTEGER,  -- Which round (NULL for tournament-long bets)
            hole_number INTEGER,  -- Which hole (NULL for round-long bets)
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
            FOREIGN KEY (player_id) REFERENCES players (id)
        )
    ''')
    
    # Create tournament schedule table (when tournaments happen)
    cur.execute('''
        CREATE TABLE tournament_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            start_date TEXT NOT NULL,  -- YYYY-MM-DD format
            start_time TEXT NOT NULL,  -- HH:MM format (e.g., "09:00")
            round_1_start TEXT NOT NULL,  -- "09:00"
            round_2_start TEXT NOT NULL,  -- "12:30"
            round_3_start TEXT NOT NULL,  -- "16:00"
            round_4_start TEXT NOT NULL,  -- "19:30"
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
        )
    ''')
    
    # Create payout structure table
    cur.execute('''
        CREATE TABLE payout_structure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tournament_id INTEGER NOT NULL,
            finish_position INTEGER NOT NULL,  -- 1, 2, 3, etc.
            payout_amount INTEGER NOT NULL,  -- Dollar amount
            payout_percentage REAL NOT NULL,  -- Percentage of purse
            tour_points INTEGER NOT NULL,  -- FedEx Cup points equivalent
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tournament_id) REFERENCES tournaments (id)
        )
    ''')
    
    # Create indexes for better performance
    cur.execute('CREATE INDEX idx_tournaments_season_week ON tournaments(season_number, week_number)')
    cur.execute('CREATE INDEX idx_tournament_fields_tournament ON tournament_fields(tournament_id)')
    cur.execute('CREATE INDEX idx_tournament_results_tournament_round ON tournament_results(tournament_id, round_number)')
    cur.execute('CREATE INDEX idx_tournament_odds_tournament_type ON tournament_odds(tournament_id, odds_type)')
    
    conn.commit()
    conn.close()
    
    print("✅ Tournament database created successfully!")
    print("   -> Tables 'tournaments', 'tournament_fields', 'tournament_results', 'tournament_odds', 'tournament_schedule', and 'payout_structure' are ready.")

if __name__ == "__main__":
    create_tournaments_database() 