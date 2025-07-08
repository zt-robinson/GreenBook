# Tournament/Event System Plan

## Overview
Building a tournament/event system from scratch for the golf simulation. This document outlines the plan and design decisions.

## Event Types
Based on user specification:

### Standard Events
- **Field size**: 144-165 players (multiple of 3)
- **Cut line**: Top 65 and ties
- **Winner points**: 500 points
- **Purse**: $7.9M-$9.5M (random, rounded to $100K)
- **Frequency**: Most common event type

### Standard Invitationals
- **Field size**: 72 players
- **Cut line**: No cut - all players play 4 rounds
- **Winner points**: 600 points
- **Purse**: $10M-$12M (random, rounded to $500K)

### Signature Events
- **Field size**: 72 players
- **Cut line**: No cut - all players play 4 rounds
- **Winner points**: 700 points
- **Purse**: $18M-$20M (random, rounded to $500K)

### The Continental Championship
- **Field size**: 123-144 players (multiple of 3)
- **Cut line**: Top 65 and ties
- **Winner points**: 750 points
- **Purse**: Flat $30M
- **Prestige**: 0.95
- **Frequency**: Once per season, precedes all majors

### Major Championships (4 total)
All majors award 750 points to winner, purse $22M-$25M (random, rounded to $1M), and have maximum prestige (1.0)

#### The Sovereign Tournament
- **Field size**: 90-114 players (multiple of 3)
- **Cut line**: Top 53 and ties advance to weekend
- **Winner points**: 750 points (major championship points structure)
- **Purse**: $22M-$25M (random, rounded to $1M)
- **Prestige**: 1.0 (maximum for major championships)
- **Frequency**: Once per season, first major of the year
- **Description**: The season's opening major championship, featuring a select field of the world's best players

#### The AGA Championship
- **Field size**: 156 players
- **Cut line**: Top 70 and ties advance to weekend
- **Winner points**: 750 points (major championship points structure)
- **Purse**: $22M-$25M (random, rounded to $1M)
- **Prestige**: 1.0 (maximum for major championships)
- **Frequency**: Once per season, second major of the year
- **Description**: Traditional major championship with full field

#### The American Open
- **Field size**: 156 players
- **Cut line**: Top 67 and ties advance to weekend
- **Winner points**: 750 points (major championship points structure)
- **Purse**: $22M-$25M (random, rounded to $1M)
- **Prestige**: 1.0 (maximum for major championships)
- **Frequency**: Once per season, third major of the year
- **Description**: National open championship with full field

#### The Royal Open
- **Field size**: 156 players
- **Cut line**: Top 70 and ties advance to weekend
- **Winner points**: 750 points (major championship points structure)
- **Purse**: $22M-$25M (random, rounded to $1M)
- **Prestige**: 1.0 (maximum for major championships)
- **Frequency**: Once per season, final major of the year
- **Description**: Last major championship of the year with full field

**Major Championship Frequency**: Once per season each, spaced 4-5 events apart

## FedExCup Points Distribution Table (All Event Types)

