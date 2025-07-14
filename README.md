# GreenBook

**GreenBook** is a sophisticated Flask-based golf simulation platform that creates an entire professional golf tour ecosystem – complete with realistic tournament simulation, dynamic player progression, and comprehensive betting systems using **play money only**. Think of it as a combination of PGA Tour simulation, fantasy sports, and sports betting analytics, all wrapped in an elegant Augusta National-inspired interface.

## 🎯 Project Vision

GreenBook aims to be the most realistic and comprehensive golf simulation platform available, featuring:

- **35-Event Professional Season**: Complete tour schedule with majors, signature events, and standard tournaments
- **Realistic Player Modeling**: 200+ virtual golfers with detailed skill attributes, mental game mechanics, and career progression
- **Dynamic Tour Card System**: Promotion/relegation system with developmental tour integration
- **Live Tournament Simulation**: Hole-by-hole, round-by-round simulation with real-world entropy
- **Comprehensive Betting Platform**: Multiple betting markets with dynamic odds and play money wagering
- **Historical Data Archive**: Complete career tracking and tournament history

The project draws inspiration from the prestige and classic style of Augusta National, featuring a sophisticated green-and-gold theme and country club aesthetic. Our goal is to mirror the drama, structure, and excitement of a real PGA Tour season while providing a **safe sandbox for sports betting** enthusiasts to test their instincts without financial risk.

## 🏆 Current Implementation Status

### ✅ Completed Features

#### **Core Data Infrastructure**
- **Player Database**: 500+ unique virtual golfers with realistic skill ratings (driving power, accuracy, approach, short game, putting) and mental attributes (composure, confidence, focus, risk tolerance)
- **Course Library**: 30+ championship courses with detailed attributes (yardage, par, difficulty, weather patterns, elevation)
- **Tournament Structure**: Complete 35-event season schedule with proper event types and field sizes
- **Database Architecture**: SQLite-based data storage with comprehensive schema for players, courses, tournaments, and results

#### **Web Application Interface**
- **Modern Augusta-Inspired UI**: Classy dark-green, gold, and off-white color scheme with classic serif typography
- **Responsive Design**: Accessible on various devices with flexible layouts and balanced tables
- **Multi-Page Experience**:
  - **Home Page**: Landing page with season overview and quick stats
  - **Players Page**: Searchable table with expandable player profiles and career stats
  - **Courses Page**: Course listings with professional scorecards and characteristics
  - **Schedule Page**: Chronological tournament list with event details and results

#### **Tour Card & Priority System**
- **Tour Card Status**: Fully exempt, conditionally exempt, and non-exempt player categories
- **Priority Lists**: Dynamic calculation system for tournament field invitations
- **Exemption Rules**: Automatic exemptions based on victories and tour status

### 🔄 In Development

#### **Tournament Simulation Engine**
- **Hole-by-Hole Simulation**: Realistic shot-by-shot simulation with skill weighting by hole type
- **Weather Integration**: Real-world weather data affecting course conditions and player performance
- **Mental Game Mechanics**: Confidence fluctuation, pressure situations, and mental fatigue
- **Real-World Entropy**: Seeded randomness using live data sources for authentic unpredictability

#### **Betting System Foundation**
- **Payout Structures**: Comprehensive payout systems for different event types
- **Points Distribution**: FedExCup-style points system with proper distribution tables
- **Tie Handling**: Proper resolution of tied positions and earnings

### 📋 Planned Features (Next Phase)

#### **Live Tournament Experience**
- **Real-Time Simulation**: Watch tournaments unfold hole-by-hole with live leaderboards
- **Dynamic Field Generation**: Automated tournament field selection based on qualification rules
- **Round-by-Round Progression**: Authentic 72-hole competitions with proper cut lines
- **Live Betting Interface**: Real-time odds updates and wagering during tournaments

#### **Enhanced Player System**
- **Career Progression**: Player aging, peak performance periods, and retirement mechanics
- **Development Tour**: Full simulation of secondary tour with promotion/relegation
- **Advanced Statistics**: Comprehensive career tracking and performance analytics
- **Player Profiles**: Detailed individual player pages with historical data

#### **Season & Championship Systems**
- **Tour Championship**: Season-ending playoff system with staggered starting scores
- **Standings Tracking**: Real-time FedExCup points race with qualification scenarios
- **Historical Archive**: Complete tournament and career history preservation

## 🎲 Betting & Gaming Features

GreenBook's betting system is designed to be comprehensive and realistic while maintaining the play-money safety net:

### **Betting Markets**
- **Outright Winners**: Tournament champion predictions
- **Position Betting**: Top-5, top-10, top-20 finishes
- **Cut Line Betting**: Make/miss the cut predictions
- **Head-to-Head**: Player matchup comparisons
- **Round Leaders**: Individual round performance
- **Prop Bets**: Bogey-free rounds, birdie counts, etc.

### **Dynamic Odds System**
- **Live Updates**: Odds change based on tournament progress
- **Skill-Based Calculation**: Player attributes, current form, course difficulty
- **Weather Factors**: Environmental conditions affecting performance
- **Mental Game Impact**: Confidence and pressure situations

### **Play Money Economy**
- **Virtual Bankroll**: Safe wagering with no real financial risk
- **Bet Tracking**: Complete history of wagers and outcomes
- **Performance Analytics**: Track betting success over time
- **Community Features**: Leaderboards and friendly competitions

## 🏌️ Tournament System

### **Event Types & Structure**

