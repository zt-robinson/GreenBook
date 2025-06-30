#!/usr/bin/env python3
"""
Check tournament details in the database and display in table format
"""

import sqlite3
import os
import sys

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.event_types import event_type_manager

def get_tournament_details():
    """Get all tournament details from the database"""
    
    tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_tournaments.db')
    
    if not os.path.exists(tournaments_db_path):
        print(f"❌ Tournament database not found at {tournaments_db_path}")
        return []
    
    conn = sqlite3.connect(tournaments_db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    try:
        # Get all tournaments with their schedule info and new columns
        cur.execute('''
            SELECT t.id, t.name, t.tournament_type, t.field_size, t.purse_amount, t.prestige,
                   t.cut_line_value, t.cut_line_type, t.points_to_winner, s.start_date
            FROM tournaments t
            JOIN tournament_schedule s ON t.id = s.tournament_id
            ORDER BY s.start_date, t.name
        ''')
        
        tournaments = []
        for row in cur.fetchall():
            tournament = dict(row)
            
            # Extract cut line info from new columns
            cut_line_type = tournament.get('cut_line_type', 'position')
            cut_line_value = tournament.get('cut_line_value', 65)
            
            if cut_line_type == 'none':
                cut_line_display = "No Cut"
            elif cut_line_type == 'position':
                cut_line_display = str(cut_line_value) if cut_line_value is not None else "Unknown"
            else:
                cut_line_display = "Standard"
            
            # Get points to winner from new column
            winner_points = tournament.get('points_to_winner', 0)
            
            tournaments.append({
                'id': tournament['id'],
                'name': tournament['name'],
                'event_type': tournament['tournament_type'],
                'field_size': tournament['field_size'],
                'purse': tournament['purse_amount'],
                'prestige': tournament['prestige'],
                'start_date': tournament['start_date'],
                'cut_line': cut_line_display,
                'winner_points': winner_points
            })
        
        return tournaments
        
    finally:
        conn.close()

def display_tournament_table(tournaments):
    """Display tournaments in a formatted table"""
    
    if not tournaments:
        print("❌ No tournaments found in database")
        return
    
    print("🎯 Tournament Details from Database")
    print("=" * 90)
    
    # Table header
    print(f"{'ID':<3} {'Name':<25} {'Type':<12} {'Field':<6} {'Purse':<12} {'Prestige':<8} {'Cut Line':<15} {'Points':<8} {'Date':<12}")
    print("-" * 90)
    
    for tournament in tournaments:
        # Handle None values with defaults
        tournament_id = tournament['id'] or 0
        name = tournament['name'] or 'Unknown'
        event_type = tournament['event_type'] or 'unknown'
        field_size = tournament['field_size'] or 0
        purse = tournament['purse'] or 0
        prestige = tournament['prestige'] or 0.0
        cut_line = tournament['cut_line'] or 'Unknown'
        winner_points = tournament['winner_points'] or 0
        start_date = tournament['start_date'] or 'Unknown'
        
        print(f"{tournament_id:<3} "
              f"{name:<25} "
              f"{event_type:<12} "
              f"{field_size:<6} "
              f"${purse:,} "
              f"{prestige:<8.3f} "
              f"{cut_line:<15} "
              f"{winner_points:<8} "
              f"{start_date:<12}")
    
    print("-" * 90)
    print(f"Total tournaments: {len(tournaments)}")
    print("\n📊 Notes:")
    print("   - Prestige is now on a 0-1 scale (was 1-10)")
    print("   - Cut line and points are stored in database")
    print("   - All event variables are now persistent")

def check_specific_issues(tournaments):
    """Check for specific issues with tournament data"""
    
    print("\n🔍 Checking for Data Issues")
    print("-" * 40)
    
    issues_found = []
    
    for tournament in tournaments:
        # Check prestige scale (should be 0-1)
        if tournament['prestige'] > 1.0:
            issues_found.append(f"❌ {tournament['name']}: Prestige {tournament['prestige']} > 1.0 (should be 0-1 scale)")
        
        # Check for missing cut line info
        if tournament['cut_line'] == "Standard":
            issues_found.append(f"⚠️ {tournament['name']}: Generic cut line (should be specific)")
        
        # Check for zero points to winner
        if tournament['winner_points'] == 0:
            issues_found.append(f"❌ {tournament['name']}: Zero points to winner")
    
    if issues_found:
        print("Issues found:")
        for issue in issues_found:
            print(f"   {issue}")
    else:
        print("✅ No major issues found")
        print("   - All prestige values are on 0-1 scale")
        print("   - All tournaments have cut line information")
        print("   - All tournaments have points to winner")

def main():
    print("🔍 Tournament Database Checker")
    print("=" * 50)
    
    tournaments = get_tournament_details()
    
    if tournaments:
        display_tournament_table(tournaments)
        check_specific_issues(tournaments)
    else:
        print("❌ No tournaments found in database")

if __name__ == "__main__":
    main() 