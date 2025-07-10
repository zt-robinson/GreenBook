# 🏌️ Golf Simulation Roadmap

This document outlines the full vision, structure, and phased development plan for the golf simulator. It reflects system goals, design decisions, and implementation guidance.

---

## 🔭 Project Vision

A realistic, skill-driven, tournament-based golf simulator with:

- 35-event main season + playoffs
- Player skill + mental modeling
- Hole-by-hole round simulation
- Realistic randomness via real-world entropy
- Career stat tracking, standings, and a results archive
- Future integration of betting and alternate tours

---

## 🗓️ Season Structure

| Component              | Description                         |
|------------------------|-------------------------------------|
| Regular Season         | ~35 events                          |
| Event Types            | Standard, Invitational, Signature, Continental, 4 Majors |
| Playoffs              | 3 playoff events + 1 Tour Championship |
| Majors                | Sovereign, AGA, American Open, Royal Open |
| Schedule              | Fixed template (see `season_schedule.md`) |

---

## 🎯 Event Framework

### Event Types Overview

| Type              | Field Size     | Cut Line       | Points (Win) | Purse Range     |
|-------------------|----------------|----------------|--------------|-----------------|
| Standard          | 144–165        | Top 65 + ties  | 500          | $7.9M–$9.5M      |
| Invitational      | 72             | None           | 600          | $10M–$12M        |
| Signature         | 72             | None           | 700          | $18M–$20M        |
| Continental       | 123–144        | Top 65 + ties  | 750          | $30M             |
| Majors (4 total)  | 90–156         | Varies         | 750          | $22M–$25M        |

### Points and Payouts

- **Points** follow a tiered system by event type (see `docs/season_points.md`)
- **Payouts** use:
  - Variable table (53–85 player payouts) for cut events
  - Static 72-player table for no-cut events
  - Ties are resolved via aggregate percent averaging

---

## 🧠 Player Model

### Skills

- `driving_power`, `driving_accuracy`, `approach_accuracy`, `short_game`, `putting`

### Mental Attributes

- `composure`, `confidence`, `focus`, `risk_tolerance`, `mental_fatigue`, `consistency`, `resilience`

### Career Progression

- Aging handled at season end
- Randomly assigned `peak_age`, `peak_duration`, and performance boost (`peak_adder`)
- Skill growth with age/experience, decline after peak
- Retirement at force age (45–50) or early retirement based on stats

### Confidence

- Influenced by recent form (last 3–5 events)
- Carried over between events (hot/cold streaks)
- Impacts performance modestly

### Status & Pressure

- Exempt / Conditional / Non-Exempt affect field entry
- Conditional/Non-Exempt players receive pressure penalties (mental performance impacted)

---

## ⛳ Course & Hole Model

### Course-Level

- `green_speed`, `turf_firmness`, `length`, `hazard_density`, `strategic_penal_index`

### Hole-Level

- `par`, `yardage`, `stroke index`, `terrain_difficulty`, `hazards`

Player performance is affected by:
- Course fit (long vs short, strategic vs penal)
- Hole type weightings (par 3, 4, 5)
- Skill matchup against difficulty

---

## 🌦️ Weather Engine

- Weather generated per round
- Factors: wind, rain, temperature, humidity, cloudiness
- Each factor affects specific skills (e.g., wind → accuracy; rain → putting/approach)

---

## 🎲 Real-World Entropy System

Randomness is seeded by:
- Current timestamp hash
- Live weather values (temp, wind from real locations)
- Last 4 digits of Bitcoin or stock index
- Mixed and hashed into entropy float

Seed resets per round or per hole, ensuring:
- No deterministic results
- Better players win more often, but anything can happen

---

## 🏁 Simulation Engine

### Round Simulation

- Hole-by-hole testing
- Skills weighted per hole type
- Weather + course + player mental state applied
- `performance_delta = Y - X` (skill vs difficulty)
- Delta fed into probability curve to return score outcome
- Probabilities are custom (not hard-coded PGA stats)

### Scoring

- Birdie/eagle/bogey chance based on `performance_delta`
- Risk tolerance influences variance
- Confidence boosts/reduces outcomes probabilistically

---

## 💾 Data Storage

### Tournament Results

- Store round-by-round scores for each player
- Final leaderboard with position and earnings
- Winner(s), ties resolved

### Career Archive

- Track all historical tournaments
- Season stats can be generated from results (scoring avg, top 10s, earnings, etc.)

---

## 🛠️ Development Phases

| Phase | Objective                             | Key Components                                   |
|-------|---------------------------------------|--------------------------------------------------|
| 1     | Data Pipeline                         | Player + Course creation, DB schema              |
| 2     | Tournament Engine                     | Round simulation, hole testing, weather modifiers|
| 3     | Entropy System                        | Real-world entropy engine                        |
| 4     | Result Storage                        | Write event/round results to DB                  |
| 5     | Standings + Tour Card Logic           | Points, status calculation, exemptions           |
| 6     | Year-End Processing                   | Retirement, peak age progression, feeder tour logic |
| 7     | Visualization                         | Leaderboards, player stats, dashboards           |
| 8     | Betting Layer (future)                | Odds gen, user wagers, payout simulation         |

---

## 🔄 Future Features

- Development/Q School tours
- Sponsorship/earnings simulation
- Match play or team formats
- Interactive betting/gameplay modes
- Broadcast-style visualization (live leaderboard streaming)

---

## 🧭 Guiding Principles

- Prioritize realism but embrace randomness
- Build modular systems with future layering in mind
- Track everything — simulate only what matters
- Build it to be watched, analyzed, and enjoyed

