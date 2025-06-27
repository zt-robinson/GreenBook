# GreenBook

GreenBook is a Flask-based golf simulation and analytics platform, inspired by the prestige and style of Augusta National. It features a modern, tactile UI, robust tournament and player systems, and a stat-focused, country club scorecard aesthetic.

## Features
- **Augusta-inspired UI**: Dark green, gold, and off-white palette, classic serif headlines, and stately, flat containers.
- **Tournament System**: Dynamic schedule, two-phase field display (provisional/finalized), strict tee time logic, and a professional "billboard" for each event.
- **Player Careers**: Realistic simulation logic, dynamic player stats, and a detailed "Tour Card" system.
- **Responsive Design**: Multi-column layouts, national flags, and compact, visually balanced tables.
- **SQLite Databases**: For players, courses, and tournaments, with seed scripts and utilities in `greenbook/scripts/`.
- **Local Virtual Environment**: All dependencies managed in `greenbook/venv` (not tracked by git).

## Directory Structure
```
greenbook/
├── app.py                # Main Flask app
├── static/               # CSS, icons, and static assets
├── templates/            # Jinja2 HTML templates
├── scripts/              # Utility and seed scripts
├── data/                 # SQLite database files
├── venv/                 # Local Python virtual environment (not in git)
└── README.md             # This file
```

## Setup & Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/zt-robinson/GreenBook.git
   cd GreenBook/greenbook
   ```
2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv --upgrade-deps
   source venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r ../requirements.txt
   ```
4. **Set up the database**
   - Use scripts in `greenbook/scripts/` to seed or update the database as needed.

5. **Run the app**
   ```bash
   flask run
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000)

## Contributing
- Please open issues or pull requests for suggestions, bug fixes, or new features.
- All code should follow the existing style and design guidelines.

## License
MIT License 