#!/usr/bin/env python3
"""
Run Complete Gauntlet Season
Simulates all 10 Gauntlet tournaments and generates final leaderboard.
"""

import sqlite3
import os
from datetime import datetime
from gauntlet_tournament_simulator import GauntletTournamentSimulator

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), '../../../data/prehistory.db')

class GauntletSeasonRunner:
    def __init__(self):
        self.db_path = DB_PATH
        self.simulator = GauntletTournamentSimulator()
        
    def get_gauntlet_tournaments(self):
        """Get all Gauntlet tournaments from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, name, event_number, start_date
            FROM tournaments 
            WHERE season_type = 'gauntlet' AND season_number = 0
            ORDER BY event_number
        ''')
        tournaments = cursor.fetchall()
        conn.close()
        return tournaments
    
    def update_simulation_state(self, current_event):
        """Update the simulation state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE simulation_state 
                SET current_phase = ?, current_season = ?, current_event = ?, last_updated = ?
                WHERE id = 1
            ''', (
                'gauntlet',
                0,  # Season 0
                current_event,
                datetime.now().isoformat()
            ))
            conn.commit()
        except Exception as e:
            print(f"❌ Error updating simulation state: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def calculate_cumulative_points(self):
        """Calculate cumulative points for all players after all tournaments"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                tr.player_id,
                p.name,
                p.age,
                p.nationality,
                SUM(tr.points_earned) as total_points,
                COUNT(tr.tournament_id) as events_played,
                COUNT(CASE WHEN tr.position = 1 THEN 1 END) as wins,
                COUNT(CASE WHEN tr.position <= 10 THEN 1 END) as top_10s
            FROM tournament_results tr
            JOIN players p ON tr.player_id = p.id
            JOIN tournaments t ON tr.tournament_id = t.id
            WHERE t.season_type = 'gauntlet' AND t.season_number = 0
            GROUP BY tr.player_id, p.name, p.age, p.nationality
            ORDER BY total_points DESC
        ''')
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def save_season_player_stats(self, season_id, cumulative_results):
        """Save season player statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for i, result in enumerate(cumulative_results):
                player_id, name, age, nationality, total_points, events_played, wins, top_10s = result
                
                cursor.execute('''
                    INSERT INTO season_player_stats (
                        season_id, player_id, total_season_points, final_rank,
                        events_played, wins, top_10s, made_cuts, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    season_id,
                    player_id,
                    total_points,
                    i + 1,  # Final rank
                    events_played,
                    wins,
                    top_10s,
                    events_played,  # All players make cut in Gauntlet
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            print(f"💾 Saved season player stats for {len(cumulative_results)} players")
            
        except Exception as e:
            print(f"❌ Error saving season player stats: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def save_season_event_results(self, season_id):
        """Save event-by-event results for the season"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT 
                    tr.tournament_id,
                    tr.player_id,
                    tr.position as event_rank,
                    tr.points_earned,
                    tr.total_score
                FROM tournament_results tr
                JOIN tournaments t ON tr.tournament_id = t.id
                WHERE t.season_type = 'gauntlet' AND t.season_number = 0
                ORDER BY tr.tournament_id, tr.position
            ''')
            
            results = cursor.fetchall()
            
            for result in results:
                tournament_id, player_id, event_rank, points_earned, total_score = result
                
                cursor.execute('''
                    INSERT INTO season_event_results (
                        season_id, tournament_id, player_id, event_rank, points_earned, total_score, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    season_id,
                    tournament_id,
                    player_id,
                    event_rank,
                    points_earned,
                    total_score,
                    datetime.now().isoformat()
                ))
            
            conn.commit()
            print(f"💾 Saved event-by-event results for the season")
            
        except Exception as e:
            print(f"❌ Error saving season event results: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def run_gauntlet_season(self):
        """Run the complete Gauntlet season simulation"""
        print("🏌️  GAUNTLET SEASON SIMULATION")
        print("=" * 60)
        
        # Get tournaments
        tournaments = self.get_gauntlet_tournaments()
        if not tournaments:
            print("❌ No Gauntlet tournaments found. Run setup_gauntlet_season.py first.")
            return
        
        print(f"📅 Found {len(tournaments)} tournaments to simulate")
        print()
        
        # Simulate each tournament
        for i, (tournament_id, tournament_name, event_number, start_date) in enumerate(tournaments, 1):
            print(f"🎯 Tournament {i}/{len(tournaments)}")
            print(f"   Event: {tournament_name}")
            print(f"   Date: {start_date}")
            print()
            
            # Update simulation state
            self.update_simulation_state(event_number)
            
            # Simulate tournament
            results = self.simulator.simulate_tournament(tournament_name, tournament_id, event_number)
            
            print(f"✅ Tournament {i} complete!")
            print(f"   Winner: {results[0]['name']} ({results[0]['total_score']} strokes)")
            print(f"   Points earned: {results[0]['points_earned']}")
            print("-" * 60)
            print()
        
        # Calculate final leaderboard
        print("📊 Calculating final Gauntlet season leaderboard...")
        cumulative_results = self.calculate_cumulative_points()
        
        # Get season ID
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM seasons WHERE season_number = 0 AND season_type = "gauntlet"')
        season_id = cursor.fetchone()[0]
        conn.close()
        
        # Save season statistics
        self.save_season_player_stats(season_id, cumulative_results)
        self.save_season_event_results(season_id)
        
        # Print final leaderboard
        print("\n🏆 FINAL GAUNTLET SEASON LEADERBOARD")
        print("=" * 80)
        print(f"{'Rank':<4} {'Player':<25} {'Age':<3} {'Nationality':<15} {'Points':<6} {'Events':<6} {'Wins':<4} {'Top10s':<6}")
        print("-" * 80)
        
        for i, result in enumerate(cumulative_results[:50], 1):  # Show top 50
            player_id, name, age, nationality, total_points, events_played, wins, top_10s = result
            print(f"{i:<4} {name:<25} {age:<3} {nationality:<15} {total_points:<6} {events_played:<6} {wins:<4} {top_10s:<6}")
        
        print("\n✅ Gauntlet season simulation complete!")
        print(f"   Total players: {len(cumulative_results)}")
        print(f"   Season winner: {cumulative_results[0][1]} ({cumulative_results[0][4]} points)")
        print(f"   Top 100 players will advance to regular seasons")
        print(f"   Bottom 500 players will be culled")
        print(f"\n⏸️  Ready for player culling process...")
        
        return cumulative_results

def main():
    """Main function"""
    runner = GauntletSeasonRunner()
    results = runner.run_gauntlet_season()
    
    if results:
        print("\n🎉 Gauntlet season tournaments complete!")
        print("Next step: Implement player culling logic")
        print("Then: Add 50 new players for Season 1")

if __name__ == "__main__":
    main() 