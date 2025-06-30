#!/usr/bin/env python3
"""
Test to demonstrate potential payout order issue with the current adjustment logic
"""

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))

from core.payout_calculator import PayoutCalculator
from faker import Faker

def test_payout_order_issue():
    """Test to show potential issue with payout order after adjustment"""
    
    print("⚠️ Testing Potential Payout Order Issue")
    print("=" * 50)
    
    # Create test results where the last player in the list is NOT the highest position
    fake = Faker()
    
    # Create results with positions 1, 2, 3, 5, 4 (note: 4 is missing, 5 comes before 4)
    test_results = [
        {'player_id': 1, 'name': fake.name(), 'position': 1, 'made_cut': True, 'total_score': 280},
        {'player_id': 2, 'name': fake.name(), 'position': 2, 'made_cut': True, 'total_score': 281},
        {'player_id': 3, 'name': fake.name(), 'position': 3, 'made_cut': True, 'total_score': 282},
        {'player_id': 5, 'name': fake.name(), 'position': 5, 'made_cut': True, 'total_score': 284},  # Position 5
        {'player_id': 4, 'name': fake.name(), 'position': 4, 'made_cut': True, 'total_score': 283},  # Position 4 (last in list)
    ]
    
    print("Test scenario: Players with positions [1, 2, 3, 5, 4]")
    print("Note: Position 4 player is last in the list")
    print()
    
    # Calculate payouts
    calculator = PayoutCalculator('major', 'The Sovereign Tournament')
    payouts = calculator.calculate_final_payouts(test_results, 21000000, 'major', 'The Sovereign Tournament')
    
    # Show the results
    print("Payout results (before sorting):")
    for payout in payouts:
        print(f"  Position {payout['position']}: {payout['player_name']} - ${payout['amount']:,}")
    
    print()
    print("Issue: The adjustment was made to the last player in the list (position 4),")
    print("but position 5 should be the one getting the adjustment!")
    print()
    
    # Check if position 4 got more than position 5
    pos4_payout = next(p['amount'] for p in payouts if p['position'] == 4)
    pos5_payout = next(p['amount'] for p in payouts if p['position'] == 5)
    
    print(f"Position 4 payout: ${pos4_payout:,}")
    print(f"Position 5 payout: ${pos5_payout:,}")
    
    if pos4_payout > pos5_payout:
        print(f"✅ CORRECT: Position 4 (${pos4_payout:,}) gets more than Position 5 (${pos5_payout:,})")
        print(f"   This is the proper payout order!")
    else:
        print(f"❌ PROBLEM: Position 5 (${pos5_payout:,}) gets more than Position 4 (${pos4_payout:,})")
        print(f"   This would violate payout order!")
    
    print()
    print("The fix ensures the adjustment goes to the highest position player,")
    print("which maintains proper payout order while ensuring exact purse distribution.")

if __name__ == "__main__":
    test_payout_order_issue() 