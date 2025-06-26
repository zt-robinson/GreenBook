# Golf Universe: Flask Golf Simulation & Betting Platform

## Project Vision & Goals

Golf Universe is a highly detailed, Flask-based golf simulation and sports betting web application. The goal is to create a living, evolving golf world that mirrors the drama, structure, and excitement of the PGA Tour—complete with:
- Realistic player careers, tour card mechanics, and dynamic field qualification
- A full season schedule of tournaments, including majors, invitationals, and opens
- Real-time, granular simulation of tournament play (hole-by-hole, group-by-group)
- A comprehensive betting platform with a wide variety of markets and live odds
- Persistent player histories, career arcs, and a developmental tour system
- A beautiful, modern, and user-friendly web interface

## Current Features (as of June 2025)

### Data & Simulation
- **Player Database:** 200+ generated players, each with realistic skill ratings, country, age, and career stats
- **Tour Card System:** Each player has a `TourCardStatus` (Full, Exempt, Conditional, None, Lifetime) and an `Exempt_Thru` year, determining eligibility for events
- **Course Database:** 30+ championship courses, each with detailed characteristics (yardage, par, weather, green speed, elevation, etc.)
- **Tournament Database:** Robust structure for tournaments, fields, results, odds, schedule, and payout structure
- **Developmental Tour:** Players who lose their card move to a separate dev league, with a chance to re-qualify each year

### Web Application
- **Home Page:** Modern, welcoming landing page with quick stats and navigation
- **Players Page:** Table of all players, expandable for detailed stats and career info
- **Courses Page:** Table of all courses, expandable for professional scorecards and real-world characteristics
- **Schedule Page:** Table of all upcoming tournaments, with field size, purse, start date, and round times (in EST)
- **Navigation:** Clean, modern navigation bar for all major sections

### Tournament & Schedule System
- **Tournament Types:** Regular Tour Events, Opens, Invitationals, Majors, and a future Tour Championship
- **Field Sizes:** Vary by event type (e.g., 156 for regular, 90 for invitationals, 90-120 for majors)
- **Qualification:** Full/Exempt/Lifetime status, then Conditional, then recent top performers, then former major winners, then players ranked 151-200
- **Event Timing:** Each event is scheduled two days apart, with the first event set for July 4, 2025
- **Round Structure:** 4 rounds per event, with staggered group starts and cut after round 2
- **Payouts & Points:** Each event has a detailed payout and points structure

## Technical Structure

- **Flask** for backend and routing
- **SQLite** for persistent storage (players, courses, tournaments, dev league)
- **Jinja2** for templating and dynamic HTML
- **Modern CSS** for a clean, responsive UI
- **Seeding Scripts** for generating and resetting all data

## Simulation & Game Mechanics

### Tour Card & Career System
- Players start with a tour card; status is re-evaluated each season
- Top 125: Full card; 126-150: Conditional; 151-200: Lose card, move to dev league
- Exemptions for wins, majors, and career achievements (tracked by `Exempt_Thru`)
- Dev league simulates a season, top 30 rejoin the main tour, new players generated each year
- Lifetime status for 20+ wins and 15+ seasons

### Tournament Simulation
- 4 rounds, 72-hole stroke play
- Rounds 1-2: 3-man groups, random order; Rounds 3-4: 2-man groups, sorted by score
- Cut after round 2 (top 65 and ties)
- Each group plays a hole every 3 minutes, with rounds and breaks scheduled for real-time betting
- Tournament schedule is persistent and visible on the web

### Betting System (Planned)
- Outright winner, top 5/10/20, make the cut, low round, group winner, round leader, 9-hole leader, bogey-free round, H2H matchups, over/under, birdie props, and more
- Odds update after every hole, and multiple times between rounds
- Odds calculation factors: player skill, current score, course/weather, pressure, momentum, history
- Pre-tournament odds update weekly; live odds update in real time during events
- Full betting UI for placing, tracking, and settling bets

## Roadmap & Planned Features

### Short-Term
- Tournament field generation logic (based on qualification rules above)
- Tournament simulation engine (group-by-group, hole-by-hole)
- Live odds calculation and updating
- Betting UI and bet settlement logic
- Player career stats and history page
- Dev league auto-simulation and player promotion

### Long-Term
- Tour Championship with special rules and points system
- Player injury, fatigue, and form tracking
- Sponsorships and pressure mechanics
- User accounts and persistent bet tracking
- Admin UI for adding/editing tournaments, courses, and players
- API for external integrations (e.g., Discord bots, mobile apps)
- More advanced betting markets and analytics

## How Everything Fits Together

- **Players** are the core of the sim, with evolving careers, stats, and eligibility
- **Courses** provide unique challenges and realism for each event
- **Tournaments** are scheduled, simulated, and bet on in real time
- **Betting** is the main user interaction, with a wide variety of markets and live odds
- **Dev League** ensures turnover and new talent, keeping the world dynamic
- **UI** is designed for clarity, beauty, and ease of use, with all data calculated in the backend for fast rendering

## How to Run

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Generate the player and course databases
5. Run the tournament and schedule seeding scripts
6. Start the Flask app: `python app.py`
7. Open your browser to [http://localhost:5000](http://localhost:5000)

## Contributing & Feedback

This project is a work in progress and open to ideas! If you have suggestions, want to contribute, or spot a bug, please open an issue or pull request.

---

**Golf Universe** is designed to be the most realistic, dynamic, and fun golf simulation and betting platform on the web. Every detail is crafted to mirror the real world of professional golf, while giving users the tools to engage, bet, and follow the action in real time.

## Project Structure
```
greenbook/
  app.py
  create_course.py
  create_player.py
  generate_players.sh
  requirements.txt
  static/
    flags/   # SVG country flags
  templates/
    ...
```

## External Resources Used
- **Country Flags:** [lipis/flag-icons](https://github.com/lipis/flag-icons) (MIT License)
- **Faker:** For generating realistic player names and attributes
- **Flask:** Web framework

---

For questions or contributions, please open an issue or pull request! 