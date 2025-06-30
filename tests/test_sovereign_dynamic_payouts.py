#!/usr/bin/env python3
"""
Test script to demonstrate dynamic payout integration for The Sovereign Tournament
"""

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))

from core.tournament_logic import tournament_logic
from core.payout_calculator import PayoutCalculator
import sqlite3
from faker import Faker

def test_sovereign_dynamic_payouts():
    """Test the dynamic payout system for The Sovereign Tournament"""
    
    print("🏆 Testing Dynamic Payout Integration for The Sovereign Tournament")
    print("=" * 70)
    
    # Test 1: Create The Sovereign Tournament
    print("\n1. Creating The Sovereign Tournament...")
    
    # Get a course for the tournament
    courses_db_path = os.path.join('greenbook', 'data', 'golf_courses.db')
    conn = sqlite3.connect(courses_db_path)
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM courses LIMIT 1')
    course = cur.fetchone()
    conn.close()
    
    if not course:
        print("❌ No courses available. Please ensure golf_courses.db exists.")
        return
    
    course_id, course_name = course
    
    # Create The Sovereign Tournament
    try:
        tournament_id = tournament_logic.create_tournament(
            tournament_name="The Sovereign Tournament",
            course_id=course_id,
            start_date="2025-08-15",
            season_number=0,
            week_number=1
        )
        print(f"✅ Created The Sovereign Tournament (ID: {tournament_id}) at {course_name}")
    except Exception as e:
        print(f"❌ Error creating tournament: {e}")
        return
    
    # Test 2: Simulate tournament results with different cut sizes
    print("\n2. Testing Dynamic Payouts with Different Cut Sizes...")
    
    # Create fake player data for testing
    fake = Faker()
    
    def create_test_results(cut_size: int, total_players: int = 120):
        """Create test tournament results with specified cut size"""
        results = []
        
        # Create players who made the cut
        for i in range(cut_size):
            results.append({
                'player_id': i + 1,
                'name': fake.name(),
                'position': i + 1,
                'made_cut': True,
                'total_score': 280 + i  # Simulate scores
            })
        
        # Create players who missed the cut
        for i in range(cut_size, total_players):
            results.append({
                'player_id': i + 1,
                'name': fake.name(),
                'position': i + 1,
                'made_cut': False,
                'total_score': 300 + i  # Higher scores for missed cut
            })
        
        return results
    
    # Test different cut sizes
    test_cut_sizes = [50, 65, 80]
    
    for cut_size in test_cut_sizes:
        print(f"\n   Testing with cut size: {cut_size}")
        
        # Create test results
        test_results = create_test_results(cut_size)
        
        # Calculate dynamic payouts
        try:
            payouts = tournament_logic.calculate_dynamic_payouts(tournament_id, test_results)
            
            # Show summary
            total_purse = sum(p['amount'] for p in payouts)
            winner_payout = next(p['amount'] for p in payouts if p['position'] == 1)
            winner_percentage = next(p['percentage'] for p in payouts if p['position'] == 1)
            
            print(f"     ✅ Cut size: {cut_size}")
            print(f"     💰 Total purse distributed: ${total_purse:,}")
            print(f"     🏆 Winner payout: ${winner_payout:,} ({winner_percentage:.1f}%)")
            
            # Show top 5 payouts
            print(f"     📊 Top 5 payouts:")
            for payout in payouts[:5]:
                print(f"       {payout['position']}. {payout['player_name']}: ${payout['amount']:,} ({payout['percentage']:.2f}%)")
            
            # Verify distribution targets
            top_10_total = sum(p['percentage'] for p in payouts if p['position'] <= 10)
            top_25_total = sum(p['percentage'] for p in payouts if p['position'] <= 25)
            others_total = sum(p['percentage'] for p in payouts if p['position'] > 25)
            
            print(f"     📈 Distribution: Top 10: {top_10_total:.1f}%, Top 25: {top_25_total:.1f}%, Others: {others_total:.1f}%")
            
        except Exception as e:
            print(f"     ❌ Error calculating payouts: {e}")
    
    # Test 3: Test tie handling
    print("\n3. Testing Tie Handling...")
    
    # Create results with ties
    tied_results = create_test_results(60)
    
    # Create some ties
    tied_results[1]['total_score'] = tied_results[0]['total_score']  # Tie for 1st
    tied_results[4]['total_score'] = tied_results[3]['total_score']  # Tie for 4th
    tied_results[9]['total_score'] = tied_results[8]['total_score']  # Tie for 9th
    
    # Re-sort by score and reassign positions
    cut_players = [p for p in tied_results if p['made_cut']]
    cut_players.sort(key=lambda x: x['total_score'])
    
    # Reassign positions (handling ties)
    current_position = 1
    for i, player in enumerate(cut_players):
        if i > 0 and player['total_score'] == cut_players[i-1]['total_score']:
            # This is a tie - keep same position
            player['position'] = cut_players[i-1]['position']
        else:
            player['position'] = current_position
        current_position += 1
    
    try:
        payouts = tournament_logic.calculate_dynamic_payouts(tournament_id, tied_results)
        
        print(f"     ✅ Calculated payouts with ties")
        print(f"     📊 Payouts with ties:")
        for payout in payouts[:10]:
            tied_info = f" (Tied)" if payout['tied'] else ""
            print(f"       {payout['position']}. {payout['player_name']}: ${payout['amount']:,} ({payout['percentage']:.2f}%){tied_info}")
        
    except Exception as e:
        print(f"     ❌ Error calculating payouts with ties: {e}")
    
    # Test 4: Compare with static payout system
    print("\n4. Comparing Dynamic vs Static Payout Systems...")
    
    # Create a regular tournament for comparison
    try:
        regular_tournament_id = tournament_logic.create_tournament(
            tournament_name="Regular Tournament Test",
            course_id=course_id,
            start_date="2025-08-20",
            season_number=0,
            week_number=2
        )
        
        # Get static payout structure
        conn = sqlite3.connect(tournament_logic.tournaments_db_path)
        cur = conn.cursor()
        cur.execute('''
            SELECT finish_position, payout_amount, payout_percentage 
            FROM payout_structure 
            WHERE tournament_id = ? 
            ORDER BY finish_position
        ''', (regular_tournament_id,))
        static_payouts = cur.fetchall()
        conn.close()
        
        print(f"     📊 Static payout system (Regular Tournament):")
        for position, amount, percentage in static_payouts[:5]:
            print(f"       {position}. ${amount:,} ({percentage:.2f}%)")
        
        print(f"     🔄 Dynamic payout system (The Sovereign Tournament):")
        # Use the last calculated payouts from test 3
        for payout in payouts[:5]:
            print(f"       {payout['position']}. ${payout['amount']:,} ({payout['percentage']:.2f}%)")
        
        print(f"\n     💡 Key differences:")
        print(f"        • Static: Pre-calculated for all possible positions")
        print(f"        • Dynamic: Calculated after cut, handles ties, adapts to actual field")
        
    except Exception as e:
        print(f"     ❌ Error in comparison: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Dynamic payout integration test completed!")
    print("\nKey Benefits of Dynamic Payout System:")
    print("• Adapts to actual cut size (not pre-calculated)")
    print("• Handles ties by averaging tied positions")
    print("• Uses anchor positions for key finishes")
    print("• Distributes remaining purse dynamically")
    print("• Perfect for major tournaments with variable cut sizes")

if __name__ == "__main__":
    test_sovereign_dynamic_payouts() 