| Position | Standard Event | Standard Invitational | Signature Event | Major/Continental Championship |
|----------|---------------|----------------------|----------------|-------------------------------|
| 1        | 500           | 600                  | 700            | 750                           |
| 2        | 300           | 300                  | 400            | 500                           |
| 3        | 190           | 270                  | 350            | 300                           |
| 4        | 135           | 230                  | 325            | 325                           |
| 5        | 110           | 205                  | 300            | 300                           |
| 6        | 100           | 185                  | 275            | 275                           |
| 7        | 90            | 170                  | 250            | 250                           |
| 8        | 85            | 140                  | 200            | 225                           |
| 9        | 80            | 125                  | 175            | 200                           |
| 10       | 75            | 110                  | 150            | 175                           |
| 11       | 70            | 100                  | 130            | 155                           |
| 12       | 65            | 95                   | 120            | 135                           |
| 13       | 60            | 85                   | 110            | 120                           |
| 14       | 57            | 80                   | 100            | 110                           |
| 15       | 55            | 75                   | 90             | 100                           |
| 16       | 53            | 65                   | 80             | 95                            |
| 17       | 51            | 60                   | 70             | 90                            |
| 18       | 49            | 57                   | 65             | 75                            |
| 19       | 48            | 54                   | 60             | 70                            |
| 20       | 45            | 50                   | 55             | 65                            |
| 21       | 43            | 46                   | 50             | 55                            |
| 22       | 41            | 44                   | 48             | 53                            |
| 23       | 39            | 42                   | 46             | 51                            |
| 24       | 37            | 40                   | 44             | 49                            |
| 25       | 35.5          | 38                   | 42             | 47                            |
| 26       | 34            | 37                   | 40             | 45                            |
| 27       | 32.5          | 35                   | 38             | 43                            |
| 28       | 31            | 33                   | 36             | 41                            |
| 29       | 29.5          | 31                   | 34             | 39                            |
| 30       | 28            | 30                   | 32.5           | 37                            |
| 31       | 26.5          | 28                   | 31             | 35                            |
| 32       | 25.5          | 27                   | 29.5           | 33                            |
| 33       | 23.5          | 25                   | 28             | 31                            |
| 34       | 22            | 24                   | 26.5           | 29                            |
| 35       | 21            | 23                   | 25             | 27                            |
| 36       | 20            | 22                   | 24             | 26                            |
| 37       | 19            | 21                   | 23             | 25                            |
| 38       | 18            | 20                   | 22             | 24                            |
| 39       | 17            | 19                   | 21             | 23                            |
| 40       | 16            | 18                   | 20.25          | 22                            |
| 41       | 15            | 17                   | 19.5           | 21                            |
| 42       | 14            | 16                   | 18.75          | 20.25                         |
| 43       | 13            | 15                   | 18             | 19.5                          |
| 44       | 12            | 14                   | 17.25          | 18.75                         |
| 45       | 11            | 13                   | 16.5           | 18                            |
| 46       | 10.5          | 12                   | 15.75          | 17.25                         |
| 47       | 10            | 11.75                | 15             | 16.5                          |
| 48       | 9.5           | 11.5                 | 14.25          | 15.75                         |
| 49       | 9             | 11.25                | 13.5           | 15                            |
| 50       | 8.5           | 11                   | 13             | 14.25                         |
| 51       | 8             | 10.5                 | 12.5           | 13.5                          |
| 52       | 7.5           | 10                   | 12             | 13                            |
| 53       | 7             | 9.75                 | 11.5           | 12.5                          |
| 54       | 6.5           | 9.5                  | 11             | 12                            |
| 55       | 6             | 9                    | 10.5           | 11.5                          |
| 56       | 5.8           | 8.75                 | 10             | 11                            |
| 57       | 5.6           | 8.5                  | 9.5            | 10.5                          |
| 58       | 5.4           | 8                    | 9              | 10                            |
| 59       | 5.2           | 7.5                  | 8.5            | 8.5                           |
| 60       | 5             | 7                    | 8.25           | 8.25                          |
| 61       | 4.8           | 6.75                 | 7.75           | 8.25                          |
| 62       | 4.6           | 6.5                  | 7.75           | 8.25                          |
| 63       | 4.4           | 6.25                 | 7.5            | 8                             |
| 64       | 4.2           | 6                    | 7.25           | 7.75                          |
| 65       | 4             | 5.75                 | 6.75           | 7.25                          |
| 66       | 3.8           | 5.5                  | 6.75           | 7.25                          |
| 67       | 3.6           | 5.25                 | 6.5            | 6.75                          |
| 68       | 3.4           | 5                    | 6.25           | 6.75                          |
| 69       | 3.2           | 4.75                 | 6.25           | 6.5                           |
| 70       | 3             | 4.5                  | 5.75           | 6.25                          |
| 71       | 2.9           | 4.25                 | 5.5            | 6.25                          |
| 72       | 2.8           | 4                    | 5.25           | 5.5                           |
| 73       | 2.7           | 3.75                 | 5              | 5.5                           |
| 74       | 2.6           | 3.5                  | 4.75           | 5.25                          |
| 75       | 2.5           | 3.25                 | 4.5            | 5.25                          |
| 76       | 2.4           | 3                    | 4.25           | 4.75                          |
| 77       | 2.3           | 2.9                  | 4              | 4.5                           |
| 78       | 2.2           | 2.8                  | 3.75           | 4.25                          |
| 79       | 2.1           | 2.7                  | 3.5            | 4                             |
| 80       | 2             | 2.6                  | 3.25           | 3.75                          |
| 81       | 1.9           | 2.5                  | 3              | 3.5                           |
| 82       | 1.8           | 2.25                 | 2.75           | 3.25                          |
| 83       | 1.7           | 2                    | 2.5            | 2.5                           |
| 84       | 1.6           | 1.9                  | 2.25           | 2.25                          |
| 85       | 1.5           | 1.75                 | 2              | 2.5                           |

