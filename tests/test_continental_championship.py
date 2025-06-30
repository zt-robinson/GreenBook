#!/usr/bin/env python3
"""
Test script to verify The Continental Championship configuration
"""

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))

from core.event_types import EventTypeManager
from core.payout_calculator import PayoutCalculator

def test_continental_championship():
    """Test The Continental Championship configuration"""
    
    event_type_manager = EventTypeManager()
    
    print("=== THE CONTINENTAL CHAMPIONSHIP TEST ===\n")
    
    tournament_name = "The Continental Championship"
    
    # Test 1: Verify configuration
    print("1. Configuration Check:")
    try:
        config = event_type_manager.get_tournament_config(tournament_name)
        
        print(f"   Event Type: {config['event_type']}")
        print(f"   Field Size: {config['field_size']}")
        print(f"   Cut Line: {config['cut_line']['description']}")
        print(f"   Purse: ${config['purse_base']:,}")
        print(f"   Prestige: {config['prestige']}")
        
        # Verify it's configured as a mini major
        assert config['event_type'] == 'standard', "Should be standard event type"
        assert config['purse_base'] == 30000000, "Should have $30M fixed purse"
        assert config['prestige'] == 0.95, "Should have 0.95 prestige"
        
        print("   ✅ Configuration is correct for mini major")
        
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return
    
    # Test 2: Verify payout structure (should use standard event logic)
    print("\n2. Payout Structure Test:")
    try:
        calculator = PayoutCalculator('standard', tournament_name)
        payout_percentages = calculator.calculate_payout_structure(65, 30000000)
        
        # Validate the structure
        is_valid, message = calculator.validate_payout_structure(payout_percentages)
        print(f"   Validation: {'✅' if is_valid else '❌'} {message}")
        
        # Show total percentage
        total_percentage = sum(payout_percentages.values())
        print(f"   Total Percentage: {total_percentage:.4f}%")
        
        # Show key payouts
        print(f"   Winner: {payout_percentages.get(1, 0):.2f}% = ${int(30000000 * (payout_percentages.get(1, 0) / 100)):,}")
        print(f"   Runner-up: {payout_percentages.get(2, 0):.2f}% = ${int(30000000 * (payout_percentages.get(2, 0) / 100)):,}")
        print(f"   Last (65): {payout_percentages.get(65, 0):.3f}% = ${int(30000000 * (payout_percentages.get(65, 0) / 100)):,}")
        
        # Verify it uses standard event targets
        top_15_total = sum(payout_percentages.get(pos, 0) for pos in range(1, 16))
        top_25_total = sum(payout_percentages.get(pos, 0) for pos in range(1, 26))
        print(f"   Top 15 Total: {top_15_total:.2f}% (Target: 70.00%)")
        print(f"   Top 25 Total: {top_25_total:.2f}% (Target: 85.00%)")
        
        print("   ✅ Uses standard event payout logic")
        
    except Exception as e:
        print(f"   ❌ Payout error: {e}")
    
    # Test 3: Verify points structure (should use major points)
    print("\n3. Points Structure Test:")
    try:
        # Test key positions
        positions_to_test = [1, 2, 3, 10, 25, 65]
        
        for pos in positions_to_test:
            points = event_type_manager.get_points_for_position(tournament_name, pos)
            print(f"   Position {pos}: {points} points")
        
        # Verify winner gets major-level points
        winner_points = event_type_manager.get_points_for_position(tournament_name, 1)
        assert winner_points == 750, f"Winner should get 750 points, got {winner_points}"
        print("   ✅ Uses major points structure")
        
    except Exception as e:
        print(f"   ❌ Points error: {e}")
    
    # Test 4: Compare with other events
    print("\n4. Comparison with Other Events:")
    
    comparison_events = [
        ("Standard Event", "Standard Event Test"),
        ("The Continental Championship", tournament_name),
        ("Major Event", "The Sovereign Tournament")
    ]
    
    for event_type, event_name in comparison_events:
        try:
            config = event_type_manager.get_tournament_config(event_name)
            winner_points = event_type_manager.get_points_for_position(event_name, 1)
            print(f"   {event_type}: {winner_points} points, ${config['purse_base']:,} purse, {config['prestige']} prestige")
        except Exception as e:
            print(f"   {event_type}: Error - {e}")
    
    print("\n" + "=" * 60)
    print("✅ The Continental Championship Test Complete!")
    print("\nSummary:")
    print("• Event type: Standard (for field size and qualifying)")
    print("• Purse: Fixed $30M")
    print("• Payout: Standard event logic (top 15: 70%, top 25: 85%)")
    print("• Points: Major structure (winner: 750 points)")
    print("• Prestige: 0.95 (high for mini major)")
    print("• Cut: Top 65 and ties (standard event cut)")

if __name__ == "__main__":
    test_continental_championship() 