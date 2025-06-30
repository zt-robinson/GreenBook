#!/usr/bin/env python3
"""
Dynamic Payout Calculator for Golf Tournaments

This module handles payout distribution for tournaments with cuts, ensuring:
1. All players who make the cut receive some payout
2. Anchor positions have predefined percentages
3. Remaining percentage is distributed among non-anchor positions
4. Tied players receive the same payout (averaged from their positions)
"""

from typing import Dict, List, Tuple, Optional
import math

class PayoutCalculator:
    """Handles dynamic payout calculation for tournaments with cuts"""
    
    # Major-specific winner percentages
    MAJOR_WINNER_PERCENTAGES = {
        'The Sovereign Tournament': 20.0,
        'Royal Open Championship': 20.0,
        'American Open Championship': 18.0,
        'AGA Championship': 18.0
    }
    
    # Standard anchor positions and their payout percentages
    # These are the key positions that have fixed percentages
    ANCHOR_POSITIONS = {
        'major': {
            1: 18.0,    # Winner (will be overridden for specific majors)
            2: 10.8,    # Runner-up
            3: 6.8,     # Third place
            5: 4.0,     # Fifth place
            10: 2.7,    # Tenth place
            15: 1.7,    # Fifteenth place
            20: 0.7,    # Twentieth place
            25: 0.2     # Twenty-fifth place
        },
        'standard': {
            1: 18.0,    # Winner
            2: 10.9,    # Runner-up
            3: 6.9,     # Third place
            5: 4.1,     # Fifth place
            10: 2.725,  # Tenth place
            15: 1.825,  # Fifteenth place
            20: 1.325,  # Twentieth place
            25: 0.885   # Twenty-fifth place
        },
        'invitational': {
            1: 20.0,    # Winner
            2: 10.8,    # Runner-up
            3: 6.8,     # Third place
            5: 3.963,   # Fifth place
            10: 2.359,  # Tenth place
            15: 1.3,    # Fifteenth place
            20: 0.4,    # Twentieth place
            25: 0.18    # Twenty-fifth place
        }
    }
    
    def __init__(self, event_type: str = 'standard', tournament_name: str = None):
        """Initialize calculator with event type and optional tournament name"""
        self.event_type = event_type
        self.tournament_name = tournament_name
        self.anchor_positions = self.ANCHOR_POSITIONS.get(event_type, self.ANCHOR_POSITIONS['standard']).copy()
        
        # Override winner percentage for specific majors
        if tournament_name and tournament_name in self.MAJOR_WINNER_PERCENTAGES:
            self.anchor_positions[1] = self.MAJOR_WINNER_PERCENTAGES[tournament_name]
    
    def calculate_major_payout_structure(self, cut_size: int, purse: int) -> Dict[int, float]:
        """
        Calculate payout percentages for majors using the new structure:
        - Top 10: 50% of purse
        - Top 25: 70% of purse  
        - Remaining: 30% of purse
        
        Args:
            cut_size: Number of players who made the cut
            purse: Total tournament purse in dollars
            
        Returns:
            Dictionary mapping position (1-based) to payout percentage
        """
        if cut_size <= 0:
            return {}
        
        payout_percentages = {}
        
        # Get winner percentage for this specific major
        winner_percentage = self.anchor_positions[1]
        
        # Step 1: Set winner percentage
        payout_percentages[1] = winner_percentage
        
        # Step 2: Distribute remaining 50% - winner_percentage among positions 2-10
        remaining_top_10 = 50.0 - winner_percentage
        positions_2_10 = list(range(2, 11))
        
        # Use declining scale for positions 2-10
        # Calculate weights that sum to 1.0
        weights_2_10 = [0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.06, 0.03, 0.01]
        
        for i, position in enumerate(positions_2_10):
            if position <= cut_size:
                percentage = remaining_top_10 * weights_2_10[i]
                payout_percentages[position] = round(percentage, 4)
        
        # Step 3: Distribute next 20% (70% - 50%) among positions 11-25
        remaining_11_25 = 20.0  # 70% - 50%
        positions_11_25 = list(range(11, 26))
        
        # Use declining scale for positions 11-25
        for i, position in enumerate(positions_11_25):
            if position <= cut_size:
                # Calculate weight based on position (higher positions get more)
                weight = (26 - position) / sum(range(1, 16))  # 15 positions, declining weight
                percentage = remaining_11_25 * weight
                payout_percentages[position] = round(percentage, 4)
        
        # Step 4: Distribute remaining 30% among positions beyond 25
        remaining_percentage = 30.0  # 100% - 70%
        positions_beyond_25 = list(range(26, cut_size + 1))
        
        if positions_beyond_25:
            # Use declining scale for remaining positions
            for i, position in enumerate(positions_beyond_25):
                # Calculate weight based on position (higher positions get more)
                weight = (cut_size + 1 - position) / sum(range(1, len(positions_beyond_25) + 1))
                percentage = remaining_percentage * weight
                
                # Ensure minimum payout (at least 0.01% of purse)
                percentage = max(percentage, 0.01)
                payout_percentages[position] = round(percentage, 4)
        
        # Step 5: Normalize to ensure total equals 100%
        total_percentage = sum(payout_percentages.values())
        if abs(total_percentage - 100.0) > 0.01:
            # Adjust all percentages proportionally
            adjustment_factor = 100.0 / total_percentage
            for position in payout_percentages:
                payout_percentages[position] = round(
                    payout_percentages[position] * adjustment_factor, 4
                )
        
        return payout_percentages
    
    def calculate_standard_payout_structure(self, cut_size: int, purse: int) -> Dict[int, float]:
        """
        Calculate payout percentages for standard events using the new structure:
        - Top 15: 70% of purse
        - Top 25: 85% of purse
        - Remaining: 15% of purse
        Args:
            cut_size: Number of players who made the cut
            purse: Total tournament purse in dollars
        Returns:
            Dictionary mapping position (1-based) to payout percentage
        """
        if cut_size <= 0:
            return {}
        payout_percentages = {}
        # Step 1: Set anchor percentages for top 10
        anchor_top_10 = [18.0, 10.9, 6.9, 4.9, 4.1, 3.625, 3.375, 3.125, 2.925, 2.725]
        for i, pct in enumerate(anchor_top_10):
            pos = i + 1
            if pos <= cut_size:
                payout_percentages[pos] = round(pct, 4)
        anchor_used = sum(payout_percentages.values())
        # Step 2: Calculate remaining for top 15
        top_15_target = 70.0
        anchor_top_10_used = sum(anchor_top_10[:min(10, cut_size)])
        remaining_top_15 = top_15_target - anchor_top_10_used
        positions_11_15 = [p for p in range(11, 16) if p <= cut_size]
        if positions_11_15:
            # Distribute remaining_top_15 using a declining scale
            n = len(positions_11_15)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_11_15):
                pct = remaining_top_15 * (weights[i] / total_weight)
                payout_percentages[pos] = round(pct, 4)
        # Step 3: Calculate remaining for top 25
        top_25_target = 85.0
        anchor_top_15_used = sum(payout_percentages.get(p, 0) for p in range(1, 16))
        remaining_top_25 = top_25_target - anchor_top_15_used
        positions_16_25 = [p for p in range(16, 26) if p <= cut_size]
        if positions_16_25:
            n = len(positions_16_25)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_16_25):
                pct = remaining_top_25 * (weights[i] / total_weight)
                payout_percentages[pos] = round(pct, 4)
        # Step 4: Distribute remaining 15% among positions beyond 25
        remaining_percentage = 100.0 - sum(payout_percentages.values())
        positions_beyond_25 = [p for p in range(26, cut_size + 1)]
        if positions_beyond_25:
            n = len(positions_beyond_25)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_beyond_25):
                pct = remaining_percentage * (weights[i] / total_weight)
                pct = max(pct, 0.01)
                payout_percentages[pos] = round(pct, 4)
        # Step 5: Normalize to ensure total equals 100%
        total_percentage = sum(payout_percentages.values())
        if abs(total_percentage - 100.0) > 0.01:
            adjustment_factor = 100.0 / total_percentage
            for position in payout_percentages:
                payout_percentages[position] = round(payout_percentages[position] * adjustment_factor, 4)
        return payout_percentages
    
    def calculate_royal_open_payout_structure(self, cut_size: int, purse: int) -> Dict[int, float]:
        """
        Calculate payout percentages for the Royal Open Championship:
        - Top 10: custom anchors
        - Top 15: 70% of purse
        - Top 25: 80% of purse
        - Remaining: 20% of purse
        """
        if cut_size <= 0:
            return {}
        payout_percentages = {}
        # Step 1: Set anchor percentages for top 10
        anchor_top_10 = [20.0, 10.8, 6.787, 4.758, 3.963, 3.514, 3.168, 2.837, 2.568, 2.359]
        for i, pct in enumerate(anchor_top_10):
            pos = i + 1
            if pos <= cut_size:
                payout_percentages[pos] = round(pct, 4)
        anchor_used = sum(payout_percentages.values())
        # Step 2: Calculate remaining for top 15
        top_15_target = 70.0
        anchor_top_10_used = sum(anchor_top_10[:min(10, cut_size)])
        remaining_top_15 = top_15_target - anchor_top_10_used
        positions_11_15 = [p for p in range(11, 16) if p <= cut_size]
        if positions_11_15:
            n = len(positions_11_15)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_11_15):
                pct = remaining_top_15 * (weights[i] / total_weight)
                payout_percentages[pos] = round(pct, 4)
        # Step 3: Calculate remaining for top 25
        top_25_target = 80.0
        anchor_top_15_used = sum(payout_percentages.get(p, 0) for p in range(1, 16))
        remaining_top_25 = top_25_target - anchor_top_15_used
        positions_16_25 = [p for p in range(16, 26) if p <= cut_size]
        if positions_16_25:
            n = len(positions_16_25)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_16_25):
                pct = remaining_top_25 * (weights[i] / total_weight)
                payout_percentages[pos] = round(pct, 4)
        # Step 4: Distribute remaining 20% among positions beyond 25
        remaining_percentage = 100.0 - sum(payout_percentages.values())
        positions_beyond_25 = [p for p in range(26, cut_size + 1)]
        if positions_beyond_25:
            n = len(positions_beyond_25)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_beyond_25):
                pct = remaining_percentage * (weights[i] / total_weight)
                pct = max(pct, 0.01)
                payout_percentages[pos] = round(pct, 4)
        # Step 5: Normalize to ensure total equals 100%
        total_percentage = sum(payout_percentages.values())
        if abs(total_percentage - 100.0) > 0.01:
            adjustment_factor = 100.0 / total_percentage
            for position in payout_percentages:
                payout_percentages[position] = round(payout_percentages[position] * adjustment_factor, 4)
        return payout_percentages
    
    def calculate_american_open_payout_structure(self, cut_size: int, purse: int) -> Dict[int, float]:
        """
        Calculate payout percentages for the American Open Championship:
        - Top 10: custom anchors
        - Top 15: 70% of purse
        - Top 25: 80% of purse
        - Remaining: 20% of purse
        """
        if cut_size <= 0:
            return {}
        payout_percentages = {}
        # Step 1: Set anchor percentages for top 10
        anchor_top_10 = [18.0, 10.8, 6.8, 4.8, 4.0, 3.599, 3.37, 3.149, 2.938, 2.736]
        for i, pct in enumerate(anchor_top_10):
            pos = i + 1
            if pos <= cut_size:
                payout_percentages[pos] = round(pct, 4)
        anchor_used = sum(payout_percentages.values())
        # Step 2: Calculate remaining for top 15
        top_15_target = 70.0
        anchor_top_10_used = sum(anchor_top_10[:min(10, cut_size)])
        remaining_top_15 = top_15_target - anchor_top_10_used
        positions_11_15 = [p for p in range(11, 16) if p <= cut_size]
        if positions_11_15:
            n = len(positions_11_15)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_11_15):
                pct = remaining_top_15 * (weights[i] / total_weight)
                payout_percentages[pos] = round(pct, 4)
        # Step 3: Calculate remaining for top 25
        top_25_target = 80.0
        anchor_top_15_used = sum(payout_percentages.get(p, 0) for p in range(1, 16))
        remaining_top_25 = top_25_target - anchor_top_15_used
        positions_16_25 = [p for p in range(16, 26) if p <= cut_size]
        if positions_16_25:
            n = len(positions_16_25)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_16_25):
                pct = remaining_top_25 * (weights[i] / total_weight)
                payout_percentages[pos] = round(pct, 4)
        # Step 4: Distribute remaining 20% among positions beyond 25
        remaining_percentage = 100.0 - sum(payout_percentages.values())
        positions_beyond_25 = [p for p in range(26, cut_size + 1)]
        if positions_beyond_25:
            n = len(positions_beyond_25)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_beyond_25):
                pct = remaining_percentage * (weights[i] / total_weight)
                pct = max(pct, 0.01)
                payout_percentages[pos] = round(pct, 4)
        # Step 5: Normalize to ensure total equals 100%
        total_percentage = sum(payout_percentages.values())
        if abs(total_percentage - 100.0) > 0.01:
            adjustment_factor = 100.0 / total_percentage
            for position in payout_percentages:
                payout_percentages[position] = round(payout_percentages[position] * adjustment_factor, 4)
        return payout_percentages
    
    def calculate_aga_championship_payout_structure(self, cut_size: int, purse: int) -> Dict[int, float]:
        """
        Calculate payout percentages for the AGA Championship:
        - Top 10: custom anchors
        - Top 15: 60% of purse
        - Top 25: 75% of purse
        - Remaining: 25% of purse
        """
        if cut_size <= 0:
            return {}
        payout_percentages = {}
        # Step 1: Set anchor percentages for top 10
        anchor_top_10 = [18.235, 10.347, 6.635, 5.153, 4.147, 3.594, 3.088, 2.603, 2.282, 2.062]
        for i, pct in enumerate(anchor_top_10):
            pos = i + 1
            if pos <= cut_size:
                payout_percentages[pos] = round(pct, 4)
        anchor_used = sum(payout_percentages.values())
        # Step 2: Calculate remaining for top 15
        top_15_target = 60.0
        anchor_top_10_used = sum(anchor_top_10[:min(10, cut_size)])
        remaining_top_15 = top_15_target - anchor_top_10_used
        positions_11_15 = [p for p in range(11, 16) if p <= cut_size]
        if positions_11_15:
            n = len(positions_11_15)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_11_15):
                pct = remaining_top_15 * (weights[i] / total_weight)
                payout_percentages[pos] = round(pct, 4)
        # Step 3: Calculate remaining for top 25
        top_25_target = 75.0
        anchor_top_15_used = sum(payout_percentages.get(p, 0) for p in range(1, 16))
        remaining_top_25 = top_25_target - anchor_top_15_used
        positions_16_25 = [p for p in range(16, 26) if p <= cut_size]
        if positions_16_25:
            n = len(positions_16_25)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_16_25):
                pct = remaining_top_25 * (weights[i] / total_weight)
                payout_percentages[pos] = round(pct, 4)
        # Step 4: Distribute remaining 25% among positions beyond 25
        remaining_percentage = 100.0 - sum(payout_percentages.values())
        positions_beyond_25 = [p for p in range(26, cut_size + 1)]
        if positions_beyond_25:
            n = len(positions_beyond_25)
            weights = [n - i for i in range(n)]
            total_weight = sum(weights)
            for i, pos in enumerate(positions_beyond_25):
                pct = remaining_percentage * (weights[i] / total_weight)
                pct = max(pct, 0.01)
                payout_percentages[pos] = round(pct, 4)
        # Step 5: Normalize to ensure total equals 100%
        total_percentage = sum(payout_percentages.values())
        if abs(total_percentage - 100.0) > 0.01:
            adjustment_factor = 100.0 / total_percentage
            for position in payout_percentages:
                payout_percentages[position] = round(payout_percentages[position] * adjustment_factor, 4)
        return payout_percentages
    
    def calculate_payout_structure(self, cut_size: int, purse: int) -> Dict[int, float]:
        """
        Calculate payout percentages for all positions after cut
        
        Args:
            cut_size: Number of players who made the cut
            purse: Total tournament purse in dollars
            
        Returns:
            Dictionary mapping position (1-based) to payout percentage
        """
        if cut_size <= 0:
            return {}
        
        # AGA Championship custom logic
        if self.tournament_name == 'AGA Championship':
            return self.calculate_aga_championship_payout_structure(cut_size, purse)
        
        # American Open custom logic
        if self.tournament_name == 'American Open Championship':
            return self.calculate_american_open_payout_structure(cut_size, purse)
        
        # Royal Open custom logic
        if self.tournament_name == 'Royal Open Championship':
            return self.calculate_royal_open_payout_structure(cut_size, purse)
        
        # The Continental Championship uses standard event payout logic
        if self.tournament_name == 'The Continental Championship':
            return self.calculate_standard_payout_structure(cut_size, purse)
        
        # Use major-specific calculation for majors with tournament names
        if self.event_type == 'major' and self.tournament_name:
            return self.calculate_major_payout_structure(cut_size, purse)
        
        # Use new standard event logic
        if self.event_type == 'standard':
            return self.calculate_standard_payout_structure(cut_size, purse)
        
        # Use original calculation for other event types
        payout_percentages = {}
        
        # Step 1: Assign anchor position percentages
        anchor_percentage_used = 0.0
        for position, percentage in self.anchor_positions.items():
            if position <= cut_size:
                payout_percentages[position] = percentage
                anchor_percentage_used += percentage
        
        # Step 2: Calculate remaining percentage to distribute
        remaining_percentage = 100.0 - anchor_percentage_used
        
        # Step 3: Distribute remaining percentage among non-anchor positions
        non_anchor_positions = []
        for pos in range(1, cut_size + 1):
            if pos not in self.anchor_positions:
                non_anchor_positions.append(pos)
        
        if non_anchor_positions:
            # Use a declining scale for non-anchor positions
            # Start with a reasonable percentage and decline gradually
            base_percentage = remaining_percentage / len(non_anchor_positions)
            
            # Apply a slight decline factor to make it more realistic
            decline_factor = 0.98  # Each position gets 98% of the previous
            
            for i, position in enumerate(non_anchor_positions):
                if i == 0:
                    # First non-anchor position gets a bit more
                    percentage = base_percentage * 1.2
                else:
                    # Subsequent positions decline
                    percentage = base_percentage * (decline_factor ** i)
                
                # Ensure minimum payout (at least 0.01% of purse)
                percentage = max(percentage, 0.01)
                payout_percentages[position] = round(percentage, 4)
        
        # Step 4: Normalize to ensure total equals 100%
        total_percentage = sum(payout_percentages.values())
        if total_percentage != 100.0:
            # Adjust all percentages proportionally
            adjustment_factor = 100.0 / total_percentage
            for position in payout_percentages:
                payout_percentages[position] = round(
                    payout_percentages[position] * adjustment_factor, 4
                )
        
        return payout_percentages
    
    def handle_ties(self, final_leaderboard: List[Dict], payout_percentages: Dict[int, float]) -> Dict[int, Dict]:
        """
        Handle ties in the final leaderboard and adjust payouts accordingly
        
        Args:
            final_leaderboard: List of player results with 'position' and 'player_id'
            payout_percentages: Pre-calculated payout percentages by position
            
        Returns:
            Dictionary mapping player_id to payout info
        """
        player_payouts = {}
        
        # Group players by their final position
        position_groups = {}
        for player in final_leaderboard:
            position = player['position']
            if position not in position_groups:
                position_groups[position] = []
            position_groups[position].append(player)
        
        # Calculate payouts for each position group
        for position, players in position_groups.items():
            if position not in payout_percentages:
                # Position beyond what we calculated (shouldn't happen)
                continue
            
            # Get the total percentage for this position
            total_percentage = payout_percentages[position]
            
            # If there are ties, average the percentage among tied players
            if len(players) > 1:
                # Calculate the average percentage for all tied positions
                tied_positions = list(range(position, position + len(players)))
                total_tied_percentage = sum(
                    payout_percentages.get(pos, 0) for pos in tied_positions
                )
                average_percentage = total_tied_percentage / len(players)
                
                # Assign the average percentage to each tied player
                for player in players:
                    player_payouts[player['player_id']] = {
                        'position': position,
                        'percentage': round(average_percentage, 4),
                        'tied': True,
                        'tied_count': len(players)
                    }
            else:
                # No ties, use the original percentage
                player_payouts[players[0]['player_id']] = {
                    'position': position,
                    'percentage': payout_percentages[position],
                    'tied': False,
                    'tied_count': 1
                }
        
        return player_payouts
    
    def calculate_final_payouts(self, tournament_results: List[Dict], purse: int, event_type: str = 'standard', tournament_name: str = None) -> List[Dict]:
        """
        Calculate final payouts for a completed tournament
        
        Args:
            tournament_results: List of player results with position and player info
            purse: Total tournament purse
            event_type: Type of tournament (major, standard, invitational)
            tournament_name: Name of the tournament (for major-specific calculations)
            
        Returns:
            List of payout results with player info and amounts
        """
        # Filter to only players who made the cut
        cut_players = [p for p in tournament_results if p.get('made_cut', False)]
        cut_size = len(cut_players)
        
        if cut_size == 0:
            return []
        
        # Initialize calculator with event type and tournament name
        self.__init__(event_type, tournament_name)
        
        # Calculate base payout structure
        payout_percentages = self.calculate_payout_structure(cut_size, purse)
        
        # Handle ties and get final player payouts
        player_payouts = self.handle_ties(cut_players, payout_percentages)
        
        # Calculate actual dollar amounts
        final_payouts = []
        total_paid = 0
        
        for player in cut_players:
            player_id = player['player_id']
            if player_id in player_payouts:
                payout_info = player_payouts[player_id]
                payout_amount = int(purse * (payout_info['percentage'] / 100))
                
                final_payouts.append({
                    'player_id': player_id,
                    'player_name': player.get('name', 'Unknown'),
                    'position': payout_info['position'],
                    'percentage': payout_info['percentage'],
                    'amount': payout_amount,
                    'tied': payout_info['tied'],
                    'tied_count': payout_info['tied_count']
                })
                total_paid += payout_amount
        
        # Ensure the total purse is distributed exactly
        if total_paid != purse and final_payouts:
            # Find the player with the highest position number (should get the adjustment)
            highest_position_player = max(final_payouts, key=lambda x: x['position'])
            
            # Adjust the highest position player's payout to account for rounding differences
            adjustment = purse - total_paid
            highest_position_player['amount'] += adjustment
            print(f"   Adjusted position {highest_position_player['position']} payout by ${adjustment:,} to ensure exact purse distribution")
            
            # Verify the adjustment doesn't violate payout order
            if len(final_payouts) > 1:
                # Check if the adjusted player now gets more than the player above them
                adjusted_position = highest_position_player['position']
                players_above = [p for p in final_payouts if p['position'] < adjusted_position]
                
                if players_above:
                    player_above = max(players_above, key=lambda x: x['position'])
                    if highest_position_player['amount'] > player_above['amount']:
                        print(f"   ⚠️ Warning: Position {adjusted_position} (${highest_position_player['amount']:,}) now gets more than position {player_above['position']} (${player_above['amount']:,})")
                        print(f"   This is acceptable as it's a small rounding adjustment")
        
        return sorted(final_payouts, key=lambda x: x['position'])
    
    def get_anchor_positions(self) -> Dict[int, float]:
        """Get the anchor positions and percentages for the current event type"""
        return self.anchor_positions.copy()
    
    def validate_payout_structure(self, payout_percentages: Dict[int, float]) -> Tuple[bool, str]:
        """
        Validate that payout percentages are reasonable
        
        Args:
            payout_percentages: Dictionary of position -> percentage
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not payout_percentages:
            return False, "No payout percentages provided"
        
        total_percentage = sum(payout_percentages.values())
        
        # Check if total is close to 100%
        if abs(total_percentage - 100.0) > 0.01:
            return False, f"Total percentage is {total_percentage:.2f}%, should be 100%"
        
        # Check for negative percentages
        for position, percentage in payout_percentages.items():
            if percentage < 0:
                return False, f"Negative percentage {percentage} for position {position}"
        
        # Check that winner gets the most
        winner_percentage = payout_percentages.get(1, 0)
        for position, percentage in payout_percentages.items():
            if position != 1 and percentage > winner_percentage:
                return False, f"Position {position} has higher percentage than winner"
        
        return True, "Payout structure is valid" 