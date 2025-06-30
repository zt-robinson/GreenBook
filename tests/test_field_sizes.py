#!/usr/bin/env python3
"""
Test script to verify field sizes and cut lines for all event types
"""

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))

from core.event_types import EventTypeManager

def test_field_sizes_and_cuts():
    """Test field sizes and cut lines for all event types"""
    
    event_type_manager = EventTypeManager()
    
    print("=== FIELD SIZES AND CUT LINES TEST ===\n")
    
    # Test standard events
    print("1. Standard Events:")
    for i in range(3):
        config = event_type_manager.get_tournament_config(f"Standard Event {i+1}")
        print(f"   Event {i+1}: Field size {config['field_size']}, Cut line: {config['cut_line']['description']}")
    
    # Test majors
    print("\n2. Majors:")
    majors = [
        "The Sovereign Tournament",
        "American Open Championship", 
        "Royal Open Championship",
        "AGA Championship"
    ]
    
    for major in majors:
        config = event_type_manager.get_tournament_config(major)
        print(f"   {major}:")
        print(f"     Field size: {config['field_size']}")
        print(f"     Cut line: {config['cut_line']['description']}")
    
    # Test invitationals
    print("\n3. Invitationals:")
    invitationals = [
        "The Players Championship",
        "Arnold Palmer Invitational", 
        "Memorial Tournament"
    ]
    
    for invitational in invitationals:
        config = event_type_manager.get_tournament_config(invitational)
        print(f"   {invitational}:")
        print(f"     Field size: {config['field_size']}")
        print(f"     Cut line: {config['cut_line']['description']}")
    
    # Test multiple Sovereign Tournament generations to show randomness
    print("\n4. The Sovereign Tournament - Multiple Generations (showing randomness):")
    for i in range(5):
        config = event_type_manager.get_tournament_config("The Sovereign Tournament")
        print(f"   Generation {i+1}: Field size {config['field_size']}, Cut line: {config['cut_line']['description']}")
    
    print("\n" + "=" * 50)
    print("✅ Field Sizes and Cut Lines Test Complete!")

if __name__ == "__main__":
    test_field_sizes_and_cuts() 