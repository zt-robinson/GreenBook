#!/usr/bin/env python3
"""
Test script to show sample payout schedules for The Sovereign and a standard event, with ties and bottom payouts.
"""
# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))
from core.payout_calculator import PayoutCalculator
from faker import Faker

def simulate_leaderboard(cut_size, ties=None):
    """Simulate a leaderboard with optional ties. ties: dict of position -> tie count"""
    fake = Faker()
    leaderboard = []
    pos = 1
    player_id = 1
    while pos <= cut_size:
        tie_count = ties.get(pos, 1) if ties else 1
        for _ in range(tie_count):
            leaderboard.append({
                'player_id': player_id,
                'name': fake.name(),
                'position': pos,
                'made_cut': True
            })
            player_id += 1
        pos += tie_count
    return leaderboard

def print_payouts(event_type, tournament_name, purse, cut_size, ties, label):
    print(f"\n===== {label} =====")
    calc = PayoutCalculator(event_type, tournament_name)
    leaderboard = simulate_leaderboard(cut_size, ties)
    payouts = calc.calculate_final_payouts(leaderboard, purse, event_type, tournament_name)
    print(f"Purse: ${purse:,} | Field: {cut_size} | Ties: {ties}")
    print(f"{'Pos':>4} {'Name':<20} {'Payout $':>12} {'%':>7} {'Tied':>5}")
    print("-"*55)
    # Print top 5
    for p in payouts[:5]:
        tie = f"T-{p['tied_count']}" if p['tied'] else ""
        print(f"{p['position']:>4} {p['player_name']:<20} {p['amount']:>12,} {p['percentage']:>7.3f} {tie:>5}")
    # Print some middle positions
    print("...")
    for p in payouts[30:35]:
        tie = f"T-{p['tied_count']}" if p['tied'] else ""
        print(f"{p['position']:>4} {p['player_name']:<20} {p['amount']:>12,} {p['percentage']:>7.3f} {tie:>5}")
    # Print bottom 5
    print("...")
    for p in payouts[-5:]:
        tie = f"T-{p['tied_count']}" if p['tied'] else ""
        print(f"{p['position']:>4} {p['player_name']:<20} {p['amount']:>12,} {p['percentage']:>7.3f} {tie:>5}")

def main():
    # The Sovereign Tournament
    sovereign_ties = {2: 2, 5: 3, 10: 2, 70: 2}  # ties for 2nd, 5th, 10th, last
    print_payouts('major', 'The Sovereign Tournament', 21000000, 70, sovereign_ties, 'SOVEREIGN TOURNAMENT')
    # Royal Open Championship
    royal_open_ties = {2: 2, 5: 2, 10: 3, 70: 2}
    print_payouts('major', 'Royal Open Championship', 24000000, 70, royal_open_ties, 'ROYAL OPEN CHAMPIONSHIP')
    # American Open Championship
    american_open_ties = {2: 2, 5: 2, 10: 2, 70: 2}
    print_payouts('major', 'American Open Championship', 22000000, 70, american_open_ties, 'AMERICAN OPEN CHAMPIONSHIP')
    # AGA Championship
    aga_ties = {2: 2, 5: 2, 10: 2, 70: 2}
    print_payouts('major', 'AGA Championship', 21000000, 70, aga_ties, 'AGA CHAMPIONSHIP')
    # Standard Event
    standard_ties = {2: 2, 5: 2, 10: 3, 65: 2}  # ties for 2nd, 5th, 10th, last
    print_payouts('standard', None, 8500000, 65, standard_ties, 'STANDARD TOUR EVENT')

if __name__ == "__main__":
    main() 