#!/usr/bin/env python3
"""
Gauntlet Tournament Simulator
Simulates 72-hole tournaments for the Gauntlet season with 600 players.
"""

import sqlite3
import os
import random
import math
from datetime import datetime, timedelta

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '../../../data/prehistory.db')

class GauntletTournamentSimulator:
    def __init__(self):
        self.db_path = DB_PATH
        
    def get_all_players(self):
        """Get all active players from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, age, nationality,
                   driving_power, driving_accuracy, approach_accuracy, short_game, putting,
                   composure, confidence, focus, risk_tolerance, mental_fatigue, consistency, resilience
            FROM players 
            WHERE current_status = 'active'
            ORDER BY id
        ''')
        players = cursor.fetchall()
        conn.close()
        return players
    
    def calculate_hole_difficulty(self):
        """Generate a random difficulty rating for a hole (0-100)"""
        # Base difficulty with some variation
        base_difficulty = random.uniform(30, 85)
        # Add some randomness for variety
        variation = random.uniform(-10, 10)
        return max(0, min(100, base_difficulty + variation))
    
    def calculate_player_performance(self, player_attrs, hole_difficulty):
        """
        Calculate a player's performance on a hole based on their attributes vs. hole difficulty.
        Returns a performance score that will be converted to a stroke count.
        """
        # Physical skills (weighted average)
        physical_score = (
            player_attrs['driving_power'] * 0.25 +
            player_attrs['driving_accuracy'] * 0.25 +
            player_attrs['approach_accuracy'] * 0.20 +
            player_attrs['short_game'] * 0.15 +
            player_attrs['putting'] * 0.15
        )
        
        # Mental skills (weighted average)
        mental_score = (
            player_attrs['composure'] * 0.20 +
            player_attrs['confidence'] * 0.15 +
            player_attrs['focus'] * 0.20 +
            player_attrs['risk_tolerance'] * 0.10 +
            player_attrs['mental_fatigue'] * 0.10 +
            player_attrs['consistency'] * 0.15 +
            player_attrs['resilience'] * 0.10
        )
        
        # Overall player rating (70% physical, 30% mental)
        player_rating = (physical_score * 0.7) + (mental_score * 0.3)
        
        # Performance calculation: player rating vs hole difficulty
        # Higher player rating and lower hole difficulty = better performance
        performance_ratio = player_rating / (hole_difficulty + 1)  # +1 to avoid division by zero
        
        # Convert to a performance score (0-100)
        performance_score = min(100, max(0, performance_ratio * 50))
        
        # Add some randomness for realism
        randomness = random.uniform(-15, 15)
        final_performance = min(100, max(0, performance_score + randomness))
        
        return final_performance
    
    def performance_to_strokes(self, performance_score, hole_par=4):
        """
        Convert performance score to stroke count.
        Higher performance = fewer strokes.
        """
        # Performance score of 100 = par
        # Performance score of 0 = par + 4 strokes
        stroke_adjustment = (100 - performance_score) / 25  # 0-4 stroke range
        strokes = hole_par + stroke_adjustment
        
        # Round to nearest whole number, minimum 1 stroke
        return max(1, round(strokes))
    
    def simulate_player_round(self, player_attrs):
        """Simulate a player's 18-hole round"""
        round_score = 0
        
        for hole in range(18):
            # Determine par for this hole (mostly par 4s, some 3s and 5s)
            if hole < 4:  # First 4 holes
                par = random.choice([3, 4, 4, 4])
            elif hole < 14:  # Middle holes
                par = random.choice([4, 4, 4, 4, 4, 4, 4, 4, 4, 4])
            else:  # Last 4 holes
                par = random.choice([4, 4, 5, 4])
            
            # Calculate hole difficulty
            hole_difficulty = self.calculate_hole_difficulty()
            
            # Calculate player performance
            performance = self.calculate_player_performance(player_attrs, hole_difficulty)
            
            # Convert to strokes
            strokes = self.performance_to_strokes(performance, par)
            round_score += strokes
        
        return round_score
    
    def simulate_tournament(self, tournament_name, tournament_id, event_number):
        """Simulate a complete 72-hole tournament"""
        print(f"🏌️  Simulating {tournament_name} (Event {event_number})")
        print("=" * 60)
        
        # Get all players
        players = self.get_all_players()
        print(f"📊 Field size: {len(players)} players")
        
        # Simulate tournament results
        tournament_results = []
        
        for player in players:
            player_id, name, age, nationality = player[0:4]
            player_attrs = {
                'driving_power': player[4],
                'driving_accuracy': player[5],
                'approach_accuracy': player[6],
                'short_game': player[7],
                'putting': player[8],
                'composure': player[9],
                'confidence': player[10],
                'focus': player[11],
                'risk_tolerance': player[12],
                'mental_fatigue': player[13],
                'consistency': player[14],
                'resilience': player[15]
            }
            
            # Simulate 4 rounds
            round_1 = self.simulate_player_round(player_attrs)
            round_2 = self.simulate_player_round(player_attrs)
            round_3 = self.simulate_player_round(player_attrs)
            round_4 = self.simulate_player_round(player_attrs)
            
            total_score = round_1 + round_2 + round_3 + round_4
            
            tournament_results.append({
                'player_id': player_id,
                'name': name,
                'total_score': total_score,
                'round_1': round_1,
                'round_2': round_2,
                'round_3': round_3,
                'round_4': round_4
            })
        
        # Sort by total score (lower is better)
        tournament_results.sort(key=lambda x: x['total_score'])
        
        # Assign positions and points
        for i, result in enumerate(tournament_results):
            position = i + 1
            points_earned = 600 - i  # 1st gets 600, 2nd gets 599, etc.
            result['position'] = position
            result['points_earned'] = points_earned
        
        # Save results to database
        self.save_tournament_results(tournament_id, tournament_results)
        
        # Print top 10 results
        print(f"\n🏆 Top 10 Results:")
        print("-" * 80)
        for i, result in enumerate(tournament_results[:10]):
            print(f"{result['position']:2d}. {result['name']:<20} {result['total_score']:3d} ({result['round_1']:2d}-{result['round_2']:2d}-{result['round_3']:2d}-{result['round_4']:2d}) {result['points_earned']:3d} pts")
        
        print(f"\n✅ Tournament simulation complete!")
        return tournament_results
    
    def save_tournament_results(self, tournament_id, results):
        """Save tournament results to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for result in results:
                cursor.execute('''
                    INSERT INTO tournament_results (
                        tournament_id, player_id, position, total_score,
                        round_1_score, round_2_score, round_3_score, round_4_score,
                        points_earned, made_cut, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tournament_id,
                    result['player_id'],
                    result['position'],
                    result['total_score'],
                    result['round_1'],
                    result['round_2'],
                    result['round_3'],
                    result['round_4'],
                    result['points_earned'],
                    1,  # All players make cut in Gauntlet
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            print(f"💾 Saved {len(results)} tournament results to database")
            
        except Exception as e:
            print(f"❌ Error saving tournament results: {e}")
            conn.rollback()
        finally:
            conn.close()

def main():
    """Test the tournament simulator"""
    simulator = GauntletTournamentSimulator()
    
    # Test with a sample tournament
    tournament_name = "Gauntlet Event #1"
    tournament_id = 1
    event_number = 1
    
    results = simulator.simulate_tournament(tournament_name, tournament_id, event_number)
    
    print(f"\n📊 Tournament Summary:")
    print(f"   Total players: {len(results)}")
    print(f"   Winner: {results[0]['name']} ({results[0]['total_score']} strokes)")
    print(f"   Runner-up: {results[1]['name']} ({results[1]['total_score']} strokes)")
    print(f"   Last place: {results[-1]['name']} ({results[-1]['total_score']} strokes)")

if __name__ == "__main__":
    main() 