**Note:** This table is the authoritative source for points distribution in the simulation.

## Purse Distribution Structure

### Core Principle
The total purse payout must always equal exactly 100% of the event purse, regardless of how many players make the cut due to ties. In all cases, the percentage awarded to a given position must exceed the percentage paid to all lower positions, and be less than the percentage paid to all higher positions. At no point should a player be entitled to a payout percentage equal to that of a player in any other place.

### Ties

In the event that multiple players tie at a given position, the proper solution is to add the percentages that each tied player at that position would be entitled to if they finished consecutively, and then divide that amount by the number of players tied at that position. For example, say five players are tied for 6th place resulting in these five players essentially occupying spots 6, 7, 8, 9, and 10. The payout percentages awarded to places 6, 7, 8, 9, and 10 are added together and then divided by 5; this percentage is then awarded to all the players tied for 6th. This has the effect of ensuring all tied players receive equal payment, while also ensuring that their aggregate payment percentage is exactly equal to what it would have been had they finished consecutively (and therefore there are no negative effects to the rest of the players entitled to a payout).    

## Event-Specific Payout Frameworks

### Standard Events
- **Cut line**: Top 65 and ties
- **Payout system**: Variable based on number of players making cut
- **Framework**: Uses the unified 53-85 CSV file for all scenarios

### Standard Invitationals
- **Cut line**: None (all players paid)
- **Field size**: Fixed at 72 players
- **Payout system**: Static percentage table (same as Signature Events)
- **Framework**: Uses the Signature Events payout table

**Standard Events use the unified payout system from the 53-85 CSV file.**

Standard Events have a cut line of "Top 65 and ties", which means the number of paid players can vary from 65 to 75 (or potentially more in rare cases). The payout percentages for all scenarios from 53 to 85 players are stored in `greenbook/data/53_85_payout_structure.csv`.

**Implementation**: The system loads the CSV file and uses the actual number of players who made the cut to determine which payout scenario to apply (e.g., if 67 players make the cut, use the 67-player scenario from the CSV).

### Payout System Summary

**Two Payout Systems:**

1. **Unified CSV System** (Standard Events, Continental Championship, Majors):
   - Uses `greenbook/data/53_85_payout_structure.csv`
   - Covers all scenarios from 53 to 85 paid players
   - Handles variable cut lines and field sizes
   - Each scenario sums to exactly 100%

2. **Static Table System** (Standard Invitationals & Signature Events):
   - Fixed 72-player field with no cut line
   - Uses the Signature Events payout table below
   - All 72 players are guaranteed to be paid
   - Single payout scenario that sums to exactly 100%

### Signature Events
- **Cut line**: None (all players paid)
- **Field size**: Fixed at 72 players
- **Payout system**: Single static percentage table
- **Framework**: One payout table for 72 players, summing to 100%

#### Signature Event Payout Table (72 Players)

| Position | Percentage | Position | Percentage | Position | Percentage |
|----------|------------|----------|------------|----------|------------|
| 1        | 18.000%    | 25       | 0.866%     | 49       | 0.247%     |
| 2        | 10.800%    | 26       | 0.809%     | 50       | 0.235%     |
| 3        | 7.000%     | 27       | 0.754%     | 51       | 0.224%     |
| 4        | 5.000%     | 28       | 0.701%     | 52       | 0.214%     |
| 5        | 4.000%     | 29       | 0.650%     | 53       | 0.204%     |
| 6        | 3.600%     | 30       | 0.602%     | 54       | 0.194%     |
| 7        | 3.500%     | 31       | 0.564%     | 55       | 0.185%     |
| 8        | 3.300%     | 32       | 0.530%     | 56       | 0.176%     |
| 9        | 3.100%     | 33       | 0.502%     | 57       | 0.168%     |
| 10       | 2.900%     | 34       | 0.478%     | 58       | 0.161%     |
| 11       | 2.600%     | 35       | 0.458%     | 59       | 0.156%     |
| 12       | 2.400%     | 36       | 0.440%     | 60       | 0.151%     |
| 13       | 2.300%     | 37       | 0.422%     | 61       | 0.147%     |
| 14       | 2.200%     | 38       | 0.405%     | 62       | 0.144%     |
| 15       | 2.100%     | 39       | 0.388%     | 63       | 0.140%     |
| 16       | 2.000%     | 40       | 0.372%     | 64       | 0.135%     |
| 17       | 1.600%     | 41       | 0.356%     | 65       | 0.134%     |
| 18       | 1.469%     | 42       | 0.341%     | 66       | 0.133%     |
| 19       | 1.400%     | 43       | 0.326%     | 67       | 0.132%     |
| 20       | 1.250%     | 44       | 0.312%     | 68       | 0.131%     |
| 21       | 1.150%     | 45       | 0.298%     | 69       | 0.129%     |
| 22       | 1.120%     | 46       | 0.284%     | 70       | 0.127%     |
| 23       | 0.989%     | 47       | 0.271%     | 71       | 0.126%     |
| 24       | 0.926%     | 48       | 0.259%     | 72       | 0.115%     |

