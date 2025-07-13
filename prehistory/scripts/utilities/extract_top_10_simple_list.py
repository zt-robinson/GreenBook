#!/usr/bin/env python3
"""
Extract Top 10 Players - Simple List Format

This script creates a simple list showing each event and its top 10 players.
"""

import os
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
                        top_10.append(name)
                    else:
                        break  # Stop after top 10
        
        return top_10
        
    except Exception as e:
        print(f"❌ Error reading {event_file}: {e}")
        return []

def generate_simple_list():
    """Generate a simple list of top 10 for each event"""
    reports_dir = Path("reports")
    output_file = Path("reports/season_1_top_10_simple_list.md")
    
    print("🏆 EXTRACTING TOP 10 - SIMPLE LIST FORMAT")
    print("=" * 50)
    
    markdown_content = []
    markdown_content.append("# Season 1 Top 10 - Event by Event")
    markdown_content.append("")
    markdown_content.append("*Simple list format showing top 10 players for each event*")
    markdown_content.append("")
    
    # Process all 35 events
    for event_num in range(1, 36):
        event_file = reports_dir / f"event_1_{event_num}_leaderboard.md"
        
        if event_file.exists():
            print(f"📊 Processing Event {event_num}...")
            top_10 = extract_top_10_from_event(event_file)
            
            if top_10:
                markdown_content.append(f"## Event {event_num}")
                markdown_content.append("")
                for i, player in enumerate(top_10, 1):
                    markdown_content.append(f"{i}. {player}")
                markdown_content.append("")
                print(f"   ✅ Found {len(top_10)} players")
            else:
                print(f"   ❌ No data found")
        else:
            print(f"❌ Event {event_num} file not found: {event_file}")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_content))
    
    print(f"✅ Simple list saved to: {output_file}")
    
    # Also print to console
    print("\n" + "="*50)
    print("SEASON 1 TOP 10 - SIMPLE LIST")
    print("="*50)
    
    for event_num in range(1, 36):
        event_file = reports_dir / f"event_1_{event_num}_leaderboard.md"
        if event_file.exists():
            top_10 = extract_top_10_from_event(event_file)
            if top_10:
                print(f"\nEvent {event_num}:")
                for i, player in enumerate(top_10, 1):
                    print(f"  {i}. {player}")

if __name__ == "__main__":
    generate_simple_list() 