# Tournament Simulation Notes

## Hole-by-Hole Skill Testing System

### Skill Weighting by Hole Type

#### Par 3 Holes
- **Driving Power**: 10% (less important on short holes)
- **Driving Accuracy**: 20% (still important for tee shot)
- **Approach Accuracy**: 60% (primary skill for par 3s)
- **Short Game**: 5% (minimal scrambling needed)
- **Putting**: 5% (standard putting)

#### Par 4 Holes
- **Driving Power**: 30% (important for distance)
- **Driving Accuracy**: 30% (critical for fairway position)
- **Approach Accuracy**: 30% (key for approach shots)
- **Short Game**: 5% (scrambling when needed)
- **Putting**: 5% (standard putting)

#### Par 5 Holes
- **Driving Power**: 40% (most important for distance)
- **Driving Accuracy**: 25% (still critical)
- **Approach Accuracy**: 25% (approach to green)
- **Short Game**: 5% (scrambling when needed)
- **Putting**: 5% (standard putting)

### Additional Considerations
- **Hole Difficulty**: Higher difficulty = more impact from all skills
- **Yardage**: Longer holes = more driving power importance
- **Course Characteristics**: Strategic/penal index affects skill importance
- **Weather**: Wind/rain affects different skills differently

### Implementation Notes
- This system will be used during tournament simulation
- Each hole will calculate a "skill test score" based on player skills and hole characteristics
- Luck/randomness will be added to create variance
- Course factors (rough length, green speed, etc.) will modify skill effectiveness

## Mental Game System

### Mental Attributes (0-100 scale)
- **Composure**: Pressure handling, final round performance, big tournament performance
- **Confidence**: Current self-belief, fluctuates during tournaments and seasons
- **Focus**: Concentration maintenance, mental fatigue resistance
- **Risk Tolerance**: Aggressive vs conservative decision making
- **Mental Fatigue**: Tournament endurance, performance decline over multiple rounds
- **Consistency**: Low variance in performance, steady play
- **Resilience**: Bounce-back ability from poor holes/rounds

### Mental Game Mechanics

#### Confidence Fluctuation
- **Starting Confidence**: Based on recent form and experience
- **Hole Performance**: Good holes boost confidence, poor holes reduce it
- **Tournament Progress**: Confidence changes throughout rounds
- **Season Performance**: Long-term confidence based on season results

#### Pressure Situations
- **Final Holes**: Increased pressure on holes 16-18
- **Final Rounds**: Sunday pressure affects all players
- **Big Tournaments**: Majors and high-profile events increase pressure
- **Leaderboard Position**: Leading vs chasing affects pressure

#### Risk Tolerance Implementation
- **Driveable Par 4s**: High risk tolerance = higher birdie chance, higher blow-up risk
- **Long Par 5s**: Risk tolerance affects go-for-green decisions
- **Par 3s**: Risk tolerance affects pin-seeking vs safe play
- **Scoring Variance**: High risk tolerance = higher variance in scores

#### Mental Fatigue
- **Rookie vs Veteran**: Rookies more affected by tournament length
- **Round Progression**: Mental fatigue increases over 4 rounds
- **Recovery**: Some players recover better between rounds
- **Focus Decline**: Mental fatigue reduces focus and composure

#### Skill Modification
- **Mental Modifiers**: Mental attributes modify physical skill effectiveness
- **Pressure Situations**: High pressure = mental attributes more important
- **Consistency**: High consistency = lower variance in performance
- **Resilience**: High resilience = better recovery from poor performance

### Implementation Notes
- Mental attributes act as modifiers on physical skills
- Confidence fluctuates hole-by-hole and round-by-round
- Risk tolerance affects scoring variance and strategy
- Mental fatigue increases over tournament duration
- Pressure situations amplify mental attribute importance

## Player Aging, Retirement, and Peaking System (Planned)

### Aging
- At the end of each season, increment every player's `age` by 1.

### Retirement
- **Force Retirement:**
  - On player creation, assign `force_retirement` as a random integer between 45–50.
  - At end of season, if a player's new age equals `force_retirement`, retire them: mark as retired, remove from active list, archive stats.
- **Early Retirement:**
  - At end of season, calculate `early_retirement_chance` for each player based on:
    - Age (closer to `force_retirement` = higher chance)
    - Recent season performance (worse = higher chance)
    - Career stats (few wins = higher chance)
    - Tour standings (lower = higher chance)
  - Generate a random number; if it's less than `early_retirement_chance`, retire the player early.

### Peaking
- On player creation, assign:
  - `performance_factor` (default 1)
  - `peak_adder` (random, e.g., 0.4–0.7)
  - `peak_age` (random 29–33)
  - `peak_duration` (random 2–3)
  - `peak_start` (`peak_age` minus random 1–2)
  - `peak_stop` (`peak_age + (peak_duration-1)` plus random 1–2)
- At any time, a player's `performance_factor` is:
  - 1 before `peak_start` and after `peak_stop`
  - Ramps up between `peak_start` and `peak_age`
  - Max at `peak_age` through `peak_age + (peak_duration-1)`
  - Ramps down between `peak_age + (peak_duration-1)` and `peak_stop`

- See detailed logic and example in project chat history for implementation details. 