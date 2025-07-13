#!/usr/bin/env python3
"""
Gauntlet Culling Script for GreenBook Prehistory

This script culls the bottom 500 players from the Gauntlet season,
permanently deleting them from the database. It also generates a markdown report.
"""

import sqlite3
import os
from datetime import datetime

def generate_post_culling_report(advancing_players):
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'post_culling_leaderboard_gauntlet.md')
    print(f"\n📊 Generating post-culling leaderboard report (Gauntlet)...")
    markdown_content = []
    markdown_content.append("# 🏆 Post-Culling Leaderboard (Gauntlet)")
    markdown_content.append("")
    markdown_content.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    markdown_content.append("")
    markdown_content.append("## 📊 Culling Summary")
    markdown_content.append("")
    markdown_content.append("- **Original players:** 600")
    markdown_content.append("- **Players culled:** 500 (permanently deleted)")
    markdown_content.append("- **Players remaining:** 100")
    markdown_content.append("- **Next step:** Add 50 new players for Season 1")
    markdown_content.append("")
    markdown_content.append("## 📋 Advancing Players (Top 100)")
    markdown_content.append("")
    markdown_content.append("| Rank | Player | Age | Nationality | Points |")
    markdown_content.append("|------|--------|-----|-------------|--------|")
    for i, (player_id, name, age, nationality, points) in enumerate(advancing_players, 1):
        markdown_content.append(f"| {i:3d} | {name} | {age} | {nationality} | {points:>6} |")
    with open(output_path, 'w') as f:
        f.write('\n'.join(markdown_content))
    print(f"✅ Post-culling report saved to: {output_path}")
    print(f"📊 Players remaining: {len(advancing_players)}")
    print(f"🏆 Top player: {advancing_players[0][1]} ({advancing_players[0][4]} points)")
    print(f"📉 Cutoff: {advancing_players[-1][1]} ({advancing_players[-1][4]} points)")

def cull_players_gauntlet():
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
    print("🗑️  GAUNTLET PLAYER CULLING PROCESS")
    print("=" * 60)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM players")
        total_players = cursor.fetchone()[0]
        print(f"📊 Current player count: {total_players}")
        cursor.execute("""
            SELECT p.id, p.name, p.age, p.nationality, sps.total_season_points
            FROM players p
            JOIN season_player_stats sps ON p.id = sps.player_id
            WHERE sps.season_id = 1
            ORDER BY sps.total_season_points DESC
            LIMIT 100
        """)
        advancing_players = cursor.fetchall()
        print(f"🏆 Top 100 players advancing to regular seasons:")
        for i, (player_id, name, age, nationality, points) in enumerate(advancing_players, 1):
            print(f"{i:2d}. {name:<20} ({age}) {nationality:<15} {points:>6} pts")
        cursor.execute("""
            SELECT p.id
            FROM players p
            JOIN season_player_stats sps ON p.id = sps.player_id
            WHERE sps.season_id = 1
            ORDER BY sps.total_season_points ASC
            LIMIT 500
        """)
        culled_player_ids = [row[0] for row in cursor.fetchall()]
        print(f"\n⚠️  About to permanently delete {len(culled_player_ids)} players")
        placeholders = ','.join(['?' for _ in culled_player_ids])
        cursor.execute(f"DELETE FROM players WHERE id IN ({placeholders})", culled_player_ids)
        cursor.execute(f"DELETE FROM tournament_results WHERE player_id IN ({placeholders})", culled_player_ids)
        cursor.execute(f"DELETE FROM season_player_stats WHERE player_id IN ({placeholders})", culled_player_ids)
        cursor.execute(f"DELETE FROM season_event_results WHERE player_id IN ({placeholders})", culled_player_ids)
        conn.commit()
        cursor.execute("SELECT COUNT(*) FROM players")
        new_total = cursor.fetchone()[0]
        print(f"\n✅ Player culling complete!")
        print(f"   Players culled: {len(culled_player_ids)}")
        print(f"   Players remaining: {new_total}")
        generate_post_culling_report(advancing_players)
        return True
    except Exception as e:
        print(f"❌ Error during player culling: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = cull_players_gauntlet()
    if success:
        print("\n🎉 Gauntlet player culling process complete!")
        print("Next step: Add 50 new players for Season 1")
    else:
        print("\n❌ Gauntlet player culling failed!") 