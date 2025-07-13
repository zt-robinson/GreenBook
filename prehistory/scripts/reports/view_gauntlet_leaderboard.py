#!/usr/bin/env python3
"""
View Complete Gauntlet Season Leaderboard

This script displays the complete final leaderboard for the Gauntlet season,
showing all 600 players ranked by total points, and saves it to a markdown file.
"""

import sqlite3
import os
from datetime import datetime

def view_gauntlet_leaderboard():
    """Display complete Gauntlet season leaderboard and save to markdown file"""
    
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'gauntlet_leaderboard_latest.md')
    
    print("🏆 GENERATING COMPLETE GAUNTLET SEASON LEADERBOARD")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get complete leaderboard
        cursor.execute("""
            SELECT p.id, p.name, p.age, p.nationality, sps.total_season_points,
                   sps.events_played, sps.wins, sps.top_10s
            FROM players p
            JOIN season_player_stats sps ON p.id = sps.player_id
            WHERE sps.season_id = 1  -- Gauntlet season
            ORDER BY sps.total_season_points DESC
        """)
        
        results = cursor.fetchall()
        
        if not results:
            print("❌ No Gauntlet season data found!")
            return
        
        # Create markdown content
        markdown_content = []
        
        # Header
        markdown_content.append("# 🏆 Complete Gauntlet Season Leaderboard")
        markdown_content.append("")
        markdown_content.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        markdown_content.append("")
        markdown_content.append("## 📊 Season Summary")
        markdown_content.append("")
        markdown_content.append(f"- **Total Players:** {len(results)}")
        markdown_content.append(f"- **Season Winner:** {results[0][1]} ({results[0][4]} points)")
        markdown_content.append(f"- **Runner-up:** {results[1][1]} ({results[1][4]} points)")
        markdown_content.append(f"- **Third Place:** {results[2][1]} ({results[2][4]} points)")
        markdown_content.append("")
        markdown_content.append("## 🎯 Culling Information")
        markdown_content.append("")
        markdown_content.append("- **Top 100 players** will advance to regular seasons")
        markdown_content.append("- **Bottom 500 players** will be culled")
        markdown_content.append(f"- **Cutoff points:** {min([row[4] for row in results[:100]])} points")
        markdown_content.append("")
        
        # Complete leaderboard table
        markdown_content.append("## 📋 Complete Leaderboard")
        markdown_content.append("")
        markdown_content.append("| Rank | Player | Age | Nationality | Points | Events | Wins | Top 10s | Status |")
        markdown_content.append("|------|--------|-----|-------------|--------|--------|------|---------|--------|")
        
        for i, (player_id, name, age, nationality, points, events, wins, top10s) in enumerate(results, 1):
            # Determine status
            if i <= 100:
                status = "🟢 **ADVANCING**"
            else:
                status = "🔴 **CULLED**"
            
            markdown_content.append(f"| {i:3d} | {name} | {age} | {nationality} | {points:>6} | {events:>6} | {wins:>4} | {top10s:>7} | {status} |")
            
            # Add separator after rank 100
            if i == 100:
                markdown_content.append("|------|--------|-----|-------------|--------|--------|------|---------|--------|")
                markdown_content.append("| **TOP 100 - ADVANCING TO REGULAR SEASONS** | | | | | | | | |")
                markdown_content.append("|------|--------|-----|-------------|--------|--------|------|---------|--------|")
        
        # Statistics section
        markdown_content.append("")
        markdown_content.append("## 📈 Statistical Analysis")
        markdown_content.append("")
        
        # Points distribution
        points_list = [row[4] for row in results]
        max_points = max(points_list)
        min_points = min(points_list)
        avg_points = sum(points_list) / len(points_list)
        
        markdown_content.append("### Overall Statistics")
        markdown_content.append("")
        markdown_content.append(f"- **Highest points:** {max_points} ({results[0][1]})")
        markdown_content.append(f"- **Lowest points:** {min_points} ({results[-1][1]})")
        markdown_content.append(f"- **Average points:** {avg_points:.1f}")
        markdown_content.append(f"- **Points range:** {max_points - min_points}")
        markdown_content.append("")
        
        # Top 100 vs Bottom 500 analysis
        top_100_points = [row[4] for row in results[:100]]
        bottom_500_points = [row[4] for row in results[100:]]
        
        markdown_content.append("### Top 100 (Advancing)")
        markdown_content.append("")
        markdown_content.append(f"- **Average points:** {sum(top_100_points) / len(top_100_points):.1f}")
        markdown_content.append(f"- **Points range:** {max(top_100_points) - min(top_100_points)}")
        markdown_content.append(f"- **Cutoff points:** {min(top_100_points)}")
        markdown_content.append("")
        
        markdown_content.append("### Bottom 500 (Culled)")
        markdown_content.append("")
        markdown_content.append(f"- **Average points:** {sum(bottom_500_points) / len(bottom_500_points):.1f}")
        markdown_content.append(f"- **Points range:** {max(bottom_500_points) - min(bottom_500_points)}")
        markdown_content.append(f"- **Highest points:** {max(bottom_500_points)}")
        markdown_content.append("")
        
        # Culling verification
        cutoff_points = min(top_100_points)
        markdown_content.append("### Culling Verification")
        markdown_content.append("")
        markdown_content.append(f"- **Players with {cutoff_points} points or higher:** {len([p for p in points_list if p >= cutoff_points])}")
        markdown_content.append(f"- **Players with less than {cutoff_points} points:** {len([p for p in points_list if p < cutoff_points])}")
        markdown_content.append(f"- **Total players:** {len(points_list)}")
        markdown_content.append("")
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write('\n'.join(markdown_content))
        
        print(f"✅ Complete leaderboard saved to: {output_path}")
        print(f"📊 Total players: {len(results)}")
        print(f"🏆 Season winner: {results[0][1]} ({results[0][4]} points)")
        print(f"🎯 Cutoff points: {min([row[4] for row in results[:100]])}")
        
    except Exception as e:
        print(f"❌ Error generating leaderboard: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    view_gauntlet_leaderboard() 