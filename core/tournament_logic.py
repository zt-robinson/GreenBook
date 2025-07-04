import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from .event_types import event_type_manager
from .payout_calculator import PayoutCalculator
import json

class TournamentLogic:
    """Handles tournament creation and management logic"""
    
    def __init__(self):
        self.tournaments_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_tournaments.db')
        self.players_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_players.db')
        self.courses_db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')
    
    def create_tournament(self, tournament_name: str, course_id: int, start_date: str, 
                         season_number: int, week_number: int, event_type: str = None,
                         overrides: Dict[str, Any] = None) -> int:
        """
        Create a new tournament in the database
        
        Args:
            tournament_name: Name of the tournament
            course_id: ID of the course where tournament will be held
            start_date: Start date in YYYY-MM-DD format
            season_number: Season number
            week_number: Week number within the season
            event_type: Optional event type override
            overrides: Optional runtime configuration overrides
            
        Returns:
            Tournament ID
        """
        # Always use the provided event_type, default to 'standard' if not provided
        if not event_type:
            event_type = 'standard'
        config = event_type_manager.get_event_type(event_type)
        if not config:
            raise ValueError(f"Invalid event type: {event_type}")
        
        # Resolve configuration objects into actual values
        field_size = event_type_manager._generate_random_field_size(config.field_size)
        purse_base = event_type_manager._generate_random_purse(config.purse_base)
        prestige = event_type_manager._generate_random_prestige(config.prestige)
        
        config_data = {
            'event_type': event_type,
            'field_size': field_size,
            'purse_base': purse_base,
            'prestige': prestige
        }
        
        # Apply any runtime overrides
        if overrides:
            for key, value in overrides.items():
                if key in config_data:
                    config_data[key] = value
        
        # Get complete tournament configuration for new columns
        full_config = event_type_manager.get_event_type(event_type)
        
        # Extract cut line information
        # Use cut_line override if present
        if overrides and 'cut_line' in overrides:
            cut_line_type = overrides['cut_line'].get('type', 'position')
            cut_line_value = overrides['cut_line'].get('value', 65)
        else:
            cut_line_config = full_config.cut_line if hasattr(full_config, 'cut_line') else full_config.get('cut_line', {})
            cut_line_type = getattr(cut_line_config, 'type', None) or cut_line_config.get('type', 'position')
            cut_line_value = getattr(cut_line_config, 'value', None) or (cut_line_config.get('value', 65) if cut_line_type == 'position' else None)
        
        # Get points to winner
        points_structure = full_config.points_structure if hasattr(full_config, 'points_structure') else full_config.get('points_structure', {})
        points_to_winner = getattr(points_structure, 'winner', None) or points_structure.get('winner', 500)
        
        # Convert prestige to 0-1 scale if needed
        prestige_0_1 = config_data['prestige']
        if prestige_0_1 > 1.0:
            prestige_0_1 = round(prestige_0_1 / 10.0, 3)
        
        # Store event configuration as JSON for reproducibility
        event_config_json = json.dumps({
            'event_type': event_type,
            'field_size': config_data['field_size'],
            'purse_base': config_data['purse_base'],
            'prestige': prestige_0_1,
            'cut_line_type': cut_line_type,
            'cut_line_value': cut_line_value,
            'points_to_winner': points_to_winner,
            'qualification_methods': getattr(full_config, 'qualification_methods', []) or full_config.get('qualification_methods', []),
            'rounds': getattr(full_config, 'rounds', 4) or full_config.get('rounds', 4)
        })
        
        # Connect to database
        conn = sqlite3.connect(self.tournaments_db_path)
        cur = conn.cursor()
        
        try:
            # Insert tournament with new columns
            cur.execute('''
                INSERT INTO tournaments (name, tournament_type, course_id, field_size, 
                                       purse_amount, prestige, cut_line_value, cut_line_type,
                                       points_to_winner, event_config_json, season_number, week_number, status, start_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tournament_name,
                event_type,
                course_id,
                config_data['field_size'],
                config_data['purse_base'],
                prestige_0_1,
                cut_line_value,
                cut_line_type,
                points_to_winner,
                event_config_json,
                season_number,
                week_number,
                'scheduled',
                start_date
            ))
            
            tournament_id = cur.lastrowid
            
            # All tournaments now use dynamic payouts calculated after the cut
            print(f"   Dynamic payouts will be calculated after cut for {tournament_name}")
            
            # Defensive: Remove any existing schedule row for this tournament
            cur.execute('DELETE FROM tournament_schedule WHERE tournament_id = ?', (tournament_id,))

            # Insert schedule
            cur.execute('''
                INSERT INTO tournament_schedule (tournament_id, start_date, start_time,
                                               round_1_start, round_2_start, round_3_start, round_4_start)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                tournament_id,
                start_date,
                '09:00',
                '09:00',
                '12:30',
                '16:00',
                '19:30'
            ))
            
            conn.commit()
            print(f"✅ Created tournament: {tournament_name} (ID: {tournament_id})")
            print(f"   Event type: {event_type}")
            print(f"   Field size: {config_data['field_size']}")
            print(f"   Purse: ${config_data['purse_base']:,}")
            print(f"   Prestige: {prestige_0_1} (0-1 scale)")
            print(f"   Cut line: {cut_line_type} {cut_line_value if cut_line_value else ''}")
            print(f"   Points to winner: {points_to_winner}")
            
            return tournament_id
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def get_tournament_config(self, tournament_name: str) -> Dict[str, Any]:
        """Get the complete configuration for a tournament"""
        return event_type_manager.get_tournament_config(tournament_name)
    
    def generate_field_candidates(self, tournament_name: str) -> List[Dict[str, Any]]:
        """
        Generate list of players eligible for tournament field based on qualification methods
        
        Args:
            tournament_name: Name of the tournament
            
        Returns:
            List of eligible players with their qualification method
        """
        config = event_type_manager.get_tournament_config(tournament_name)
        qualification_methods = config['qualification_methods']
        
        # Connect to players database
        conn = sqlite3.connect(self.players_db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        eligible_players = []
        
        try:
            # Get all players
            cur.execute('''
                SELECT id, name, tour_card_status, exempt_thru, world_rank, 
                       recent_performance, career_wins, major_wins, country
                FROM players 
                ORDER BY world_rank ASC NULLS LAST, name ASC
            ''')
            all_players = [dict(row) for row in cur.fetchall()]
            
            # Apply qualification methods
            for method in qualification_methods:
                if method == 'tour_points_standings':
                    # For standard events, fill field based on tour points standings
                    # For now, we'll use world rank as a proxy for tour points
                    # In the future, this would query actual tour points standings
                    tour_standings_players = sorted(all_players, key=lambda p: p.get('world_rank', 999))
                    for player in tour_standings_players:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'Tour Points Standings'})
                
                elif method == 'full_status':
                    full_status_players = [p for p in all_players if p.get('tour_card_status') == 'Full']
                    for player in full_status_players:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'Full Status'})
                
                elif method == 'conditional_status':
                    conditional_players = [p for p in all_players if p.get('tour_card_status') == 'Conditional']
                    for player in conditional_players:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'Conditional Status'})
                
                elif method == 'world_rank_top_50':
                    top_50_players = [p for p in all_players if p.get('world_rank') and p.get('world_rank') <= 50]
                    for player in top_50_players:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'World Rank Top 50'})
                
                elif method == 'world_rank_top_100':
                    top_100_players = [p for p in all_players if p.get('world_rank') and p.get('world_rank') <= 100]
                    for player in top_100_players:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'World Rank Top 100'})
                
                elif method == 'past_champion':
                    # For now, simulate past champions (in real implementation, this would check tournament history)
                    past_champions = [p for p in all_players if p.get('career_wins', 0) > 0]
                    for player in past_champions:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'Past Champion'})
                
                elif method == 'sponsor_exemption':
                    # For now, add some players as sponsor exemptions (in real implementation, this would be configurable)
                    sponsor_exemptions = all_players[:5]  # First 5 players as sponsor exemptions
                    for player in sponsor_exemptions:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'Sponsor Exemption'})
                
                elif method == 'invitation_only':
                    # For invitationals, simulate invitation-based selection
                    invited_players = sorted(all_players, key=lambda p: p.get('world_rank', 999))[:90]
                    for player in invited_players:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'Invitation Only'})
                
                elif method == 'special_exemption':
                    # Special exemptions for certain players
                    special_exemptions = all_players[:3]  # First 3 players as special exemptions
                    for player in special_exemptions:
                        if not any(p['id'] == player['id'] for p in eligible_players):
                            eligible_players.append({**player, 'qualification_method': 'Special Exemption'})
            
            # Sort by world rank, then by name
            eligible_players.sort(key=lambda p: (p.get('world_rank', 999), p['name']))
            
            return eligible_players
            
        finally:
            conn.close()
    
    def finalize_tournament_field(self, tournament_id: int, player_ids: List[int]) -> bool:
        """
        Finalize the tournament field with selected players
        
        Args:
            tournament_id: ID of the tournament
            player_ids: List of player IDs to include in the field
            
        Returns:
            True if successful, False otherwise
        """
        conn = sqlite3.connect(self.tournaments_db_path)
        cur = conn.cursor()
        
        try:
            # Clear existing field
            cur.execute('DELETE FROM tournament_fields WHERE tournament_id = ?', (tournament_id,))
            
            # Insert new field
            for i, player_id in enumerate(player_ids):
                group_number = (i // 3) + 1
                group_position = (i % 3) + 1
                
                # Calculate tee time (every 3 players start 3 minutes apart)
                start_minute = (i // 3) * 3
                hour = 9 + (start_minute // 60)
                minute = start_minute % 60
                tee_time = f"{hour:02d}:{minute:02d}"
                
                cur.execute('''
                    INSERT INTO tournament_fields (tournament_id, player_id, entry_method, 
                                                 starting_position, group_number, group_position, tee_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tournament_id,
                    player_id,
                    'qualified',  # Default entry method
                    i + 1,
                    group_number,
                    group_position,
                    tee_time
                ))
            
            conn.commit()
            print(f"✅ Finalized field for tournament {tournament_id} with {len(player_ids)} players")
            return True
            
        except Exception as e:
            conn.rollback()
            print(f"❌ Error finalizing field: {e}")
            return False
        finally:
            conn.close()
    
    def get_tournament_summary(self, tournament_id: int) -> Dict[str, Any]:
        """Get a summary of tournament configuration and status"""
        conn = sqlite3.connect(self.tournaments_db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
        try:
            # Get tournament details
            cur.execute('''
                SELECT t.*, s.start_date, s.round_1_start, s.round_2_start, s.round_3_start, s.round_4_start
                FROM tournaments t
                JOIN tournament_schedule s ON t.id = s.tournament_id
                WHERE t.id = ?
            ''', (tournament_id,))
            tournament = cur.fetchone()
            
            if not tournament:
                return None
            
            tournament = dict(tournament)
            
            # Get field count
            cur.execute('SELECT COUNT(*) as field_count FROM tournament_fields WHERE tournament_id = ?', (tournament_id,))
            field_count = cur.fetchone()['field_count']
            
            # Get payout structure
            cur.execute('''
                SELECT finish_position, payout_amount, tour_points 
                FROM payout_structure 
                WHERE tournament_id = ? 
                ORDER BY finish_position
            ''', (tournament_id,))
            payout_structure = [dict(row) for row in cur.fetchall()]
            
            # Get tournament configuration
            config = event_type_manager.get_tournament_config(tournament['name'])
            
            return {
                'tournament': tournament,
                'field_count': field_count,
                'payout_structure': payout_structure,
                'config': config
            }
            
        finally:
            conn.close()

    def calculate_dynamic_payouts(self, tournament_id: int, tournament_results: List[Dict]) -> List[Dict]:
        """
        Calculate dynamic payouts for a tournament after completion
        
        Args:
            tournament_id: ID of the tournament
            tournament_results: List of player results with position, player_id, name, and made_cut status
            
        Returns:
            List of payout results with player info and amounts
        """
        # Get tournament details
        conn = sqlite3.connect(self.tournaments_db_path)
        cur = conn.cursor()
        
        try:
            cur.execute('SELECT name, purse_amount, tournament_type FROM tournaments WHERE id = ?', (tournament_id,))
            tournament = cur.fetchone()
            
            if not tournament:
                raise ValueError(f"Tournament {tournament_id} not found")
            
            tournament_name, purse_amount, tournament_type = tournament
            
            # Use the dynamic payout calculator
            calculator = PayoutCalculator(tournament_type, tournament_name)
            final_payouts = calculator.calculate_final_payouts(tournament_results, purse_amount, tournament_type, tournament_name)
            
            # Clear existing payout structure and insert new dynamic payouts
            cur.execute('DELETE FROM payout_structure WHERE tournament_id = ?', (tournament_id,))
            
            for payout in final_payouts:
                points = event_type_manager.get_points_for_position(tournament_name, payout['position'])
                cur.execute('''
                    INSERT INTO payout_structure (tournament_id, finish_position, 
                                                 payout_amount, payout_percentage, tour_points)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    tournament_id,
                    payout['position'],
                    payout['amount'],
                    payout['percentage'],
                    points
                ))
            
            conn.commit()
            print(f"✅ Calculated dynamic payouts for {tournament_name}")
            print(f"   Cut size: {len([p for p in tournament_results if p.get('made_cut', False)])}")
            print(f"   Total purse distributed: ${sum(p['amount'] for p in final_payouts):,}")
            
            return final_payouts
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

# Global instance for easy access
tournament_logic = TournamentLogic() 