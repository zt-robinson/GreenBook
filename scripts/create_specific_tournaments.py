#!/usr/bin/env python3
"""
Create specific tournaments for testing event type parameters
"""

try:
    from scripts.create_single_tournament import create_tournament
except ImportError:
    from create_single_tournament import create_tournament

def create_specific_tournaments():
    """Create the specific tournaments requested for testing"""
    
    print("🎯 Creating Specific Tournaments for Testing")
    print("=" * 60)
    
    tournaments = [
        # Standard Event
        {"name": "Standard Event", "event_type": "standard", "date": "2025-07-04"},
        
        # Invitational Event  
        {"name": "Invitational Event", "event_type": "invitational", "date": "2025-07-07"},
        
        # Majors (these will use tournament overrides)
        {"name": "The Sovereign Tournament", "event_type": None, "date": "2025-07-10"},
        {"name": "The American Open", "event_type": None, "date": "2025-07-13"},
        {"name": "The Royal Open", "event_type": None, "date": "2025-07-16"},
        {"name": "The AGA Championship", "event_type": None, "date": "2025-07-19"},
        
        # Special Event (Continental Championship - will use special event override)
        {"name": "The Continental Championship", "event_type": None, "date": "2025-07-22"},
    ]
    
    created_tournaments = []
    
    for i, tournament in enumerate(tournaments, 1):
        print(f"\n{i}️⃣ Creating: {tournament['name']}")
        print("-" * 40)
        
        tournament_id = create_tournament(
            tournament_name=tournament['name'],
            event_type=tournament['event_type'],  # None means use tournament name to determine type
            start_date=tournament['date']
        )
        
        if tournament_id:
            created_tournaments.append({
                'id': tournament_id,
                'name': tournament['name'],
                'event_type': tournament['event_type'] or 'auto-determined',
                'date': tournament['date']
            })
            print(f"✅ Successfully created {tournament['name']}")
        else:
            print(f"❌ Failed to create {tournament['name']}")
    
    print("\n" + "=" * 60)
    print("🎉 Tournament Creation Summary")
    print("=" * 60)
    
    for tournament in created_tournaments:
        print(f"   {tournament['name']} (ID: {tournament['id']}) - {tournament['event_type']}")
    
    print(f"\n✅ Created {len(created_tournaments)} out of {len(tournaments)} tournaments")
    
    if len(created_tournaments) == len(tournaments):
        print("\n🎯 All tournaments created successfully!")
        print("   -> Check the schedule page to verify event type parameters")
        print("   -> Each tournament should have appropriate field sizes, purses, and prestige")
        print("   -> The Sovereign Tournament should have field size 90-114")
        print("   -> The Continental Championship should have $30M purse")
    else:
        print(f"\n⚠️ {len(tournaments) - len(created_tournaments)} tournaments failed to create")

if __name__ == "__main__":
    create_specific_tournaments() 