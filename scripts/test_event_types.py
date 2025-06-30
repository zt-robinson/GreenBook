#!/usr/bin/env python3
"""
Test script for the event types framework
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.event_types import event_type_manager
from core.tournament_logic import tournament_logic

def test_event_types():
    """Test the event types framework"""
    print("🏌️ Testing Event Types Framework")
    print("=" * 50)
    
    # Test 1: List available event types
    print("\n1. Available Event Types:")
    event_types = event_type_manager.list_event_types()
    for event_type in event_types:
        config = event_type_manager.get_event_type(event_type)
        print(f"   • {event_type}: {config.name}")
        
        # Handle random vs fixed values
        if isinstance(config.field_size, dict):
            print(f"     Field size: Random {config.field_size['min']}-{config.field_size['max']} (multiple of {config.field_size['multiple']})")
        else:
            print(f"     Field size: {config.field_size}")
            
        if isinstance(config.purse_base, dict):
            print(f"     Purse: Random ${config.purse_base['min']:,}-${config.purse_base['max']:,}")
        else:
            print(f"     Purse: ${config.purse_base:,}")
            
        print(f"     Cut line: {config.cut_line.description}")
        print(f"     Winner points: {config.points_structure.winner}")
        
        if isinstance(config.prestige, dict):
            print(f"     Prestige: Random {config.prestige['min']}-{config.prestige['max']}")
        else:
            print(f"     Prestige: {config.prestige}")
    
    # Test 2: Tournament overrides
    print("\n2. Tournament Overrides:")
    overrides = event_type_manager.list_tournament_overrides()
    for tournament in overrides:
        config = event_type_manager.get_tournament_config(tournament)
        print(f"   • {tournament}")
        print(f"     Event type: {config['event_type']}")
        print(f"     Field size: {config['field_size']}")
        print(f"     Purse: ${config['purse_base']:,}")
        print(f"     Cut line: {config['cut_line']['description']}")
        print(f"     Prestige: {config['prestige']}")
    
    # Test 3: Payout structure calculation
    print("\n3. Payout Structure Examples:")
    test_tournaments = ["Sony Open in Hawaii", "The Masters Tournament", "U.S. Open Championship"]
    
    for tournament in test_tournaments:
        print(f"\n   {tournament}:")
        payout_structure = event_type_manager.calculate_payout_structure(tournament)
        for payout in payout_structure[:5]:  # Show top 5
            points = event_type_manager.get_points_for_position(tournament, payout['position'])
            print(f"     {payout['position']}. ${payout['amount']:,} ({payout['percentage']}%) - {points} points")
    
    # Test 4: Field candidate generation
    print("\n4. Field Candidate Generation:")
    for tournament in test_tournaments[:1]:  # Test with Sony Open
        print(f"\n   {tournament} eligible players:")
        candidates = tournament_logic.generate_field_candidates(tournament)
        print(f"     Total eligible: {len(candidates)}")
        
        # Show first 10 with qualification method
        for i, player in enumerate(candidates[:10]):
            print(f"     {i+1:2d}. {player['name']} - {player['qualification_method']}")
        
        if len(candidates) > 10:
            print(f"     ... and {len(candidates) - 10} more")
    
    # Test 5: Tournament creation with random values
    print("\n5. Tournament Creation Test (with random values):")
    try:
        # Get available courses
        import sqlite3
        courses_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')
        conn = sqlite3.connect(courses_db_path)
        cur = conn.cursor()
        cur.execute('SELECT id, name FROM courses LIMIT 1')
        course = cur.fetchone()
        conn.close()
        
        if course:
            # Test creating a standard event (will have random field size, purse, prestige)
            tournament_id = tournament_logic.create_tournament(
                tournament_name="Test Standard Event",
                course_id=course[0],
                start_date="2025-08-15",
                season_number=0,
                week_number=10,
                event_type="standard"
            )
            print(f"   ✅ Created test tournament with ID: {tournament_id}")
            
            # Get tournament summary
            summary = tournament_logic.get_tournament_summary(tournament_id)
            if summary:
                print(f"   Tournament: {summary['tournament']['name']}")
                print(f"   Field size: {summary['tournament']['field_size']}")
                print(f"   Purse: ${summary['tournament']['purse_amount']:,}")
                print(f"   Prestige: {summary['tournament']['prestige_level']}")
                print(f"   Status: {summary['tournament']['status']}")
                
                # Show some payout examples
                print(f"   Payout examples:")
                for payout in summary['payout_structure'][:3]:
                    points = event_type_manager.get_points_for_position(summary['tournament']['name'], payout['finish_position'])
                    print(f"     {payout['finish_position']}. ${payout['payout_amount']:,} - {points} points")
        else:
            print("   ⚠️ No courses available for testing")
            
    except Exception as e:
        print(f"   ❌ Error creating test tournament: {e}")
    
    # Test 6: Multiple standard events to show randomness
    print("\n6. Random Value Generation Test:")
    print("   Creating 3 standard events to show randomness:")
    
    for i in range(3):
        config = event_type_manager.get_tournament_config(f"Random Event {i+1}")
        print(f"   Event {i+1}: Field size {config['field_size']}, Purse ${config['purse_base']:,}, Prestige {config['prestige']}")
    
    print("\n" + "=" * 50)
    print("✅ Event Types Framework Test Complete!")

if __name__ == "__main__":
    test_event_types() 