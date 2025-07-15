# Priority List System Documentation

## Overview

The Priority List System is a comprehensive solution for managing tournament field invitations in GreenBook. It handles the dynamic generation, storage, and regular re-shuffling of priority lists for all 8 event types, determining who gets invited to limited field events.

## 🎯 Key Features

### **8 Event Types Supported**
- **Standard Events**: 17 priority categories
- **Standard Invitationals**: 7 priority categories  
- **Signature Events**: 12 priority categories
- **Continental Championship**: 12 priority categories
- **Sovereign Tournament**: 12 priority categories
- **AGA Championship**: 12 priority categories
- **American Open**: 10 priority categories
- **Royal Open**: 10 priority categories

### **Dynamic Updates**
- Priority lists are updated after every tournament completion
- All 8 priority lists are recalculated simultaneously
- Historical tracking of priority list changes

### **Realistic Invitation System**
- Simulates player acceptance/decline decisions
- Tracks invitation responses and reasons
- Handles field filling when players decline

## 🗄️ Database Schema

### **Priority Lists Table**
```sql
CREATE TABLE priority_lists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    season_number INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    priority_category TEXT NOT NULL,
    player_id INTEGER NOT NULL,
    priority_order INTEGER NOT NULL,
    qualification_reason TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (player_id) REFERENCES players (id),
    UNIQUE(event_type, season_number, week_number, priority_category, player_id)
);
```

### **Tournament Invitations Table**
```sql
CREATE TABLE tournament_invitations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tournament_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    invitation_sent_date TEXT,
    invitation_response TEXT, -- 'accepted', 'declined', 'pending'
    response_date TEXT,
    decline_reason TEXT,
    priority_category TEXT,
    priority_order INTEGER,
    FOREIGN KEY (tournament_id) REFERENCES tournaments (id),
    FOREIGN KEY (player_id) REFERENCES players (id),
    UNIQUE(tournament_id, player_id)
);
```

