#!/usr/bin/env python3
"""
Extract All 150 Players - Table Format

This script creates a table with 35 rows (events) and 151 columns (event + 150 players).
"""

import os
from pathlib import Path

def extract_all_players_from_event(event_file):
    """Extract all 150 players from a single event leaderboard"""
    all_players = []
    
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
                    name = parts[1]
                    all_players.append(name)
        
        return all_players
        
    except Exception as e:
        print(f"❌ Error reading {event_file}: {e}")
        return []

def generate_full_table():
    """Generate a table with events as rows and all 150 players as columns"""
    reports_dir = Path("reports")
    output_file = Path("reports/season_1_all_150_table.md")
    
    print("🏆 EXTRACTING ALL 150 PLAYERS - TABLE FORMAT")
    print("=" * 60)
    
    # Collect all data
    all_events_data = {}
    
    for event_num in range(1, 36):
        event_file = reports_dir / f"event_1_{event_num}_leaderboard.md"
        
        if event_file.exists():
            print(f"📊 Processing Event {event_num}...")
            all_players = extract_all_players_from_event(event_file)
            
            if all_players:
                all_events_data[event_num] = all_players
                print(f"   ✅ Found {len(all_players)} players")
            else:
                print(f"   ❌ No data found")
        else:
            print(f"❌ Event {event_num} file not found: {event_file}")
    
    # Generate table
    markdown_content = []
    markdown_content.append("# Season 1 All 150 Players - Event Table")
    markdown_content.append("")
    markdown_content.append("*Table showing all 150 players for each event*")
    markdown_content.append("")
    markdown_content.append("**Note:** This is a very wide table. Consider viewing in a wide window or using horizontal scroll.")
    markdown_content.append("")
    
    # Create header row
    header = "| Event |"
    for i in range(1, 151):
        header += f" {i} |"
    
    separator = "|------|"
    for i in range(1, 151):
        separator += "---|"
    
    markdown_content.append(header)
    markdown_content.append(separator)
    
    # Create data rows
    for event_num in range(1, 36):
        if event_num in all_events_data:
            all_players = all_events_data[event_num]
            row = f"| {event_num:2d} |"
            for player in all_players:
                row += f" {player} |"
            markdown_content.append(row)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_content))
    
    print(f"✅ Full table saved to: {output_file}")
    print(f"📊 Table dimensions: 35 rows × 151 columns")
    
    # Also create a CSV version for easier viewing
    csv_output_file = Path("reports/season_1_all_150_table.csv")
    csv_content = []
    
    # CSV header
    csv_header = "Event"
    for i in range(1, 151):
        csv_header += f",{i}"
    csv_content.append(csv_header)
    
    # CSV data rows
    for event_num in range(1, 36):
        if event_num in all_events_data:
            all_players = all_events_data[event_num]
            row = str(event_num)
            for player in all_players:
                row += f",{player}"
            csv_content.append(row)
    
    with open(csv_output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(csv_content))
    
    print(f"✅ CSV version saved to: {csv_output_file}")
    
    # Print a sample (first 5 events, first 10 players each)
    print("\n" + "="*80)
    print("SAMPLE - FIRST 5 EVENTS, TOP 10 PLAYERS EACH")
    print("="*80)
    
    sample_header = "| Event | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th | 8th | 9th | 10th |"
    sample_separator = "|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|"
    
    print(sample_header)
    print(sample_separator)
    
    for event_num in range(1, 6):
        if event_num in all_events_data:
            all_players = all_events_data[event_num]
            row = f"| {event_num:2d} |"
            for i in range(10):  # Just top 10 for sample
                row += f" {all_players[i]} |"
            print(row)

if __name__ == "__main__":
    generate_full_table() 