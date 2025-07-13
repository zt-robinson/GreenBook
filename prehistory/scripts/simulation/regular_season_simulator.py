#!/usr/bin/env python3
"""
Regular Season Simulator for GreenBook Prehistory

This script simulates a regular season with 35 events, each with 72 holes.
It incorporates all player skills into a performance formula for realistic results.
"""

import sqlite3
import random
import os
import csv
from datetime import datetime
from typing import List, Dict, Tuple

class PlayerSkills:
    """Represents a player's golf skills and attributes"""
    
    def __init__(self, player_data: Dict):
        self.player_id = player_data['id']
        self.name = player_data['name']
        self.age = player_data['age']
        self.nationality = player_data['nationality']
        
        # Read existing skills from database
        self.driving_power = player_data['driving_power']
        self.driving_accuracy = player_data['driving_accuracy']
        self.approach_accuracy = player_data['approach_accuracy']
        self.short_game = player_data['short_game']
        self.putting = player_data['putting']
        self.composure = player_data['composure']
        self.confidence = player_data['confidence']
        self.focus = player_data['focus']
        self.risk_tolerance = player_data['risk_tolerance']
        self.mental_fatigue = player_data['mental_fatigue']
        self.consistency = player_data['consistency']
        self.resilience = player_data['resilience']
        
        # Derived attributes
        self.total_skill = self._calculate_total_skill()
    
    def _calculate_total_skill(self) -> float:
        """Calculate overall skill rating"""
        weights = {
            'driving_power': 0.10,
            'driving_accuracy': 0.12,
            'approach_accuracy': 0.15,
            'short_game': 0.08,
            'putting': 0.18,
            'composure': 0.08,
            'confidence': 0.08,
            'focus': 0.08,
            'risk_tolerance': 0.05,
            'mental_fatigue': 0.03,
            'consistency': 0.03,
            'resilience': 0.02
        }
        
        total = (
            self.driving_power * weights['driving_power'] +
            self.driving_accuracy * weights['driving_accuracy'] +
            self.approach_accuracy * weights['approach_accuracy'] +
            self.short_game * weights['short_game'] +
            self.putting * weights['putting'] +
            self.composure * weights['composure'] +
            self.confidence * weights['confidence'] +
            self.focus * weights['focus'] +
            self.risk_tolerance * weights['risk_tolerance'] +
            self.mental_fatigue * weights['mental_fatigue'] +
            self.consistency * weights['consistency'] +
            self.resilience * weights['resilience']
        )
        return total
    
    def get_event_performance(self, event_id: int, seed: int = None) -> float:
        """Calculate total performance for a 72-hole event, with per-event luck"""
        # Use a unique seed for this event/player combination
        if seed is not None:
            event_player_seed = seed + event_id * 1000 + self.player_id
            random.seed(event_player_seed)
        
        # Per-event luck modifier (±25% of total skill) - increased randomness
        event_luck_factor = random.uniform(-0.25, 0.25)
        event_luck = self.total_skill * event_luck_factor
        
        total_performance = 0
        for hole in range(1, 73):
            hole_performance = self.get_hole_performance(hole, seed, event_luck, event_id)
            total_performance += hole_performance
        return total_performance

    def get_hole_performance(self, hole_number: int, seed: int = None, event_luck: float = 0.0, event_id: int = None) -> float:
        """Calculate performance for a single hole, with increased randomness and event luck"""
        # Use a unique seed for each hole to ensure maximum randomness
        if seed is not None and event_id is not None:
            hole_seed = seed + event_id * 1000 + self.player_id * 100 + hole_number
            random.seed(hole_seed)
        
        base_performance = self.total_skill + event_luck
        
        # Increase randomness factor (±80% of base skill) - much more randomness
        randomness_factor = random.uniform(-0.80, 0.80)
        random_adjustment = base_performance * randomness_factor
        
        # Add additional per-hole randomness
        hole_randomness = random.uniform(-0.20, 0.20) * base_performance
        
        fatigue_factor = 1.0 - (hole_number / 72) * 0.05  # Max 5% decline
        pressure_factor = 1.0 + (self.composure - 65) / 1000  # ±3.5%
        
        hole_performance = (base_performance + random_adjustment + hole_randomness) * fatigue_factor * pressure_factor
        return max(0, min(100, hole_performance))