| Event Type | Field Size | Cut Line | Winner Points | Purse Range | Prestige |
|------------|------------|----------|---------------|-------------|----------|
| Standard Events | 144-165 | Top 65 + ties | 500 | $7.9M-$9.5M | Variable |
| Standard Invitationals | 72 | None | 600 | $10M-$12M | Variable |
| Signature Events | 72 | None | 700 | $18M-$20M | Variable |
| Continental Championship | 123-144 | Top 65 + ties | 750 | $30M | 0.95 |
| Major Championships | 90-156 | Variable | 750 | $22M-$25M | 1.0 |

### **Season Schedule**
- **35 Regular Season Events**: Mix of standard, invitational, signature, and major tournaments
- **4 Major Championships**: Sovereign Tournament, AGA Championship, American Open, Royal Open
- **Playoff System**: 3 playoff events + Tour Championship
- **Real-Time Progression**: Events scheduled with authentic timing and progression

## 👤 Player Modeling System

### **Physical Skills (0-100 scale)**
- `driving_power`: Distance off the tee
- `driving_accuracy`: Fairway finding ability  
- `approach_accuracy`: Iron play and approach shots
- `short_game`: Chipping, pitching, bunker play
- `putting`: Green reading and putting skill

### **Mental Attributes (0-100 scale)**
- `composure`: Pressure handling, final round performance
- `confidence`: Current self-belief, fluctuates during tournaments
- `focus`: Concentration maintenance, mental fatigue resistance
- `risk_tolerance`: Aggressive vs conservative decision making
- `mental_fatigue`: Tournament endurance, performance decline
- `consistency`: Low variance in performance, steady play
- `resilience`: Bounce-back ability from poor holes/rounds

### **Career Progression**
- **Aging System**: Players age 1 year at season end
- **Peak Performance**: Random peak age (29-33) with 2-3 year duration
- **Performance Factor**: Ramps up/down around peak age
- **Retirement**: Force retirement (45-50) or early retirement based on performance

## 🛠️ Technical Architecture

### **Backend Stack**
- **Flask Framework**: Python-based web application
- **SQLite Database**: Lightweight, file-based data storage
- **Jinja2 Templates**: Server-side rendering for dynamic content
- **Utility Scripts**: Data generation and management tools

### **Data Management**
- **Player Generation**: Scripts for creating realistic player profiles
- **Course Creation**: Tools for building course databases
- **Tournament Results**: Comprehensive result storage and retrieval
- **Historical Archive**: Complete tournament and career history

### **Development Phases**

| Phase | Objective | Status |
|-------|-----------|--------|
| 1 | Data Pipeline | ✅ Complete |
| 2 | Tournament Engine | 🔄 In Progress |
| 3 | Entropy System | 🔄 In Progress |
| 4 | Result Storage | 🔄 In Progress |
| 5 | Standings + Tour Card Logic | 📋 Planned |
| 6 | Year-End Processing | 📋 Planned |
| 7 | Visualization | 📋 Planned |
| 8 | Betting Layer | 📋 Planned |

## 🚀 Getting Started

Ready to explore the GreenBook universe? Here's how to get started:

### **Prerequisites**
- Python 3.7+
- Git
- Web browser

### **Installation Steps**

1. **Clone the repository**
   ```bash
   git clone https://github.com/zt-robinson/GreenBook.git
   cd GreenBook
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database (optional)**
   ```bash
   python scripts/create_player.py    # Regenerate player database
   python scripts/create_course.py   # Regenerate course database
   ```

5. **Run the application**
   ```bash
   flask run
   ```

6. **Open in browser**
   Navigate to [http://localhost:5000](http://localhost:5000)

### **Current Limitations**
- Tournament simulation is currently stubbed/placeholder
- Betting interface not yet implemented
- Real-time features in development
- Some advanced features planned for future releases

## 🤝 Contributing

GreenBook is an ambitious project and we welcome contributions! Here's how you can help:

### **Ways to Contribute**
- **Bug Reports**: Open issues for any problems you encounter
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests for enhancements
- **Documentation**: Help improve documentation and guides
- **Testing**: Test features and provide feedback

### **Development Guidelines**
- Maintain the project's focus on realism and accessibility
- Follow the established code style and architecture
- Test thoroughly before submitting changes
- Update documentation for new features

### **Getting Involved**
- Watch the repository for updates
- Join discussions in issues and pull requests
- Share ideas for new features or improvements
- Help build the community around the project

*We're building something special here – a comprehensive golf simulation that combines the thrill of sports betting with the depth of professional golf analytics. Join us in creating the ultimate virtual golf experience!* ⛳🏆

## 📊 Data Sources

[![Weather Data Provided by Visual Crossing](data/visual_crossing_logo_small.png)](https://www.visualcrossing.com/)

GreenBook incorporates historical weather data for 610 US cities throughout 2024, collected via the Visual Crossing Weather API. This data includes monthly averages for temperature, wind speed, precipitation, humidity, and cloud cover, which are used to simulate realistic course conditions and weather effects on tournament play.

For detailed information about the weather data structure and processing, see the [Weather Data Dictionary](data/WEATHER_DATA_DICTIONARY.md).

## 📄 License

GreenBook is an open-source project, released under the **MIT License**. This means you're free to use, modify, and distribute the code, as long as you include the original license notice. (See the `LICENSE` file for the full text of the license.) Enjoy!

---

*GreenBook: Where golf simulation meets sports betting analytics in a safe, sophisticated environment.* 🏌️‍♂️💰
