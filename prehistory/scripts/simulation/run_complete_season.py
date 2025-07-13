#!/usr/bin/env python3
"""
Complete Season Runner for GreenBook Prehistory

This script orchestrates the complete season cycle:
1. Simulate 35 events for all active players
2. Age all players by 1 year
3. Cull bottom 50 players (mark as inactive)
4. Generate 50 new players for next season

All steps are validated and reported for transparency.
"""

import os
import sys
import sqlite3
import subprocess
import argparse
from datetime import datetime
from typing import Dict, List, Tuple

class SeasonRunner:
    """Orchestrates the complete season cycle"""
    
    def __init__(self, season_num: int, skip_new_players: bool = False):
        self.season_num = season_num
        self.skip_new_players = skip_new_players
        self.db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
        self.scripts_dir = os.path.join(os.path.dirname(__file__), '..')
        
        # Track statistics
        self.stats = {
            'initial_active_players': 0,
            'final_active_players': 0,
            'players_aged': 0,
            'players_culled': 0,
            'new_players_generated': 0,
            'season_winner': None,
            'season_points': 0
        }
    
    def validate_database(self) -> bool:
        """Validate database exists and has required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if required tables exist
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('players', 'tournaments', 'tournament_results', 'season_player_stats')")
            tables = [row[0] for row in cursor.fetchall()]
            required_tables = ['players', 'tournaments', 'tournament_results', 'season_player_stats']
            
            if not all(table in tables for table in required_tables):
                print("❌ Database missing required tables!")
                return False
            
            # Check if season already exists
            cursor.execute("SELECT COUNT(*) FROM tournaments WHERE season_number = ?", (self.season_num,))
            existing_tournaments = cursor.fetchone()[0]
            
            if existing_tournaments > 0:
                print(f"⚠️  Season {self.season_num} already has {existing_tournaments} tournaments!")
                response = input("Continue anyway? (y/N): ")
                if response.lower() != 'y':
                    return False
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Database validation failed: {e}")
            return False
    
    def get_player_counts(self) -> Tuple[int, int]:
        """Get current active and inactive player counts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM players WHERE current_status = 'active'")
        active_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM players WHERE current_status != 'active'")
        inactive_count = cursor.fetchone()[0]
        
        conn.close()
        return active_count, inactive_count
    
    def run_season_simulation(self) -> bool:
        """Run the season simulation"""
        print(f"🏆 STEP 1: Simulating Season {self.season_num}")
        print("=" * 50)
        
        # Get initial player count
        active_count, inactive_count = self.get_player_counts()
        self.stats['initial_active_players'] = active_count
        print(f"📊 Starting with {active_count} active players")
        
        # Run season simulator
        simulator_script = os.path.join(self.scripts_dir, 'simulation', 'regular_season_simulator.py')
        cmd = [sys.executable, simulator_script, '--season', str(self.season_num)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(self.db_path))
            
            if result.returncode != 0:
                print(f"❌ Season simulation failed!")
                print(f"Error: {result.stderr}")
                return False
            
            print(result.stdout)
            
            # Extract season winner from output
            for line in result.stdout.split('\n'):
                if "Season winner:" in line:
                    winner_info = line.split("Season winner:")[1].strip()
                    self.stats['season_winner'] = winner_info.split("(")[0].strip()
                    points_str = winner_info.split("(")[1].split(")")[0].split()[0]
                    self.stats['season_points'] = int(points_str)
                    break
            
            return True
            
        except Exception as e:
            print(f"❌ Season simulation error: {e}")
            return False
    
    def age_all_players(self) -> bool:
        """Age all players by 1 year"""
        print(f"📈 STEP 2: Aging all players by 1 year")
        print("=" * 50)
        
        # Get player counts before aging
        active_count, inactive_count = self.get_player_counts()
        print(f"📊 Before aging: {active_count} active, {inactive_count} inactive players")
        
        # Run aging script
        aging_script = os.path.join(self.scripts_dir, 'player_management', 'age_up_players.py')
        cmd = [sys.executable, aging_script]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(self.db_path))
            
            if result.returncode != 0:
                print(f"❌ Player aging failed!")
                print(f"Error: {result.stderr}")
                return False
            
            print(result.stdout)
            
            # Verify aging worked
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM players")
            total_players = cursor.fetchone()[0]
            conn.close()
            
            self.stats['players_aged'] = total_players
            print(f"✅ Aged {total_players} players successfully")
            
            return True
            
        except Exception as e:
            print(f"❌ Player aging error: {e}")
            return False
    
    def cull_bottom_players(self) -> bool:
        """Cull bottom 50 players"""
        print(f"🗑️  STEP 3: Culling bottom 50 players")
        print("=" * 50)
        
        # Get player counts before culling
        active_count, inactive_count = self.get_player_counts()
        print(f"📊 Before culling: {active_count} active, {inactive_count} inactive players")
        
        # Run culling script
        culling_script = os.path.join(self.scripts_dir, 'player_management', 'cull_players_regular_season.py')
        cmd = [sys.executable, culling_script, '--season', str(self.season_num)]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(self.db_path))
            
            if result.returncode != 0:
                print(f"❌ Player culling failed!")
                print(f"Error: {result.stderr}")
                return False
            
            print(result.stdout)
            
            # Verify culling worked
            active_count_after, inactive_count_after = self.get_player_counts()
            culled_count = active_count - active_count_after
            
            if culled_count != 50:
                print(f"⚠️  Expected to cull 50 players, but culled {culled_count}")
                return False
            
            self.stats['players_culled'] = culled_count
            print(f"✅ Culled {culled_count} players successfully")
            print(f"📊 After culling: {active_count_after} active, {inactive_count_after} inactive players")
            
            return True
            
        except Exception as e:
            print(f"❌ Player culling error: {e}")
            return False
    
    def generate_new_players(self) -> bool:
        """Generate 50 new players for next season (without aging existing players)"""
        print(f"👥 STEP 4: Generating 50 new players")
        print("=" * 50)
        
        # Get player counts before generation
        active_count, inactive_count = self.get_player_counts()
        print(f"📊 Before generation: {active_count} active, {inactive_count} inactive players")
        
        # Create directory for next season's CSV files
        next_season = self.season_num + 1
        next_season_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'regular_seasons', f'season_{next_season}')
        os.makedirs(next_season_dir, exist_ok=True)
        print(f"📁 Created directory for Season {next_season}: {next_season_dir}")
        
        # Create a temporary modified version of generate_players.py that doesn't age players
        # We'll do this by creating a wrapper script that skips the aging step
        temp_script = self._create_temp_generation_script()
        
        try:
            # Run our modified generation script
            cmd = [sys.executable, temp_script, '--num', '50', '--season', str(next_season), '--event', '0', '--suffix', f'S{next_season}']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(self.db_path))
            
            # Clean up temp script
            os.remove(temp_script)
            
            if result.returncode != 0:
                print(f"❌ Player generation failed!")
                print(f"Error: {result.stderr}")
                return False
            
            print(result.stdout)
            
            # Verify generation worked
            active_count_after, inactive_count_after = self.get_player_counts()
            generated_count = active_count_after - active_count
            
            if generated_count != 50:
                print(f"⚠️  Expected to generate 50 players, but generated {generated_count}")
                return False
            
            self.stats['new_players_generated'] = generated_count
            self.stats['final_active_players'] = active_count_after
            print(f"✅ Generated {generated_count} new players successfully")
            print(f"📊 After generation: {active_count_after} active, {inactive_count_after} inactive players")
            
            # Fix CSV formatting for new players file
            self._fix_new_players_csv_format()
            
            return True
            
        except Exception as e:
            print(f"❌ Player generation error: {e}")
            # Clean up temp script on error
            if os.path.exists(temp_script):
                os.remove(temp_script)
            return False
    
    def _create_temp_generation_script(self) -> str:
        """Create a temporary version of generate_players.py that skips aging"""
        original_script = os.path.join(self.scripts_dir, 'player_generation', 'generate_players.py')
        temp_script = os.path.join(os.path.dirname(__file__), 'temp_generate_players_no_aging.py')
        
        with open(original_script, 'r') as f:
            content = f.read()
        
        # Remove the aging line from the generate_players function
        # Find the line that says "cursor.execute("UPDATE players SET age = age + 1")"
        lines = content.split('\n')
        modified_lines = []
        skip_next_line = False
        
        for line in lines:
            if 'cursor.execute("UPDATE players SET age = age + 1")' in line:
                # Skip this line and the next line (which is usually conn.commit())
                skip_next_line = True
                continue
            elif skip_next_line and 'conn.commit()' in line:
                skip_next_line = False
                continue
            else:
                modified_lines.append(line)
        
        modified_content = '\n'.join(modified_lines)
        
        with open(temp_script, 'w') as f:
            f.write(modified_content)
        
        return temp_script
    
    def _fix_new_players_csv_format(self):
        """Fix the CSV formatting for the new players file (convert pipes to commas)"""
        next_season = self.season_num + 1
        csv_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'regular_seasons', f'season_{next_season}', f'season_{next_season}_new_players.csv')
        
        if os.path.exists(csv_path):
            try:
                # Read the file and convert pipes to commas (except header)
                with open(csv_path, 'r') as f:
                    content = f.read()
                
                lines = content.split('\n')
                if len(lines) > 1:
                    # Keep header as is, convert data lines
                    header = lines[0]
                    data_lines = lines[1:]
                    
                    # Convert pipes to commas in data lines
                    converted_data = []
                    for line in data_lines:
                        if line.strip():  # Skip empty lines
                            converted_line = line.replace('|', ',')
                            converted_data.append(converted_line)
                    
                    # Write back with proper CSV format
                    with open(csv_path, 'w') as f:
                        f.write(header + '\n')
                        f.write('\n'.join(converted_data))
                    
                    print(f"✅ Fixed CSV formatting for Season {next_season} new players file")
                
            except Exception as e:
                print(f"⚠️  Warning: Could not fix CSV formatting: {e}")
    
    def validate_complete_cycle(self) -> bool:
        """Validate that all steps were completed correctly"""
        print(f"🔍 STEP 5: Validating complete cycle")
        print("=" * 50)
        
        validation_results = []
        
        # 1. Check tournament count
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tournaments WHERE season_number = ?", (self.season_num,))
        tournament_count = cursor.fetchone()[0]
        
        if tournament_count == 35:
            validation_results.append(("✅ Season tournaments", f"35 tournaments created for Season {self.season_num}"))
        else:
            validation_results.append(("❌ Season tournaments", f"Expected 35, found {tournament_count}"))
        
        # 2. Check player counts
        cursor.execute("SELECT COUNT(*) FROM players WHERE current_status = 'active'")
        final_active_count = cursor.fetchone()[0]
        
        if final_active_count == 150:
            validation_results.append(("✅ Final active players", f"150 active players (correct)"))
        else:
            validation_results.append(("❌ Final active players", f"Expected 150, found {final_active_count}"))
        
        # 3. Check new players were created (skip if --no-new-players flag is set)
        if not self.skip_new_players:
            next_season = self.season_num + 1
            cursor.execute("SELECT COUNT(*) FROM players WHERE name LIKE ? AND current_status = 'active'", (f'%S{next_season}',))
            new_player_count = cursor.fetchone()[0]
            
            if new_player_count == 50:
                validation_results.append(("✅ New players generated", f"50 new S{next_season} players created"))
            else:
                validation_results.append(("❌ New players generated", f"Expected 50, found {new_player_count}"))
        else:
            validation_results.append(("⏭️  New players generated", "Skipped (--no-new-players flag)"))
        
        # 4. Check that returning players were aged correctly
        if not self.skip_new_players:
            cursor.execute("""
                SELECT COUNT(*) FROM players 
                WHERE current_status = 'active' 
                AND name NOT LIKE ? 
                AND age > 18
            """, (f'%S{next_season}',))
            aged_players_count = cursor.fetchone()[0]
            
            if aged_players_count == 100:
                validation_results.append(("✅ Returning players aged", f"100 returning players aged correctly"))
            else:
                validation_results.append(("❌ Returning players aged", f"Expected 100, found {aged_players_count}"))
        else:
            # If no new players, all active players should be aged
            cursor.execute("""
                SELECT COUNT(*) FROM players 
                WHERE current_status = 'active' 
                AND age > 18
            """)
            aged_players_count = cursor.fetchone()[0]
            
            if aged_players_count == 100:
                validation_results.append(("✅ Returning players aged", f"100 returning players aged correctly"))
            else:
                validation_results.append(("❌ Returning players aged", f"Expected 100, found {aged_players_count}"))
        
        # 5. Check that new players have correct ages (skip if --no-new-players flag is set)
        if not self.skip_new_players:
            cursor.execute("""
                SELECT COUNT(*) FROM players 
                WHERE name LIKE ? 
                AND current_status = 'active'
                AND age BETWEEN 19 AND 22
            """, (f'%S{next_season}',))
            correct_age_new_players = cursor.fetchall()[0]
            
            if correct_age_new_players == 50:
                validation_results.append(("✅ New player ages", f"50 new players with ages 19-22"))
            else:
                validation_results.append(("❌ New player ages", f"Expected 50, found {correct_age_new_players}"))
        else:
            validation_results.append(("⏭️  New player ages", "Skipped (--no-new-players flag)"))
        
        # 6. Check season standings were saved
        cursor.execute("SELECT COUNT(*) FROM season_player_stats WHERE season_id = ?", (self.season_num,))
        season_stats_count = cursor.fetchone()[0]
        
        if season_stats_count == 150:
            validation_results.append(("✅ Season standings", f"150 player season stats saved"))
        else:
            validation_results.append(("❌ Season standings", f"Expected 150, found {season_stats_count}"))
        
        # 7. Check CSV files were created
        csv_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'regular_seasons', f'season_{self.season_num}')
        expected_files = [
            f'season_{self.season_num}_final_ranking.csv',
            f'season_{self.season_num}_event_leaderboard.csv',
            f'season_{self.season_num}_bottom_50_players.csv'
        ]
        
        missing_files = []
        for file in expected_files:
            if not os.path.exists(os.path.join(csv_dir, file)):
                missing_files.append(file)
        
        if not missing_files:
            validation_results.append(("✅ CSV files", "All expected CSV files created"))
        else:
            validation_results.append(("❌ CSV files", f"Missing: {', '.join(missing_files)}"))
        
        # 8. Check new players CSV for next season (skip if --no-new-players flag is set)
        if not self.skip_new_players:
            next_season_csv = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'regular_seasons', f'season_{next_season}', f'season_{next_season}_new_players.csv')
            if os.path.exists(next_season_csv):
                validation_results.append(("✅ Next season CSV", f"New players CSV created for Season {next_season}"))
            else:
                validation_results.append(("❌ Next season CSV", f"Missing new players CSV for Season {next_season}"))
        else:
            validation_results.append(("⏭️  Next season CSV", "Skipped (--no-new-players flag)"))
        
        conn.close()
        
        # Print validation results
        print("🔍 VALIDATION RESULTS:")
        print("=" * 50)
        all_passed = True
        for status, message in validation_results:
            print(f"{status}: {message}")
            if status.startswith("❌"):
                all_passed = False
        
        print("=" * 50)
        if all_passed:
            print("🎉 ALL VALIDATIONS PASSED!")
        else:
            print("⚠️  SOME VALIDATIONS FAILED!")
        
        return all_passed
    
    def generate_completion_report(self):
        """Generate a comprehensive completion report"""
        print(f"📊 STEP 6: Generating completion report")
        print("=" * 50)
        
        # Run validation first
        validation_passed = self.validate_complete_cycle()
        
        report = []
        report.append(f"# 🏆 Season {self.season_num} Complete Cycle Report")
        report.append("")
        report.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        report.append("")
        report.append("## 📈 Season Summary")
        report.append("")
        report.append(f"- **Season:** {self.season_num}")
        report.append(f"- **Season Winner:** {self.stats['season_winner']} ({self.stats['season_points']} points)")
        report.append(f"- **Events Simulated:** 35")
        report.append("")
        report.append("## 👥 Player Management Summary")
        report.append("")
        report.append(f"- **Initial Active Players:** {self.stats['initial_active_players']}")
        report.append(f"- **Players Aged:** {self.stats['players_aged']}")
        report.append(f"- **Players Culled:** {self.stats['players_culled']}")
        report.append(f"- **New Players Generated:** {self.stats['new_players_generated']}")
        report.append(f"- **Final Active Players:** {self.stats['final_active_players']}")
        report.append("")
        report.append("## ✅ Process Validation")
        report.append("")
        report.append("- ✅ Season simulation completed successfully")
        report.append("- ✅ All players aged by 1 year")
        report.append("- ✅ Bottom 50 players culled")
        if not self.skip_new_players:
            report.append("- ✅ 50 new players generated (without double-aging)")
        else:
            report.append("- ⏭️  New player generation skipped (--no-new-players flag)")
        report.append("")
        report.append("## 🔍 Validation Results")
        report.append("")
        if validation_passed:
            report.append("**🎉 ALL VALIDATIONS PASSED!**")
        else:
            report.append("**⚠️  SOME VALIDATIONS FAILED!**")
        report.append("")
        report.append("## 🎯 Ready for Next Season")
        report.append("")
        report.append(f"The database is now ready for Season {self.season_num + 1} with {self.stats['final_active_players']} active players.")
        
        # Save report
        report_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', f'season_{self.season_num}_complete_cycle_report.md')
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))
        
        print(f"📊 Completion report saved: {report_path}")
        print('\n'.join(report))
    
    def run_complete_season(self) -> bool:
        """Run the complete season cycle"""
        print(f"🚀 STARTING COMPLETE SEASON {self.season_num} CYCLE")
        print("=" * 60)
        print(f"Database: {self.db_path}")
        print(f"Scripts: {self.scripts_dir}")
        print("=" * 60)
        
        # Step 0: Validate database
        if not self.validate_database():
            return False
        
        # Step 1: Simulate season
        if not self.run_season_simulation():
            return False
        
        # Step 2: Age all players
        if not self.age_all_players():
            return False
        
        # Step 3: Cull bottom players
        if not self.cull_bottom_players():
            return False
        
        # Step 4: Generate new players (skip if --no-new-players flag is set)
        if not self.skip_new_players:
            if not self.generate_new_players():
                return False
        else:
            print(f"⏭️  STEP 4: Skipping new player generation (--no-new-players flag)")
            print("=" * 50)
            print("📊 No new players will be generated for next season")
            self.stats['new_players_generated'] = 0
        
        # Step 5: Generate completion report
        self.generate_completion_report()
        
        print(f"\n🎉 SEASON {self.season_num} COMPLETE CYCLE SUCCESSFUL!")
        print("=" * 60)
        return True

def main():
    parser = argparse.ArgumentParser(description="Run complete season cycle")
    parser.add_argument('--season', type=int, required=True, help='Season number to run')
    parser.add_argument('--no-new-players', action='store_true', help='Skip new player generation (for final season)')
    args = parser.parse_args()
    
    runner = SeasonRunner(args.season, args.no_new_players)
    success = runner.run_complete_season()
    
    if success:
        print("\n✅ Complete season cycle finished successfully!")
        sys.exit(0)
    else:
        print("\n❌ Complete season cycle failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 