**Total**: 100.000%

### The Continental Championship
- **Cut line**: Top 65 and ties
- **Payout system**: Same as standard events
- **Framework**: Uses the unified 53-85 CSV file for all scenarios

### The Four Majors
Each major has unique field sizes and cut lines, but uses a unified payout system:

#### Majors Payout System (Variable Paid Players)
- **Cut lines vary by major**: Top 50-70 and ties (depending on the specific major)
- **Field sizes vary**: 90-156 players (depending on the specific major)
- **Payout system**: Variable based on number of players making cut
- **Framework**: General-purpose lookup table covering 53-85 paid players

#### Majors Payout Percentages (53-85 Players)

**Complete payout table covering ALL scenarios from 53 to 85 paid players (33 total scenarios). Each scenario sums to exactly 100%.**

The complete majors payout data is stored in `greenbook/data/53_85_payout_structure.csv` with the following format:
- Column 1: Number of players (53-85)
- Column 2: Position (1-85) 
- Column 3: Percentage (as decimal)

This CSV file contains all 33 scenarios (53-85 players) with precise percentage distributions for each position. Each scenario sums to exactly 100% of the purse.

**Implementation**: The system should load this CSV file as a lookup table, using the number of players who made the cut to determine which payout scenario to apply.

**Note**: All four majors use this unified payout system, with each major's specific cut line determining how many players qualify for payouts.



### Implementation Strategy

1. **Static Tables** (Standard Invitationals & Signature Events):
   - Pre-calculate all payout percentages
   - Store as lookup tables
   - No runtime calculations needed

2. **Dynamic Systems** (Standard Events, Continental, Majors):
   - Use the CSV lookup table system
   - Calculate payouts based on actual number of paid players
   - Handle ties and variable field sizes



## Core Requirements

### 1. Event Identity
- Event name and type (8 specific event types)
- Field size ranges (with multiples of 3 requirement)
- Cut line rules (varies by event type, some have no cut)
- FedExCup points structure (mirroring PGA TOUR distribution tables)
- Purse ranges (random values within specified ranges)
- Event frequency and scheduling (majors spaced 4-5 events apart)

**FedExCup Points Structure (Based on PGA TOUR):**
- **Standard Events**: 500 points to winner (PGA TOUR Events distribution table)
- **Standard Invitationals**: 600 points to winner (custom structure)
- **Signature Events**: 700 points to winner (Signature Events distribution table)
- **The Continental Championship**: 750 points to winner (Majors distribution table)
- **All Majors**: 750 points to winner (Majors distribution table)

### 2. Course Selection
- Manual course selection for events
- Some events always use specific courses
- Course assignment logic

### 3. Weather Integration
- Round-specific weather
- Forecasted and locked in before each round
- Realistic modifiers for rain, wind, humidity
- Weather affects player performance

### 4. Tournament Structure
- Multi-round events (typically 4 rounds)
- Cut line after 2 rounds
- Field size varies by event type
- Purse distribution

### 5. Player Qualification
- Different qualification methods per event type
- Based on simulated history (future)
- World ranking, tour points, exemptions

## Design Questions to Resolve

1. **Event Identity Structure**
   - Should we use enums, classes, or simple dictionaries?
   - How much complexity do we need for event definitions?

2. **Course Assignment**
   - How do we specify which courses go with which events?
   - Should courses be assigned per event or per round?

3. **Weather System**
   - How do we generate realistic weather forecasts?
   - How do weather conditions affect player performance?

4. **Tournament Execution**
   - How do we actually run a tournament?
   - How do players progress through rounds?

5. **Data Storage**
   - How do we store tournament results?
   - How do we track player performance over time?

## Next Steps
1. Define basic event types (enum/class)
2. Create simple event identity structure
3. Build course assignment logic
4. Design weather system
5. Implement tournament execution

## Notes
- Keep it simple initially
- Build incrementally
- Focus on core functionality first
- Add complexity only when needed 