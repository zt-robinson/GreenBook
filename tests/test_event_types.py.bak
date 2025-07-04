#!/usr/bin/env python3
"""
Test script to create one tournament of each event type
"""

from scripts.create_single_tournament import create_tournament

def test_event_types():
    """Test creating one tournament of each event type"""
    
    print("🧪 Testing Event Type Parameters")
    print("=" * 50)
    
    # Test 1: Standard Event
    print("\n1️⃣ Testing STANDARD Event:")
    print("-" * 30)
    standard_id = create_tournament("Sony Open in Hawaii", "standard", start_date="2025-07-04")
    
    # Test 2: Major Event
    print("\n2️⃣ Testing MAJOR Event:")
    print("-" * 30)
    major_id = create_tournament("The Sovereign Tournament", "major", start_date="2025-07-07")
    
    # Test 3: Invitational Event
    print("\n3️⃣ Testing INVITATIONAL Event:")
    print("-" * 30)
    invitational_id = create_tournament("The Memorial Tournament", "invitational", start_date="2025-07-10")
    
    print("\n" + "=" * 50)
    print("🎉 Event Type Testing Complete!")
    print(f"   Standard Event ID: {standard_id}")
    print(f"   Major Event ID: {major_id}")
    print(f"   Invitational Event ID: {invitational_id}")
    
    if all([standard_id, major_id, invitational_id]):
        print("\n✅ All event types created successfully!")
        print("   -> Check the schedule page to see the generated tournaments")
        print("   -> Each should have different field sizes, purses, and prestige levels")
        print("   -> Standard: Random field size 144-165, random purse $7.9M-$9.5M")
        print("   -> Major: Fixed field size 156, random purse $21M-$25M, high prestige")
        print("   -> Invitational: Random field size 72-90, random purse $12M-$18M, no cut")
    else:
        print("\n❌ Some event types failed to create")

if __name__ == "__main__":
    test_event_types() 