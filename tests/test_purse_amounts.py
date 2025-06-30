#!/usr/bin/env python3
"""
Test script to verify purse amounts for all event types
"""

# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), 'greenbook'))

from core.event_types import EventTypeManager

def test_purse_amounts():
    """Test purse amounts for all event types"""
    
    event_type_manager = EventTypeManager()
    
    print("=== PURSE AMOUNTS TEST ===\n")
    
    # Test standard events
    print("1. Standard Events:")
    for i in range(3):
        config = event_type_manager.get_tournament_config(f"Standard Event {i+1}")
        purse = config['purse_base']
        print(f"   Event {i+1}: ${purse:,} (${purse/1_000_000:.1f}M)")
    
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
        purse = config['purse_base']
        print(f"   {major}: ${purse:,} (${purse/1_000_000:.1f}M)")
    
    # Test invitationals (using generic invitational event type)
    print("\n3. Invitationals (Generic):")
    for i in range(3):
        # Create a generic invitational name to test the base event type
        config = event_type_manager.get_tournament_config(f"Invitational Event {i+1}")
        purse = config['purse_base']
        print(f"   Invitational {i+1}: ${purse:,} (${purse/1_000_000:.1f}M)")
    
    # Test multiple invitational generations to show randomness
    print("\n4. Invitational - Multiple Generations (showing randomness):")
    for i in range(5):
        config = event_type_manager.get_tournament_config("Invitational Test")
        purse = config['purse_base']
        print(f"   Generation {i+1}: ${purse:,} (${purse/1_000_000:.1f}M)")
    
    print("\n" + "=" * 50)
    print("✅ Purse Amounts Test Complete!")

if __name__ == "__main__":
    test_purse_amounts() 