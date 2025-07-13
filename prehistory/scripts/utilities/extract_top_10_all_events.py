#!/usr/bin/env python3
"""
Extract Top 10 Players from All Season 1 Events

This script goes through all 35 event leaderboards and extracts the top 10 players for each event.
"""

import os
import re
from pathlib import Path

def extract_top_10_from_event(event_file):
    """Extract top 10 players from a single event leaderboard"""
    top_10 = []
    
    try:
        with open(event_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the table section
        lines = content.split('\n')
        in_table = False
        
        for line in lines:
            if '| Rank | Player | Nationality | Performance | Points |' in line:
                in_table = True
                continue
            elif in_table and line.strip() == '':
                break
            elif in_table and line.startswith('|'):
                # Parse table row
                parts = [part.strip() for part in line.split('|')[1:-1]]  # Remove empty first/last parts
                if len(parts) >= 4 and parts[0].isdigit():
                    rank = int(parts[0])
                    if rank <= 10:  # Only top 10
                        name = parts[1]
                        nationality = parts[2]
                        performance = float(parts[3])
                        points = int(parts[4])
                        
                        top_10.append({
                            'rank': rank,
                            'name': name,
                            'nationality': nationality,
                            'performance': performance,
                            'points': points
                        })
                    else:
                        break  # Stop after top 10
        
        return top_10
        
    except Exception as e:
        print(f"❌ Error reading {event_file}: {e}")
        return []

def extract_all_top_10():
    """Extract top 10 from all 35 Season 1 events"""
    reports_dir = Path("reports")
    
    print("🏆 EXTRACTING TOP 10 FROM ALL SEASON 1 EVENTS")
    print("=" * 60)
    
    all_events_data = {}
    
    # Process all 35 events
    for event_num in range(1, 36):
        event_file = reports_dir / f"event_1_{event_num}_leaderboard.md"
        
        if event_file.exists():
            print(f"📊 Processing Event {event_num}...")
            top_10 = extract_top_10_from_event(event_file)
            
            if top_10:
                all_events_data[event_num] = top_10
                print(f"   ✅ Found {len(top_10)} players")
            else:
                print(f"   ❌ No data found")
        else:
            print(f"❌ Event {event_num} file not found: {event_file}")
    
    return all_events_data

def generate_summary_report(all_events_data):
    """Generate a comprehensive summary report"""
    output_file = Path("reports/season_1_top_10_summary.md")
    
    print(f"\n📝 Generating summary report...")
    
    # Count wins by player
    wins_by_player = {}
    top_10_appearances = {}
    
    for event_num, top_10 in all_events_data.items():
        winner = top_10[0]['name']
        wins_by_player[winner] = wins_by_player.get(winner, 0) + 1
        
        for player in top_10:
            name = player['name']
            top_10_appearances[name] = top_10_appearances.get(name, 0) + 1
    
    # Sort by wins, then by top 10 appearances
    sorted_winners = sorted(wins_by_player.items(), key=lambda x: (-x[1], -top_10_appearances.get(x[0], 0)))
    sorted_appearances = sorted(top_10_appearances.items(), key=lambda x: (-x[1], -wins_by_player.get(x[0], 0)))
    
    # Generate markdown report
    markdown_content = []
    markdown_content.append("# 🏆 Season 1 Top 10 Summary")
    markdown_content.append("")
    markdown_content.append("*Generated from all 35 Season 1 events*")
    markdown_content.append("")
    
    # Event winners summary
    markdown_content.append("## 🏆 Event Winners")
    markdown_content.append("")
    markdown_content.append("| Event | Winner | Nationality | Wins | Top 10s |")
    markdown_content.append("|-------|--------|-------------|------|---------|")
    
    for event_num, top_10 in all_events_data.items():
        winner = top_10[0]
        wins = wins_by_player[winner['name']]
        appearances = top_10_appearances[winner['name']]
        markdown_content.append(f"| {event_num:2d} | {winner['name']} | {winner['nationality']} | {wins} | {appearances} |")
    
    markdown_content.append("")
    
    # Top performers summary
    markdown_content.append("## 📊 Top Performers")
    markdown_content.append("")
    markdown_content.append("### Most Event Wins")
    markdown_content.append("")
    markdown_content.append("| Rank | Player | Nationality | Wins | Top 10s |")
    markdown_content.append("|------|--------|-------------|------|---------|")
    
    for i, (player, wins) in enumerate(sorted_winners[:10], 1):
        appearances = top_10_appearances.get(player, 0)
        markdown_content.append(f"| {i:2d} | {player} | - | {wins} | {appearances} |")
    
    markdown_content.append("")
    markdown_content.append("### Most Top 10 Appearances")
    markdown_content.append("")
    markdown_content.append("| Rank | Player | Nationality | Top 10s | Wins |")
    markdown_content.append("|------|--------|-------------|---------|------|")
    
    for i, (player, appearances) in enumerate(sorted_appearances[:10], 1):
        wins = wins_by_player.get(player, 0)
        markdown_content.append(f"| {i:2d} | {player} | - | {appearances} | {wins} |")
    
    markdown_content.append("")
    
    # Detailed event breakdown
    markdown_content.append("## 📋 Event-by-Event Top 10")
    markdown_content.append("")
    
    for event_num in range(1, 36):
        if event_num in all_events_data:
            markdown_content.append(f"### Event {event_num}")
            markdown_content.append("")
            markdown_content.append("| Rank | Player | Nationality | Performance | Points |")
            markdown_content.append("|------|--------|-------------|-------------|--------|")
            
            for player in all_events_data[event_num]:
                markdown_content.append(f"| {player['rank']:3d} | {player['name']} | {player['nationality']} | {player['performance']:>10.1f} | {player['points']:>6} |")
            
            markdown_content.append("")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_content))
    
    print(f"✅ Summary report saved to: {output_file}")
    
    # Print quick stats
    print(f"\n📊 QUICK STATS:")
    print(f"   Total events processed: {len(all_events_data)}")
    print(f"   Unique event winners: {len(wins_by_player)}")
    print(f"   Players with top 10 appearances: {len(top_10_appearances)}")
    
    if sorted_winners:
        top_winner, top_wins = sorted_winners[0]
        print(f"   Most wins: {top_winner} ({top_wins} events)")
    
    if sorted_appearances:
        top_appearance_player, top_appearances_count = sorted_appearances[0]
        print(f"   Most top 10s: {top_appearance_player} ({top_appearances_count} appearances)")

if __name__ == "__main__":
    all_events_data = extract_all_top_10()
    
    if all_events_data:
        generate_summary_report(all_events_data)
        print(f"\n🎉 Successfully processed {len(all_events_data)} events!")
    else:
        print("\n❌ No event data found!") 