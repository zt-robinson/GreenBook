#!/usr/bin/env python3
"""
Test to ensure last place player never gets more than the player above them in a large field
"""

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))

from core.payout_calculator import PayoutCalculator
from faker import Faker

def test_large_field_last_place_adjustment():
    print("🔎 Testing large field payout adjustment (80 players)")
    print("=" * 60)
    
    fake = Faker()
    cut_size = 80
    purse = 21000000
    
    # Create test results for 80 players, positions 1-80
    test_results = []
    for pos in range(1, cut_size + 1):
        test_results.append({
            'player_id': pos,
            'name': fake.name(),
            'position': pos,
            'made_cut': True,
            'total_score': 280 + pos  # Just to have unique scores
        })
    
    calculator = PayoutCalculator('major', 'The Sovereign Tournament')
    payouts = calculator.calculate_final_payouts(test_results, purse, 'major', 'The Sovereign Tournament')
    
    # Find last and second-to-last payouts
    payout_79 = next(p['amount'] for p in payouts if p['position'] == 79)
    payout_80 = next(p['amount'] for p in payouts if p['position'] == 80)
    
    print(f"Player 79 payout: ${payout_79:,}")
    print(f"Player 80 payout: ${payout_80:,}")
    print(f"Difference (79 - 80): ${payout_79 - payout_80}")
    
    if payout_80 > payout_79:
        print(f"❌ ERROR: Player 80 (last place) gets more than player 79!")
    else:
        print(f"✅ CORRECT: Player 80 gets less than player 79 (as expected)")
    
    print("\nAll payouts for last 5 positions:")
    for pos in range(76, 81):
        payout = next(p['amount'] for p in payouts if p['position'] == pos)
        print(f"  Position {pos}: ${payout:,}")
    
    print("\nTest complete.")

if __name__ == "__main__":
    test_large_field_last_place_adjustment() 