# Dynamic Payout Integration for The Sovereign Tournament

## Overview

The Sovereign Tournament now uses a dynamic payout system that calculates payouts after the cut is determined, rather than using pre-calculated static payouts. This provides more accurate and fair payout distribution that adapts to the actual tournament field.

## Key Features

### 1. Dynamic Calculation
- Payouts are calculated after round 2 when the cut is determined
- Adapts to the actual number of players who make the cut
- No pre-calculated static payout structure stored in database

### 2. Anchor Position System
- **Winner**: 20% of purse (The Sovereign Tournament and Royal Open Championship)
- **Runner-up**: 12% of purse
- **3rd Place**: 7.5% of purse
- **4th Place**: 5.5% of purse
- **5th Place**: 4.5% of purse

### 3. Distribution Targets
- **Top 10**: 50% of total purse
- **Top 25**: 70% of total purse  
- **Remaining positions**: 30% of total purse

### 4. Tie Handling
- Tied players receive the average payout of their tied positions
- Example: Two players tied for 1st each get 16.5% (average of 1st and 2nd place percentages)

## Integration Points

### Tournament Creation
```python
# The Sovereign Tournament is created without static payout structure
tournament_id = tournament_logic.create_tournament(
    tournament_name="The Sovereign Tournament",
    course_id=course_id,
    start_date="2025-08-15",
    season_number=0,
    week_number=1
)
# Note: No payout_structure entries are created in database
```

### After Tournament Completion
```python
# Calculate dynamic payouts after cut is determined
tournament_results = [
    {
        'player_id': 1,
        'name': 'Player Name',
        'position': 1,
        'made_cut': True,
        'total_score': 280
    },
    # ... more results
]

payouts = tournament_logic.calculate_dynamic_payouts(tournament_id, tournament_results)
```

## Database Changes

### Tournament Creation
- **Before**: Static payout structure inserted during tournament creation
- **After**: No payout structure for The Sovereign Tournament until after completion

### Payout Calculation
- **Before**: Pre-calculated percentages from event type configuration
- **After**: Dynamic calculation based on actual cut size and tournament results

## Benefits

1. **Accuracy**: Payouts reflect actual tournament field size
2. **Fairness**: Ties are handled properly with averaged payouts
3. **Flexibility**: System adapts to different cut sizes
4. **Consistency**: Distribution targets are always met regardless of field size

## Usage in Tournament Simulation

### Step 1: Create Tournament
```python
tournament_id = tournament_logic.create_tournament(
    tournament_name="The Sovereign Tournament",
    course_id=course_id,
    start_date="2025-08-15",
    season_number=0,
    week_number=1
)
```

### Step 2: Simulate Tournament Rounds
```python
# Simulate rounds 1-4 and determine cut after round 2
# Store results in tournament_results table
```

### Step 3: Calculate Final Results
```python
# After round 4, get final tournament results
tournament_results = get_tournament_final_results(tournament_id)

# Calculate dynamic payouts
payouts = tournament_logic.calculate_dynamic_payouts(tournament_id, tournament_results)
```

### Step 4: Display Results
```python
for payout in payouts:
    print(f"{payout['position']}. {payout['player_name']}: ${payout['amount']:,}")
```

## Configuration

The dynamic payout system is automatically used for:
- **The Sovereign Tournament**
- **Royal Open Championship** (winner gets 20%)
- **American Open Championship** (winner gets 18%)
- **AGA Championship** (winner gets 18%)

Other tournaments continue to use the static payout system.

## Testing

Run the test script to see the system in action:
```bash
cd greenbook && source venv/bin/activate && cd .. && python test_sovereign_dynamic_payouts.py
```

This will demonstrate:
- Different cut sizes
- Tie handling
- Distribution target verification
- Comparison with static payout system 