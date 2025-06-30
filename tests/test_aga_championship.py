#!/usr/bin/env python3
"""
Test script for the AGA Championship configuration
"""

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))

from core.event_types import event_type_manager

def test_aga_championship():
    """Test the AGA Championship configuration"""
    print("🏆 Testing AGA Championship Configuration\n")
    
    tournament_name = "AGA Championship"
    config = event_type_manager.get_tournament_config(tournament_name)
    
    print(f"📋 Tournament: {tournament_name}")
    print(f"   Event Type: {config['event_type']}")
    print(f"   Field Size: {config['field_size']}")
    print(f"   Cut Line: {config['cut_line']['description']}")
    print(f"   Purse: ${config['purse_base']:,}")
    print(f"   Prestige: {config['prestige']}")
    print(f"   Qualification Methods: {', '.join(config['qualification_methods'])}")
    
    # Test points structure
    print(f"\n🏆 Points Structure:")
    winner_points = event_type_manager.get_points_for_position(tournament_name, 1)
    runner_up_points = event_type_manager.get_points_for_position(tournament_name, 2)
    third_points = event_type_manager.get_points_for_position(tournament_name, 3)
    tenth_points = event_type_manager.get_points_for_position(tournament_name, 10)
    cut_line_points = event_type_manager.get_points_for_position(tournament_name, config['cut_line']['value'])
    
    print(f"   Winner (1st): {winner_points}")
    print(f"   Runner-up (2nd): {runner_up_points}")
    print(f"   Third (3rd): {third_points}")
    print(f"   Tenth (10th): {tenth_points}")
    print(f"   Cut Line ({config['cut_line']['value']}th): {cut_line_points}")
    
    # Test payout structure
    payout_structure = event_type_manager.calculate_payout_structure(tournament_name)
    print(f"\n💰 Payout Structure:")
    print(f"   Total Positions: {len(payout_structure)}")
    print(f"   Winner Payout: ${payout_structure[0]['amount']:,}")
    print(f"   Runner-up Payout: ${payout_structure[1]['amount']:,}")
    print(f"   Third Payout: ${payout_structure[2]['amount']:,}")
    print(f"   Tenth Payout: ${payout_structure[9]['amount']:,}")
    print(f"   Cut Line Payout: ${payout_structure[config['cut_line']['value']-1]['amount']:,}")
    
    print(f"\n✅ AGA Championship configuration test completed!")

if __name__ == "__main__":
    test_aga_championship() 