class RegularSeasonSimulator:
    """Simulates a regular season with 35 events"""
    
    def __init__(self, db_path: str, season_num: int = 1):
        self.db_path = db_path
        self.season_num = season_num
        self.players = []
        self.season_results = {}
        
    def load_active_players(self, seed: int = None) -> List[PlayerSkills]:
        """Load all active players and their skills (skills fixed for the season)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, age, nationality, driving_power, driving_accuracy, approach_accuracy, 
                   short_game, putting, composure, confidence, focus, risk_tolerance, 
                   mental_fatigue, consistency, resilience
            FROM players 
            WHERE current_status = 'active'
            ORDER BY id
        """)
        players = []
        for row in cursor.fetchall():
            player_data = {
                'id': row[0],
                'name': row[1],
                'age': row[2],
                'nationality': row[3],
                'driving_power': row[4],
                'driving_accuracy': row[5],
                'approach_accuracy': row[6],
                'short_game': row[7],
                'putting': row[8],
                'composure': row[9],
                'confidence': row[10],
                'focus': row[11],
                'risk_tolerance': row[12],
                'mental_fatigue': row[13],
                'consistency': row[14],
                'resilience': row[15]
            }
            players.append(PlayerSkills(player_data))
        conn.close()
        print(f"📊 Loaded {len(players)} active players")
        return players
    
    def simulate_event(self, event_num: int, players: List[PlayerSkills], season_seed: int = None) -> List[Dict]:
        """Simulate a single event (72 holes) with unique randomness per event"""
        print(f"🏌️  Simulating Event {event_num}...")
        event_seed = (season_seed or 0) + event_num
        event_results = []
        for player in players:
            performance = player.get_event_performance(event_num, event_seed)
            event_results.append({
                'player_id': player.player_id,
                'name': player.name,
                'nationality': player.nationality,
                'performance': performance
            })
        event_results.sort(key=lambda x: x['performance'], reverse=True)
        for i, result in enumerate(event_results):
            result['rank'] = i + 1
            result['points'] = 151 - (i + 1)
        return event_results
    
    def save_event_results(self, event_results: List[Dict], event_num: int):
        """Save event results to database using correct schema columns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO tournaments (season_number, event_number, name, field_size, status)
                VALUES (?, ?, ?, ?, ?)
            """, (self.season_num, event_num, f"Season {self.season_num} Event {event_num}", len(event_results), 'completed'))
            tournament_id = cursor.lastrowid
            for result in event_results:
                cursor.execute("""
                    INSERT INTO tournament_results (tournament_id, player_id, position, total_score, points_earned)
                    VALUES (?, ?, ?, ?, ?)
                """, (tournament_id, result['player_id'], result['rank'], int(result['performance']), result['points']))
            conn.commit()
            print(f"✅ Event {event_num} results saved to database")
        except Exception as e:
            print(f"❌ Error saving event results: {e}")
            conn.rollback()
        finally:
            conn.close()
    

    
    def calculate_season_standings(self, all_event_results: List[List[Dict]]) -> List[Dict]:
        """Calculate final season standings"""
        player_season_points = {}
        
        # Aggregate points from all events
        for event_results in all_event_results:
            for result in event_results:
                player_id = result['player_id']
                if player_id not in player_season_points:
                    player_season_points[player_id] = {
                        'player_id': player_id,
                        'name': result['name'],
                        'nationality': result['nationality'],
                        'total_points': 0,
                        'events_played': 0
                    }
                player_season_points[player_id]['total_points'] += result['points']
                player_season_points[player_id]['events_played'] += 1
        
        # Convert to list and sort by total points
        season_standings = list(player_season_points.values())
        season_standings.sort(key=lambda x: x['total_points'], reverse=True)
        
        return season_standings
    
    def save_season_standings(self, season_standings: List[Dict]):
        """Save season standings to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for i, player in enumerate(season_standings):
                cursor.execute("""
                    INSERT INTO season_player_stats (season_id, player_id, total_season_points, final_rank, events_played)
                    VALUES (?, ?, ?, ?, ?)
                """, (self.season_num, player['player_id'], player['total_points'], i + 1, player['events_played']))
            
            conn.commit()
            print(f"✅ Season {self.season_num} standings saved to database")
            
        except Exception as e:
            print(f"❌ Error saving season standings: {e}")
            conn.rollback()
        finally:
            conn.close()
    

    
    def generate_final_ranking_csv(self, season_standings: List[Dict], all_event_results: List[List[Dict]]):
        """Generate final ranking CSV with player ages and event wins"""
        # Get player ages from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, age FROM players WHERE current_status = 'active'")
        player_ages = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        # Calculate event wins
        event_wins = {}
        for event_results in all_event_results:
            winner_id = event_results[0]['player_id']
            event_wins[winner_id] = event_wins.get(winner_id, 0) + 1
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'regular_seasons', f'season_{self.season_num}')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f'season_{self.season_num}_final_ranking.csv')
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['final_rank', 'player', 'player_age', 'nationality', 'season_points', 'wins'])
            
            for i, player in enumerate(season_standings, 1):
                age = player_ages.get(player['player_id'], 0)
                wins = event_wins.get(player['player_id'], 0)
                writer.writerow([
                    i,
                    player['name'],
                    age,
                    player['nationality'],
                    player['total_points'],
                    wins
                ])
        
        print(f"📊 Final ranking CSV saved: {output_path}")
    
    def generate_event_leaderboard_csv(self, all_event_results: List[List[Dict]]):
        """Generate event leaderboard CSV with all players for each event"""
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'regular_seasons', f'season_{self.season_num}')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f'season_{self.season_num}_event_leaderboard.csv')
        
        # Event type mapping
        event_types = {
            1: "Signature Event #1", 5: "Standard Event #3", 9: "Signature Event #2", 10: "Mini Major",
            15: "Major #1", 20: "Major #2", 26: "Major #3", 31: "Major #3", 35: "Signature Event #7"
        }
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header row
            header = ['season_event', 'event_type', 'event_name']
            for i in range(1, len(all_event_results[0]) + 1):
                header.append(str(i))
            writer.writerow(header)
            
            # Data rows
            for event_num, event_results in enumerate(all_event_results, 1):
                event_type = event_types.get(event_num, f"Standard Event #{event_num}" if event_num % 2 == 0 else f"Standard Invitational #{event_num//2}")
                event_name = event_types.get(event_num, f"Standard Event #{event_num}" if event_num % 2 == 0 else f"Standard Invitational #{event_num//2}")
                
                row = [f"{self.season_num}_{event_num}", event_type, event_name]
                for result in event_results:
                    row.append(result['name'])
                writer.writerow(row)
        
        print(f"📊 Event leaderboard CSV saved: {output_path}")
    
    def generate_bottom_players_csv(self, season_standings: List[Dict], all_event_results: List[List[Dict]]):
        """Generate bottom 50 players CSV for relegated players"""
        # Get player ages from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, age FROM players WHERE current_status = 'active'")
        player_ages = {row[0]: row[1] for row in cursor.fetchall()}
        conn.close()
        
        # Calculate event wins
        event_wins = {}
        for event_results in all_event_results:
            winner_id = event_results[0]['player_id']
            event_wins[winner_id] = event_wins.get(winner_id, 0) + 1
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'regular_seasons', f'season_{self.season_num}')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, f'season_{self.season_num}_bottom_50_players.csv')
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['final_rank', 'player', 'player_age', 'nationality', 'season_points', 'wins'])
            
            # Bottom 50 players (ranks 101-150)
            for i in range(101, 151):
                if i <= len(season_standings):
                    player = season_standings[i-1]  # 0-indexed
                    age = player_ages.get(player['player_id'], 0)
                    wins = event_wins.get(player['player_id'], 0)
                    writer.writerow([
                        i,
                        player['name'],
                        age,
                        player['nationality'],
                        player['total_points'],
                        wins
                    ])
        
        print(f"📊 Bottom 50 players CSV saved: {output_path}")
    
    def run_season(self, seed: int = None):
        print(f"🏆 REGULAR SEASON {self.season_num} SIMULATION")
        print("=" * 60)
        players = self.load_active_players(seed)
        if not players:
            print("❌ No active players found!")
            return False
        all_event_results = []
        event_wins = {p.player_id: 0 for p in players}
        for event_num in range(1, 36):
            event_results = self.simulate_event(event_num, players, seed)
            self.save_event_results(event_results, event_num)
            all_event_results.append(event_results)
            # Track event winner
            winner_id = event_results[0]['player_id']
            event_wins[winner_id] += 1
        season_standings = self.calculate_season_standings(all_event_results)
        # Attach event wins to season standings
        for player in season_standings:
            player['event_wins'] = event_wins.get(player['player_id'], 0)
        self.save_season_standings(season_standings)
        
        # Generate CSV files
        self.generate_final_ranking_csv(season_standings, all_event_results)
        self.generate_event_leaderboard_csv(all_event_results)
        self.generate_bottom_players_csv(season_standings, all_event_results)
        
        print(f"\n🎉 Season {self.season_num} simulation complete!")
        print(f"🏆 Season winner: {season_standings[0]['name']} ({season_standings[0]['total_points']} points)")
        return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Simulate a regular season")
    parser.add_argument('--season', type=int, default=1, help='Season number (default: 1)')
    parser.add_argument('--seed', type=int, help='Random seed for reproducibility')
    args = parser.parse_args()
    
    # Use season number as seed if no seed provided, ensuring different results per season
    if args.seed is None:
        args.seed = args.season * 1000 + 42  # Different seed for each season
    
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
    simulator = RegularSeasonSimulator(db_path, args.season)
    
    success = simulator.run_season(args.seed)
    if success:
        print("\n✅ Season simulation completed successfully!")
    else:
        print("\n❌ Season simulation failed!")

if __name__ == "__main__":
    main() 