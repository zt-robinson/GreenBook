#!/usr/bin/env python3
"""
Debug script for major points structure
"""

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))

from core.event_types import event_type_manager

def debug_major_points():
    """Debug the major points structure"""
    print("🔍 Debugging Major Points Structure\n")
    
    major_name = "The Masters"
    config = event_type_manager.get_tournament_config(major_name)
    
    print(f"Tournament: {major_name}")
    print(f"Event Type: {config['event_type']}")
    print(f"Cut Line: {config['cut_line']}")
    print()
    
    # Check points structure
    points_structure = config['points_structure']
    print("Points Structure Keys:")
    for key in sorted(points_structure.keys()):
        print(f"  {key}: {points_structure[key]}")
    print()
    
    # Test specific positions
    cut_line_position = config['cut_line']['value']
    print(f"Testing position {cut_line_position} (cut line):")
    
    # Check if the position key exists
    position_key = f'top_{cut_line_position}'
    print(f"  Looking for key: '{position_key}'")
    print(f"  Key exists: {position_key in points_structure}")
    if position_key in points_structure:
        print(f"  Value: {points_structure[position_key]}")
    else:
        print(f"  Key not found, using 'made_cut': {points_structure['made_cut']}")
    
    # Test the get_points_for_position method
    points = event_type_manager.get_points_for_position(major_name, cut_line_position)
    print(f"  get_points_for_position result: {points}")
    
    # Test a few other positions
    print(f"\nTesting other positions:")
    for pos in [1, 2, 3, 4, 5, 10, 20, 30, 40, 50]:
        points = event_type_manager.get_points_for_position(major_name, pos)
        print(f"  Position {pos}: {points}")

if __name__ == "__main__":
    debug_major_points() 