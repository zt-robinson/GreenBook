# 🏌️ Master Golf Simulation Specification

## 📋 Table of Contents
1. [Project Vision & Overview](#project-vision--overview)
2. [Season Structure & Scheduling](#season-structure--scheduling)
3. [Event Types & Tournament System](#event-types--tournament-system)
4. [Player Model & Attributes](#player-model--attributes)
5. [Tour Card Status & Priority System](#tour-card-status--priority-system)
6. [Simulation Engine](#simulation-engine)
7. [Payout & Points System](#payout--points-system)
8. [Data Management](#data-management)
9. [Development Phases](#development-phases)
10. [Conflicts & Clarifications Needed](#conflicts--clarifications-needed)

---

## 🎯 Project Vision & Overview

A realistic, skill-driven, tournament-based golf simulator featuring:
- 35-event main season + playoffs
- Player skill + mental modeling with realistic progression
- Hole-by-hole round simulation with real-world entropy
- Career stat tracking, standings, and results archive
- Future integration of betting and alternate tours

### Core Principles
- Prioritize realism but embrace randomness
- Build modular systems with future layering in mind
- Track everything — simulate only what matters
- Build it to be watched, analyzed, and enjoyed

---

## 📅 Season Structure & Scheduling

### Season Composition
- **Regular Season**: 35 events
- **Event Types**: Standard, Invitational, Signature, Continental, 4 Majors
- **Playoffs**: 3 playoff events + 1 Tour Championship
- **Schedule**: Fixed template that repeats annually

### Season Schedule Template

| Event # | Event Type | Event Name | Notes |
|---------|------------|------------|-------|
| 01 | Signature Event #1 | | |
| 02 | Standard Event #1 | | |
| 03 | Standard Event #2 | | |
| 04 | Standard Invitational #1 | | |
| 05 | Standard Event #3 | | |
| 06 | Standard Invitational #2 | | |
| 07 | Standard Event #4 | | |
| 08 | Standard Event #5 | | |
| 09 | Signature Event #2 | | |
| 10 | Continental Championship | | |
| 11 | Standard Event #6 | | |
| 12 | Standard Invitational #3 | | |
| 13 | Signature Event #3 | | |
| 14 | Standard Event #7 | | |
| 15 | Sovereign Tournament | First Major | |
| 16 | Standard Event #8 | | |
| 17 | Standard Event #9 | | |
| 18 | Standard Invitational #4 | | |
| 19 | Signature Event #4 | | |
| 20 | AGA Championship | Second Major | |
| 21 | Standard Event #10 | | |
| 22 | Signature Event #5 | | |
| 23 | Standard Invitational #5 | | |
| 24 | Standard Event #11 | | |
| 25 | Standard Event #12 | | |
| 26 | American Open | Third Major | |
| 27 | Signature Event #6 | | |
| 28 | Standard Event #13 | | |
| 29 | Standard Event #14 | | |
| 30 | Standard Invitational #6 | | |
| 31 | Royal Open | Fourth Major | |
| 32 | Standard Event #15 | | |
| 33 | Standard Invitational #7 | | |
| 34 | Standard Event #16 | | |
| 35 | Signature Event #7 | | |

### Prehistory System
For the first 20 seasons, a "prehistory" system creates initial player rankings:
1. Generate 600 players (ages 19-22)
2. Run 10 "Gauntlet Season" tournaments (600-player fields, 72 holes each)
3. Cull to top 100 players + add 50 new players
4. Run 10 seasons of 35 events each to establish historical rankings
5. After each season: cull bottom 50, age remaining players, add 50 new players

---

## 🏆 Event Types & Tournament System

### Event Type Specifications

| Type | Field Size | Cut Line | Winner Points | Purse Range | Prestige |
|------|------------|----------|---------------|-------------|----------|
| Standard Events | 144-165 | Top 65 + ties | 500 | $7.9M-$9.5M | Variable |
| Standard Invitationals | 72 | None | 600 | $10M-$12M | Variable |
| Signature Events | 72 | None | 700 | $18M-$20M | Variable |
| Continental Championship | 123-144 | Top 65 + ties | 750 | $30M | 0.95 |
| Sovereign Tournament | 90-114 | Top 53 + ties | 750 | $22M-$25M | 1.0 |
| AGA Championship | 156 | Top 70 + ties | 750 | $22M-$25M | 1.0 |
| American Open | 156 | Top 67 + ties | 750 | $22M-$25M | 1.0 |
| Royal Open | 156 | Top 70 + ties | 750 | $22M-$25M | 1.0 |

### Tournament Structure
- **Rounds**: Typically 4 rounds (72 holes)
- **Cut Line**: After 2 rounds (varies by event type)
- **Field Size**: Varies by event type (72-165 players)
- **Weather**: Generated per round with realistic modifiers

### Course & Weather Integration
- **Course Selection**: Manual assignment per event
- **Weather Factors**: Wind, rain, temperature, humidity, cloudiness
- **Weather Impact**: Affects specific skills (wind → accuracy, rain → putting)

---

## 👤 Player Model & Attributes

### Physical Skills (0-100 scale)
- `driving_power`: Distance off the tee
- `driving_accuracy`: Fairway finding ability
- `approach_accuracy`: Iron play and approach shots
- `short_game`: Chipping, pitching, bunker play
- `putting`: Green reading and putting skill

### Mental Attributes (0-100 scale)
- `composure`: Pressure handling, final round performance
- `confidence`: Current self-belief, fluctuates during tournaments
- `focus`: Concentration maintenance, mental fatigue resistance
- `risk_tolerance`: Aggressive vs conservative decision making
- `mental_fatigue`: Tournament endurance, performance decline
- `consistency`: Low variance in performance, steady play
- `resilience`: Bounce-back ability from poor holes/rounds

### Career Progression System
- **Aging**: Players age 1 year at season end
- **Peaking**: Random `peak_age` (29-33), `peak_duration` (2-3 years)
- **Performance Factor**: Ramps up/down around peak age
- **Retirement**: Force retirement (45-50) or early retirement based on performance

### Confidence System
- Influenced by recent form (last 3-5 events)
- Carried over between events (hot/cold streaks)
- Fluctuates hole-by-hole and round-by-round
- Impacts performance modestly

---

## 🎫 Tour Card Status & Priority System

### Tour Card Status Types

#### Fully Exempt
- Top 100 from final prior season points list
- Top 20 players from Development Tour
- Top 5 players from Q School Tournament
- Winners of events (automatic exemptions based on event category)

#### Conditionally Exempt
- Players 101-125 on final prior season points list
- Do not have guaranteed entry into most events
- Eligible to fill remaining spots after priority categories
- Can earn points and money, potentially regain full status

#### Non-Exempt
- Have no standing on priority list
- Can only play via tournament-specific exemptions or Monday qualifying
- Do not accrue points
- Can earn money but doesn't count toward standings unless status regained

### Priority Lists (8 event types)
Priority lists are dynamically calculated after every event and determine field invitations:

1. **Standard Events**: 17 priority categories
2. **Standard Invitationals**: 7 priority categories  
3. **Signature Events**: 12 priority categories
4. **Continental Championship**: 12 priority categories
5. **Sovereign Tournament**: 12 priority categories
6. **AGA Championship**: 12 priority categories
7. **American Open**: 10 priority categories
8. **Royal Open**: 10 priority categories

### Priority List Update System
- **Frequency**: After every single event completion
- **Scope**: All 8 priority lists are recalculated after each event
- **Logic**: Dynamic calculation based on latest results and updated criteria
- **Field Updates**: Active fields for all subsequent events are updated

### Update Flow Example
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

### Implementation Logic
```python
# After each event completes:
for event_type in all_8_event_types:
    priority_list = calculate_priority_list(event_type, current_season_results)
    update_future_event_fields(event_type, priority_list)
```

### Key Points
- **Exemption Status**: Handled separately (end-of-season processing)
- **Points/Rankings**: Updated after each event
- **Dynamic Qualification**: Winners immediately qualify for future events
- **Cascading Updates**: Each event result affects multiple future events

### Monday Qualifying System
- **Format**: Single-round, 18-hole simulation
- **Participants**: Eligible non-exempt or conditional players
- **Qualification**: Top 4 finishers earn guaranteed spot in upcoming event
- **Timing**: Held on off-days between events

### Automatic Exemptions Based on Victories
- **Standard/Invitational**: +2 seasons
- **Signature Event**: +3 seasons
- **Tour Championship**: +3 seasons
- **Continental Championship**: +4 seasons
- **Major Championship**: +5 seasons
- **Extension Cap**: Maximum +7 seasons per season
- **Forward Limit**: Cannot extend beyond 7 seasons from current season

---

## 🎲 Simulation Engine

### Hole-by-Hole Simulation Flow

1. **Retrieve Static Data**
   - Course attributes (par, yardage, difficulty, terrain, etc.)
   - Player attributes (skills and mental stats)

2. **Apply Dynamic Modifiers**
   - Weather factors (wind, rain, temperature, humidity, cloudiness)
   - Tournament context (prestige factor, pressure)

3. **Calculate Final Values**
   - Hole difficulty (X) = base difficulty × environmental modifiers
   - Player performance (Y) = base skills × environmental modifiers

4. **Determine Outcome**
   - Performance delta = Y - X
   - Use delta to determine probabilistic score outcome

### Skill Weighting by Hole Type

#### Par 3 Holes
- Driving Power: 10%
- Driving Accuracy: 20%
- Approach Accuracy: 60%
- Short Game: 5%
- Putting: 5%

#### Par 4 Holes
- Driving Power: 30%
- Driving Accuracy: 30%
- Approach Accuracy: 30%
- Short Game: 5%
- Putting: 5%

#### Par 5 Holes
- Driving Power: 40%
- Driving Accuracy: 25%
- Approach Accuracy: 25%
- Short Game: 5%
- Putting: 5%

### Real-World Entropy System
Randomness seeded by:
- Current timestamp hash
- Live weather values from real locations
- Last 4 digits of Bitcoin or stock index
- Mixed and hashed into entropy float
- Resets per round or per hole

### Mental Game Mechanics
- **Confidence Fluctuation**: Based on recent form and hole performance
- **Pressure Situations**: Final holes, final rounds, big tournaments
- **Risk Tolerance**: Affects scoring variance and strategy decisions
- **Mental Fatigue**: Increases over tournament duration
- **Skill Modification**: Mental attributes modify physical skill effectiveness

---

## 💰 Payout & Points System

### FedExCup Points Distribution

| Position | Standard Event | Standard Invitational | Signature Event | Major/Continental |
|----------|---------------|----------------------|----------------|-------------------|
| 1 | 500 | 600 | 700 | 750 |
| 2 | 300 | 300 | 400 | 500 |
| 3 | 190 | 270 | 350 | 300 |
| 4 | 135 | 230 | 325 | 325 |
| 5 | 110 | 205 | 300 | 300 |
| ... | ... | ... | ... | ... |

### Payout Systems

#### Two Payout Systems:

1. **Unified CSV System** (Standard Events, Continental Championship, Majors):
   - Uses `greenbook/data/53_85_payout_structure.csv`
   - Covers scenarios from 53 to 85 paid players
   - Handles variable cut lines and field sizes
   - Each scenario sums to exactly 100%

2. **Static Table System** (Standard Invitationals & Signature Events):
   - Fixed 72-player field with no cut line
   - Uses Signature Events payout table
   - All 72 players guaranteed to be paid
   - Single payout scenario summing to exactly 100%

#### Implementation Logic
```python
# For Signature Events & Standard Invitationals:
if event_type in ['signature_event', 'standard_invitational']:
    use_static_72_player_table()
    
# For all other events (Standard Events, Continental, Majors):
else:
    players_making_cut = determine_cut_size(event_results)
    payout_percentages = lookup_csv_payouts(players_making_cut)
```

#### Example
- **Signature Event**: Always 72 players, use static table
- **Standard Event**: Cut line "Top 65 and ties" → if 67 players make cut, use 67-player scenario from CSV
- **Major**: Cut line varies by major → if 70 players make cut, use 70-player scenario from CSV

### Tie Handling
- Tied players receive average payout of their tied positions
- Example: Two players tied for 1st each get 16.5% (average of 1st and 2nd)

---

## 💾 Data Management

### Tournament Results Storage
- Round-by-round scores for each player
- Final leaderboard with position and earnings
- Winner(s) with ties resolved

### Career Archive
- Track all historical tournaments
- Season stats generated from results (scoring avg, top 10s, earnings, etc.)
- Player progression and retirement tracking

### Database Schema Requirements
- Player attributes and career progression
- Tournament results and standings
- Priority lists and tour card status
- Course and weather data
- Payout structures and points distribution

---

## 🛠️ Development Phases

| Phase | Objective | Key Components |
|-------|-----------|----------------|
| 1 | Data Pipeline | Player + Course creation, DB schema |
| 2 | Tournament Engine | Round simulation, hole testing, weather modifiers |
| 3 | Entropy System | Real-world entropy engine |
| 4 | Result Storage | Write event/round results to DB |
| 5 | Standings + Tour Card Logic | Points, status calculation, exemptions |
| 6 | Year-End Processing | Retirement, peak age progression, feeder tour logic |
| 7 | Visualization | Leaderboards, player stats, dashboards |
| 8 | Betting Layer (future) | Odds gen, user wagers, payout simulation |

---

## ✅ Resolved Conflicts & Clarifications

All conflicts have been resolved and the master document now serves as the authoritative source for the golf simulation project. Key decisions include:

### **Priority List System**: Dynamic calculation after every event
### **Payout Systems**: Static table for Signature/Invitationals, CSV lookup for others
### **Field Sizes**: Randomized multiples of 3 within specified ranges
### **Points Distribution**: Authoritative 85-position table from tournament_system_plan.md
### **Player Generation**: Ages 19-22 with detailed peaking system
### **Weather System**: Very detailed, per-round implementation
### **Mental Game**: Complex system from TOURNAMENT_SIMULATION_NOTES.md
### **Development Timeline**: Adjusted 8-phase roadmap with clear priorities

---

## 📝 Next Steps

1. **✅ Resolve Conflicts**: All conflicts have been resolved
2. **Implement Core Systems**: Start with Phase 1-4 (essential features)
3. **Build Testing Framework**: Create comprehensive test suite
4. **Database Design**: Design complete database structure as needed
5. **Documentation**: Maintain this master specification as the single source of truth

---

*This document consolidates all concepts from the individual specification files and serves as the master reference for the golf simulation project.* 