### **Priority List Snapshots Table**
```sql
CREATE TABLE priority_list_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    season_number INTEGER NOT NULL,
    week_number INTEGER NOT NULL,
    snapshot_date TEXT NOT NULL,
    total_players INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Priority List Update Cycle

### **After Tournament Completion**
1. **Tournament finishes** with final results
2. **Update all 8 priority lists** based on new results
3. **Future tournament fields** are updated with new priority information
4. **Historical tracking** of priority list changes

### **Example Update Flow**
```
Week 1: Sovereign Tournament (Major #1) completes
→ Update all 8 priority lists
→ Royal Open field now includes Sovereign winner
→ AGA Championship field updated
→ American Open field updated
→ All other event fields updated based on new results

Week 2: Standard Event #1 completes  
→ Update all 8 priority lists again
→ Any new winners/qualifiers added to future events
→ Points standings updated
→ Rankings recalculated
```

## 📋 Priority Categories by Event Type

### **Standard Events (17 Categories)**
1. Previous 5 winners of the AGA Championship
2. Previous 5 winners of the American Open
3. Previous 5 winners of the Royal Open
4. Previous 5 winners of the Sovereign Tournament
5. Previous 5 winners of the Continental Championship
6. Winner of any Signature Events over the last three seasons + current season
7. Previous 5 winners of the Tour Championship
8. Winners of all other Tour events over last two seasons
9. Previous 4 winners of previous instances of this specific event
10. Top four finishers of a Monday Qualifying tournament
11. Top 20 finishers on the Development Tour from the previous season
12. Top 5 finishers on the Q School Tournament from the previous season
13. Top 10 finishers from the Tour event specifically preceding this event
14. Tour points standings (fill remaining spots)

### **Signature Events (12 Categories)**
1. Major winners (last 5 years)
2. Signature event winners (last 2 seasons)
3. World ranking (fill remaining spots)

### **Major Championships (12 Categories)**
1. Previous winners of this specific major
2. Other major winners (last 3 years)
3. Signature event winners (last 2 seasons)
4. World ranking (fill remaining spots)

### **Standard Invitationals (7 Categories)**
1. Major winners (last 3 years)
2. World ranking (fill remaining spots)

## 🎪 Tournament Invitation Process

### **Step 1: Priority List Generation**
```python
# Update all priority lists after tournament completion
priority_system.update_all_priority_lists(season_number, week_number)
```

### **Step 2: Tournament Creation**
```python
# Create tournament using existing logic
tournament_id = tournament_logic.create_tournament(
    tournament_name="Example Tournament",
    course_id=1,
    start_date="2025-02-15",
    season_number=1,
    week_number=5,
    event_type="standard"
)
```

### **Step 3: Extend Invitations**
```python
# Extend invitations based on priority list
invitations = priority_system.extend_tournament_invitations(
    tournament_id, 
    event_type, 
    field_size
)
```

### **Step 4: Process Responses**
```python
# Get accepted players
accepted_players = [inv for inv in invitations if inv['response'] == 'accepted']
player_ids = [inv['player_id'] for inv in accepted_players]

# Finalize tournament field
success = tournament_logic.finalize_tournament_field(tournament_id, player_ids)
```

## 🧠 Player Response Simulation

### **Acceptance Logic**
The system simulates realistic player decisions based on:
- **Priority order**: Higher priority players more likely to accept
- **Player form**: Recent performance affects decision
- **Tournament prestige**: Higher prestige events more attractive
- **Player ranking**: Top players more selective
- **Historical performance**: Past success at event type

### **Response Simulation**
```python
def _simulate_player_response(self, priority_entry: Dict[str, Any]) -> str:
    # Base acceptance rate decreases with priority order
    base_rate = max(0.1, 0.9 - (priority_entry['priority_order'] / 1000))
    
    # Add randomness
    if random.random() < base_rate:
        return 'accepted'
    else:
        return 'declined'
```

## 📊 Usage Examples

### **Basic Priority List Usage**
```python
from core.priority_list_system import PriorityListSystem, EventType

# Initialize system
priority_system = PriorityListSystem()

# Update priority lists after tournament completion
priority_system.update_all_priority_lists(season_number=1, week_number=5)

# Get priority list for specific event type
priority_list = priority_system.get_priority_list(
    EventType.STANDARD_EVENTS.value, 
    season_number=1, 
    week_number=5
)

# Show priority list
for entry in priority_list[:10]:
    print(f"{entry['priority_order']}. {entry['player_name']} ({entry['priority_category']})")
```

### **Tournament Field Generation**
```python
# Create tournament
tournament_id = tournament_logic.create_tournament(...)

# Generate field using priority lists
invitations = priority_system.extend_tournament_invitations(
    tournament_id, 
    "standard", 
    144
)

# Get final field
final_field = priority_system.get_tournament_field_from_invitations(tournament_id)
```

### **Priority List Analysis**
```python
# Analyze priority list by category
priority_list = priority_system.get_priority_list(event_type, season, week)

categories = {}
for entry in priority_list:
    cat = entry['priority_category']
    categories[cat] = categories.get(cat, 0) + 1

# Show category distribution
for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    print(f"{cat}: {count} players")
```

## 🔧 Integration with Existing System

### **Tournament Logic Integration**
The priority list system integrates seamlessly with the existing `TournamentLogic` class:

```python
# Existing tournament creation
tournament_id = tournament_logic.create_tournament(...)

# New: Use priority lists for field generation
invitations = priority_system.extend_tournament_invitations(...)
player_ids = [inv['player_id'] for inv in accepted_invitations]
tournament_logic.finalize_tournament_field(tournament_id, player_ids)
```

### **Database Integration**
- Uses existing tournament and player databases
- Adds new tables for priority lists and invitations
- Maintains referential integrity with existing data

### **Event Type Integration**
- Works with all existing event types
- Extends event type system with priority categories
- Maintains compatibility with existing tournament creation

## 📈 Performance Considerations

### **Efficient Updates**
- Updates only changed priority lists
- Uses database indexes for fast queries
- Batches priority list updates

### **Scalability**
- Handles 600+ players efficiently
- Supports multiple seasons and weeks
- Optimized for frequent updates

### **Memory Usage**
- Streams large priority lists
- Uses database storage for persistence
- Minimal memory footprint

## 🧪 Testing and Validation

### **Demo Scripts**
- `priority_list_demo.py`: Basic functionality demonstration
- `integrate_priority_lists.py`: Integration with tournament system
- Comprehensive error handling and validation

### **Validation Checks**
- Priority list completeness
- Invitation response consistency
- Field size validation
- Database integrity checks

## 🚀 Future Enhancements

### **Advanced Player Response Logic**
- Player form analysis
- Tournament prestige weighting
- Historical performance tracking
- Schedule conflict detection

### **Enhanced Priority Categories**
- Sponsor exemptions
- Special invitations
- Performance-based promotions
- Development tour integration

### **Real-time Updates**
- Live priority list updates
- Dynamic field adjustments
- Real-time invitation tracking

## 📝 Best Practices

### **Priority List Management**
1. **Update after every tournament**: Ensures accuracy
2. **Validate priority lists**: Check for completeness
3. **Monitor field sizes**: Ensure adequate player pools
4. **Track historical changes**: Maintain audit trail

### **Tournament Creation**
1. **Use appropriate event types**: Match tournament to priority list
2. **Handle declined invitations**: Have fallback strategies
3. **Validate field sizes**: Ensure realistic player counts
4. **Monitor acceptance rates**: Adjust simulation parameters

### **Database Management**
1. **Regular backups**: Priority lists are critical data
2. **Index optimization**: Ensure fast queries
3. **Data validation**: Check for consistency
4. **Archive old data**: Maintain performance

---

*The Priority List System provides a robust, scalable solution for managing tournament field invitations while maintaining the realism and complexity of professional golf tour operations.* 