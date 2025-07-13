#!/usr/bin/env python3
"""
Regular Season Culling Script for GreenBook Prehistory

This script culls relegated players after a regular season by marking them as inactive (not deleting).
It also generates a markdown report.
"""

import sqlite3
import os
from datetime import datetime

def generate_post_culling_report(advancing_players, relegated_players, season_num):
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', f'post_culling_leaderboard_regular_season_{season_num}.md')
    print(f"\n📊 Generating post-culling leaderboard report (Regular Season {season_num})...")
    markdown_content = []
    markdown_content.append(f"# 🏆 Post-Culling Leaderboard (Regular Season {season_num})")
    markdown_content.append("")
    markdown_content.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    markdown_content.append("")
    markdown_content.append("## 📊 Culling Summary")
    markdown_content.append("")
    markdown_content.append(f"- **Players relegated:** {len(relegated_players)} (marked as inactive)")
    markdown_content.append(f"- **Players remaining:** {len(advancing_players)}")
    markdown_content.append("")
    
    if advancing_players:
        markdown_content.append("## 📋 Advancing Players")
        markdown_content.append("")
        markdown_content.append("| Rank | Player | Age | Nationality | Points |")
        markdown_content.append("|------|--------|-----|-------------|--------|")
        for i, (player_id, name, age, nationality, points) in enumerate(advancing_players, 1):
            markdown_content.append(f"| {i:3d} | {name} | {age} | {nationality} | {points:>6} |")
        markdown_content.append("")
    else:
        markdown_content.append("## ⚠️  No Advancing Players")
        markdown_content.append("")
        markdown_content.append("All players were relegated.")
        markdown_content.append("")
    
    if relegated_players:
        markdown_content.append("## 📋 Relegated Players")
        markdown_content.append("")
        markdown_content.append("| Rank | Player | Age | Nationality | Points |")
        markdown_content.append("|------|--------|-----|-------------|--------|")
        for i, (player_id, name, age, nationality, points) in enumerate(relegated_players, 1):
            markdown_content.append(f"| {i:3d} | {name} | {age} | {nationality} | {points:>6} |")
    else:
        markdown_content.append("## ⚠️  No Relegated Players")
        markdown_content.append("")
        markdown_content.append("No players were relegated.")
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(markdown_content))
    print(f"✅ Post-culling report saved to: {output_path}")
    
    if advancing_players:
        print(f"📊 Players remaining: {len(advancing_players)}")
        print(f"🏆 Top player: {advancing_players[0][1]} ({advancing_players[0][4]} points)")
        print(f"📉 Last advancing: {advancing_players[-1][1]} ({advancing_players[-1][4]} points)")
    else:
        print(f"📊 Players remaining: 0")
        print("⚠️  All players were relegated!")

def cull_players_regular_season(season_num=1, num_to_relegate=50):
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
    print(f"🗑️  REGULAR SEASON {season_num} PLAYER CULLING PROCESS")
    print("=" * 60)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM players WHERE current_status = 'active'")
        total_players = cursor.fetchone()[0]
        print(f"📊 Current active player count: {total_players}")
        
        # Get all players with their season stats, ordered by points
        cursor.execute(f"""
            SELECT p.id, p.name, p.age, p.nationality, sps.total_season_points
            FROM players p
            JOIN season_player_stats sps ON p.id = sps.player_id
            WHERE sps.season_id = ? AND p.current_status = 'active'
            ORDER BY sps.total_season_points DESC
        """, (season_num,))
        all_players = cursor.fetchall()
        
        if len(all_players) == 0:
            print("❌ No players found with season stats!")
            return False
        
        if len(all_players) <= num_to_relegate:
            print(f"⚠️  Warning: Only {len(all_players)} players found, but {num_to_relegate} requested to relegate")
            print("   This would relegate ALL players, which is not allowed.")
            print("   Please reduce the number of players to relegate.")
            return False
        
        # Split into advancing and relegated players
        advancing_players = all_players[:-num_to_relegate]  # Top players
        relegated_players = all_players[-num_to_relegate:]  # Bottom players
        
        relegated_player_ids = [row[0] for row in relegated_players]
        print(f"\n⚠️  About to mark {len(relegated_player_ids)} players as inactive")
        print(f"   Bottom player: {relegated_players[-1][1]} ({relegated_players[-1][4]} points)")
        print(f"   Top relegated: {relegated_players[0][1]} ({relegated_players[0][4]} points)")
        print(f"   Players advancing: {len(advancing_players)}")
        print(f"   DEBUG: Total players with stats: {len(all_players)}")
        print(f"   DEBUG: Advancing players count: {len(advancing_players)}")
        print(f"   DEBUG: Relegated players count: {len(relegated_players)}")
        
        # Mark relegated players as inactive (preserve all historical data)
        placeholders = ','.join(['?' for _ in relegated_player_ids])
        cursor.execute(f"UPDATE players SET current_status = 'inactive' WHERE id IN ({placeholders})", relegated_player_ids)
        
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM players WHERE current_status = 'active'")
        new_total = cursor.fetchone()[0]
        print(f"\n✅ Player culling complete!")
        print(f"   Players relegated: {len(relegated_player_ids)}")
        print(f"   Players remaining: {new_total}")
        print(f"   Historical data preserved for relegated players")
        generate_post_culling_report(advancing_players, relegated_players, season_num)
        return True
    except Exception as e:
        print(f"❌ Error during player culling: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cull relegated players after a regular season.")
    parser.add_argument('--season', type=int, default=1, help='Season number (default: 1)')
    parser.add_argument('--relegate', type=int, default=50, help='Number of players to relegate (default: 50)')
    args = parser.parse_args()
    success = cull_players_regular_season(season_num=args.season, num_to_relegate=args.relegate)
    if success:
        print(f"\n🎉 Regular season {args.season} player culling process complete!")
        print("Next step: Add new players for next season")
    else:
        print(f"\n❌ Regular season {args.season} player culling failed!") 