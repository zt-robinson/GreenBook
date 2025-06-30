#!/usr/bin/env python3
"""
Test script for the new dynamic payout system
"""

from core.payout_calculator import PayoutCalculator

def test_major_specific_payouts():
    """Test the new major-specific payout structure"""
    print("🏆 Testing Major-Specific Payout Structure\n")
    
    # Test each major with their specific winner percentages
    majors = [
        {
            'name': 'The Sovereign Tournament',
            'winner_pct': 20.0,
            'purse': 23000000,
            'cut_size': 70
        },
        {
            'name': 'Royal Open Championship', 
            'winner_pct': 20.0,
            'purse': 24000000,
            'cut_size': 70
        },
        {
            'name': 'American Open Championship',
            'winner_pct': 18.0,
            'purse': 22000000,
            'cut_size': 70
        },
        {
            'name': 'AGA Championship',
            'winner_pct': 18.0,
            'purse': 21000000,
            'cut_size': 70
        }
    ]
    
    for major in majors:
        print(f"🏆 {major['name']}")
        print("-" * 50)
        
        calculator = PayoutCalculator('major', major['name'])
        
        # Calculate payout structure
        payout_percentages = calculator.calculate_payout_structure(
            major['cut_size'], 
            major['purse']
        )
        
        # Validate the structure
        is_valid, message = calculator.validate_payout_structure(payout_percentages)
        print(f"Validation: {'✅' if is_valid else '❌'} {message}")
        
        # Show total percentage
        total_percentage = sum(payout_percentages.values())
        print(f"Total Percentage: {total_percentage:.4f}%")
        
        # Calculate and show top 10 total
        top_10_total = sum(payout_percentages.get(pos, 0) for pos in range(1, 11))
        print(f"Top 10 Total: {top_10_total:.2f}% (Target: 60.00%)")
        
        # Calculate and show top 25 total
        top_25_total = sum(payout_percentages.get(pos, 0) for pos in range(1, 26))
        print(f"Top 25 Total: {top_25_total:.2f}% (Target: 80.00%)")
        
        # Show key positions
        print(f"\nKey Payouts:")
        key_positions = [1, 2, 3, 5, 10, 15, 20, 25]
        for pos in key_positions:
            if pos in payout_percentages:
                percentage = payout_percentages[pos]
                amount = int(major['purse'] * (percentage / 100))
                print(f"  {pos:2d}. {percentage:6.3f}% = ${amount:,}")
        
        # Show some middle positions
        print(f"\nMiddle Positions:")
        middle_positions = [30, 40, 50, 60]
        for pos in middle_positions:
            if pos in payout_percentages:
                percentage = payout_percentages[pos]
                amount = int(major['purse'] * (percentage / 100))
                print(f"  {pos:2d}. {percentage:6.3f}% = ${amount:,}")
        
        # Show last position
        last_pos = major['cut_size']
        if last_pos in payout_percentages:
            percentage = payout_percentages[last_pos]
            amount = int(major['purse'] * (percentage / 100))
            print(f"  {last_pos:2d}. {percentage:6.3f}% = ${amount:,}")
        
        print()

def test_payout_system():
    """Test the new dynamic payout calculation system"""
    print("💰 Testing Dynamic Payout System\n")
    
    # Test different tournament types
    test_cases = [
        {
            'name': 'Standard Tour Event',
            'event_type': 'standard',
            'tournament_name': None,
            'purse': 8500000,   # $8.5M
            'cut_size': 65
        },
        {
            'name': 'Small Cut Tournament',
            'event_type': 'standard',
            'tournament_name': None,
            'purse': 5000000,   # $5M
            'cut_size': 30
        }
    ]
    
    for test_case in test_cases:
        print(f"🏆 {test_case['name']}")
        print("-" * 50)
        
        calculator = PayoutCalculator(test_case['event_type'], test_case['tournament_name'])
        
        # Show anchor positions
        anchor_positions = calculator.get_anchor_positions()
        print(f"Anchor Positions:")
        for pos, pct in anchor_positions.items():
            print(f"  {pos:2d}. {pct:5.3f}%")
        
        # Calculate payout structure
        payout_percentages = calculator.calculate_payout_structure(
            test_case['cut_size'], 
            test_case['purse']
        )
        
        # Validate the structure
        is_valid, message = calculator.validate_payout_structure(payout_percentages)
        print(f"\nValidation: {'✅' if is_valid else '❌'} {message}")
        
        # Show total percentage
        total_percentage = sum(payout_percentages.values())
        print(f"Total Percentage: {total_percentage:.4f}%")
        
        # Show key positions
        print(f"\nKey Payouts:")
        key_positions = [1, 2, 3, 5, 10, 15, 20, 25]
        for pos in key_positions:
            if pos in payout_percentages:
                percentage = payout_percentages[pos]
                amount = int(test_case['purse'] * (percentage / 100))
                print(f"  {pos:2d}. {percentage:6.3f}% = ${amount:,}")
        
        # Show some middle positions
        print(f"\nMiddle Positions:")
        middle_positions = [30, 40, 50, 60]
        for pos in middle_positions:
            if pos in payout_percentages:
                percentage = payout_percentages[pos]
                amount = int(test_case['purse'] * (percentage / 100))
                print(f"  {pos:2d}. {percentage:6.3f}% = ${amount:,}")
        
        # Show last position
        last_pos = test_case['cut_size']
        if last_pos in payout_percentages:
            percentage = payout_percentages[last_pos]
            amount = int(test_case['purse'] * (percentage / 100))
            print(f"  {last_pos:2d}. {percentage:6.3f}% = ${amount:,}")
        
        print()

