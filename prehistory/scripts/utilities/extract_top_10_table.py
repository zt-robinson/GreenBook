#!/usr/bin/env python3
"""
Extract Top 10 Players - Table Format

This script creates a table with 35 rows (events) and 11 columns (event + 10 players).
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

def generate_table():
    """Generate a table with events as rows and top 10 players as columns"""
    reports_dir = Path("reports")
    output_file = Path("reports/season_1_top_10_table.md")
    
    print("🏆 EXTRACTING TOP 10 - TABLE FORMAT")
    print("=" * 50)
    
    # Collect all data
    all_events_data = {}
    
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
    
    # Generate table
    markdown_content = []
    markdown_content.append("# Season 1 Top 10 - Event Table")
    markdown_content.append("")
    markdown_content.append("*Table showing top 10 players for each event*")
    markdown_content.append("")
    
    # Create header row
    header = "| Event | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th | 10th |"
    separator = "|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|"
    
    markdown_content.append(header)
    markdown_content.append(separator)
    
    # Create data rows
    for event_num in range(1, 36):
        if event_num in all_events_data:
            top_10 = all_events_data[event_num]
            row = f"| {event_num:2d} |"
            for player in top_10:
                row += f" {player} |"
            markdown_content.append(row)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_content))
    
    print(f"✅ Table saved to: {output_file}")
    
    # Also print to console
    print("\n" + "="*80)
    print("SEASON 1 TOP 10 - TABLE FORMAT")
    print("="*80)
    print(header)
    print(separator)
    
    for event_num in range(1, 36):
        if event_num in all_events_data:
            top_10 = all_events_data[event_num]
            row = f"| {event_num:2d} |"
            for player in top_10:
                row += f" {player} |"
            print(row)

if __name__ == "__main__":
    generate_table() 