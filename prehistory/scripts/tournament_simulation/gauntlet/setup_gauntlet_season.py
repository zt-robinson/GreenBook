#!/usr/bin/env python3
"""
Setup Gauntlet Season
Creates the 10 Gauntlet tournaments in the database.
"""

import sqlite3
import os
from datetime import datetime, timedelta

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '../../../data/prehistory.db')

def setup_gauntlet_season():
    """Create the 10 Gauntlet tournaments in the database"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tournament names for the Gauntlet season
    tournament_names = [
        "The Gauntlet Opener",
        "Spring Championship",
        "Summer Classic",
        "Fall Invitational", 
        "Winter Challenge",
        "Mid-Season Showdown",
        "Championship Qualifier",
        "Elite Tournament",
        "Final Countdown",
        "The Gauntlet Finale"
    ]
    
    # Start date for the season
    start_date = datetime(2024, 1, 15)  # January 15, 2024
    
    try:
        # Create the Gauntlet season record
        cursor.execute('''
            INSERT INTO seasons (
                season_number, season_type, total_events, start_date, end_date, status
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            0,  # Season 0 = Gauntlet
            'gauntlet',
            10,
            start_date.isoformat(),
            (start_date + timedelta(days=90)).isoformat(),  # 90-day season
            'scheduled'
        ))
        season_id = cursor.lastrowid
        
        print(f"✅ Created Gauntlet season (ID: {season_id})")
        
        # Create the 10 tournaments
        for i, tournament_name in enumerate(tournament_names, 1):
            # Calculate tournament date (every 9 days)
            tournament_date = start_date + timedelta(days=(i-1) * 9)
            
            # Create tournament record
            cursor.execute('''
                INSERT INTO tournaments (
                    name, tournament_type, season_number, event_number,
                    field_size, purse_amount, prestige, start_date, end_date,
                    status, season_type, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tournament_name,
                'gauntlet',
                0,  # Season 0 = Gauntlet
                i,  # Event number 1-10
                600,  # Field size
                1000000.0,  # $1M purse
                0.5,  # Medium prestige
                tournament_date.isoformat(),
                (tournament_date + timedelta(days=4)).isoformat(),  # 4-day tournament
                'scheduled',
                'gauntlet',
                datetime.now().isoformat()
            ))
            tournament_id = cursor.lastrowid
            
            # Create tournament schedule
            cursor.execute('''
                INSERT INTO tournament_schedule (
                    tournament_id, start_date, round_1_start, round_2_start, 
                    round_3_start, round_4_start
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                tournament_id,
                tournament_date.isoformat(),
                '08:00',  # Round 1
                '08:00',  # Round 2  
                '08:00',  # Round 3
                '08:00'   # Round 4
            ))
            
            print(f"✅ Created tournament {i}: {tournament_name} (ID: {tournament_id}) - {tournament_date.strftime('%Y-%m-%d')}")
        
        conn.commit()
        print(f"\n🎉 Gauntlet season setup complete!")
        print(f"   Season ID: {season_id}")
        print(f"   Tournaments created: 10")
        print(f"   Season duration: 90 days")
        print(f"   Total field size: 600 players per event")
        
        return season_id
        
    except Exception as e:
        print(f"❌ Error setting up Gauntlet season: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def main():
    """Main function"""
    print("🏌️  Gauntlet Season Setup")
    print("=" * 50)
    
    season_id = setup_gauntlet_season()
    
    if season_id:
        print("\n✅ Gauntlet season is ready for simulation!")
        print("Next step: Run tournament simulations")
    else:
        print("\n❌ Gauntlet season setup failed!")

if __name__ == "__main__":
    main() 