def test_tie_handling():
    """Test how ties are handled in the payout system"""
    print("🤝 Testing Tie Handling\n")
    
    calculator = PayoutCalculator('major', 'The Sovereign Tournament')
    purse = 23000000
    cut_size = 70
    
    # Calculate base payout structure
    payout_percentages = calculator.calculate_payout_structure(cut_size, purse)
    
    # Create a sample leaderboard with ties
    sample_results = [
        {'player_id': 1, 'name': 'Player A', 'position': 1, 'made_cut': True},  # Winner
        {'player_id': 2, 'name': 'Player B', 'position': 2, 'made_cut': True},  # Runner-up
        {'player_id': 3, 'name': 'Player C', 'position': 3, 'made_cut': True},  # Third
        {'player_id': 4, 'name': 'Player D', 'position': 3, 'made_cut': True},  # Tied for third
        {'player_id': 5, 'name': 'Player E', 'position': 5, 'made_cut': True},  # Fifth
        {'player_id': 6, 'name': 'Player F', 'position': 6, 'made_cut': True},  # Sixth
        {'player_id': 7, 'name': 'Player G', 'position': 6, 'made_cut': True},  # Tied for sixth
        {'player_id': 8, 'name': 'Player H', 'position': 6, 'made_cut': True},  # Tied for sixth
        {'player_id': 9, 'name': 'Player I', 'position': 9, 'made_cut': True},  # Ninth
        {'player_id': 10, 'name': 'Player J', 'position': 10, 'made_cut': True}, # Tenth
    ]
    
    # Handle ties
    player_payouts = calculator.handle_ties(sample_results, payout_percentages)
    
    print("Tie Handling Results:")
    print("-" * 30)
    
    for player in sample_results:
        player_id = player['player_id']
        if player_id in player_payouts:
            payout_info = player_payouts[player_id]
            amount = int(purse * (payout_info['percentage'] / 100))
            
            tie_info = f" (T-{payout_info['tied_count']})" if payout_info['tied'] else ""
            print(f"{player['name']:12} - {payout_info['position']:2d}. {payout_info['percentage']:6.3f}% = ${amount:,}{tie_info}")
    
    print()

def test_different_cut_sizes():
    """Test how the system handles different cut sizes"""
    print("📊 Testing Different Cut Sizes\n")
    
    calculator = PayoutCalculator('major', 'The Sovereign Tournament')
    purse = 23000000
    
    cut_sizes = [50, 60, 70, 80, 90]
    
    for cut_size in cut_sizes:
        print(f"Cut Size: {cut_size} players")
        print("-" * 25)
        
        payout_percentages = calculator.calculate_payout_structure(cut_size, purse)
        
        # Calculate top 10 and top 25 totals
        top_10_total = sum(payout_percentages.get(pos, 0) for pos in range(1, 11))
        top_25_total = sum(payout_percentages.get(pos, 0) for pos in range(1, 26))
        
        print(f"Top 10 Total: {top_10_total:.2f}% (Target: 60.00%)")
        print(f"Top 25 Total: {top_25_total:.2f}% (Target: 80.00%)")
        
        # Show last position payout
        last_pos = cut_size
        if last_pos in payout_percentages:
            percentage = payout_percentages[last_pos]
            amount = int(purse * (percentage / 100))
            print(f"Last Position ({last_pos}): {percentage:.3f}% = ${amount:,}")
        
        print()

if __name__ == "__main__":
    test_major_specific_payouts()
    test_payout_system()
    test_tie_handling()
    test_different_cut_sizes()
    
    print("✅ Dynamic payout system test completed!") 