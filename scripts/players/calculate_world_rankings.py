#!/usr/bin/env python3
"""
Calculate world rankings for all players based on their stats
"""

import sqlite3
import os
import math

def calculate_player_score(player):
    """Calculate a total score for a player based on their stats"""
    
    # Skill weights (0-100 scale, higher is better)
    skill_weights = {
        'driving_power': 0.12,      # 12% - Power off the tee
        'driving_accuracy': 0.15,   # 15% - Accuracy off the tee  
        'approach_long': 0.14,      # 14% - Long iron play
        'approach_short': 0.16,     # 16% - Short game (most important)
        'scrambling': 0.13,         # 13% - Getting up and down
        'putting': 0.15,            # 15% - Putting (most important)
        'consistency': 0.08,        # 8% - Mental game
        'composure': 0.04,          # 4% - Pressure handling
        'resilience': 0.03          # 3% - Bounce back ability
    }
    
    # Calculate weighted skill score (0-100)
    skill_score = 0
    for skill, weight in skill_weights.items():
        skill_value = player.get(skill, 50)  # Default to 50 if missing
        skill_score += skill_value * weight
    
    # Performance bonus based on career wins (0-10 points)
    career_wins = player.get('career_wins', 0)
    win_bonus = min(10, career_wins * 2)  # 2 points per win, max 10
    
    # Age factor (peak performance around 28-32)
    age = player.get('age', 30)
    if age < 25:
        age_factor = 0.95  # Young players get slight penalty
    elif age >= 25 and age <= 32:
        age_factor = 1.0   # Prime years
    elif age > 32 and age <= 40:
        age_factor = 0.98  # Slight decline
    else:
        age_factor = 0.95  # Older players get penalty
    
    # Season money bonus (0-5 points)
    season_money = player.get('season_money', 0)
    money_bonus = min(5, season_money / 1000000)  # 1 point per $1M, max 5
    
    # Calculate final score
    final_score = (skill_score + win_bonus + money_bonus) * age_factor
    
    return final_score

def update_world_rankings():
    """Update world rankings for all players"""
    
    # Database path
    db_path = os.path.join(os.path.dirname(__file__), '../../data/golf_players.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    try:
        # Get all players with their stats
        cur.execute('''
            SELECT id, name, age, country, career_wins, season_money,
                   driving_power, driving_accuracy, approach_long, approach_short,
                   scrambling, putting, consistency, composure, resilience
            FROM players 
            ORDER BY name
        ''')
        
        players = [dict(row) for row in cur.fetchall()]
        
        if not players:
            print("❌ No players found in database")
            return False
        
        print(f"📊 Calculating world rankings for {len(players)} players...")
        
        # Calculate scores for all players
        player_scores = []
        for player in players:
            score = calculate_player_score(player)
            player_scores.append({
                'id': player['id'],
                'name': player['name'],
                'score': score,
                'country': player['country']
            })
        
        # Sort by score (highest first) and assign rankings
        player_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Update database with new rankings
        for rank, player in enumerate(player_scores, 1):
            cur.execute('''
                UPDATE players 
                SET world_ranking = ? 
                WHERE id = ?
            ''', (rank, player['id']))
        
        conn.commit()
        
        # Display top 20 players
        print("\n🏆 Top 20 World Rankings:")
        print("-" * 80)
        print(f"{'Rank':<4} {'Name':<25} {'Score':<8} {'Country':<15}")
        print("-" * 80)
        
        for rank, player in enumerate(player_scores[:20], 1):
            print(f"{rank:<4} {player['name']:<25} {player['score']:<8.1f} {player['country']:<15}")
        
        # Show some statistics
        scores = [p['score'] for p in player_scores]
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)
        max_score = max(scores)
        
        print(f"\n📈 Statistics:")
        print(f"   Average Score: {avg_score:.1f}")
        print(f"   Highest Score: {max_score:.1f}")
        print(f"   Lowest Score: {min_score:.1f}")
        print(f"   Score Range: {max_score - min_score:.1f}")
        
        print(f"\n✅ World rankings updated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating world rankings: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    update_world_rankings() 