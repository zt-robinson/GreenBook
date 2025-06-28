#!/usr/bin/env python3
"""
Simple Golf Course Generator
Creates a single golf course with a variety of realistic attributes.
"""

import random
import sqlite3
import json
import os
import argparse
import sys

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_players.db')

# List of coastal cities for 'Links' eligibility
COASTAL_CITIES = set([
    'Edinburgh', 'Dublin', 'Vancouver', 'Sydney', 'Melbourne', 'Osaka', 'Tokyo',
    # Add more as needed
])

# Standard list of large metro cities (top 2-3 per state, US)
LARGE_METRO_CITIES = set([
    # Example: Top 2-3 per state (abbreviated for brevity)
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
    'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle', 'Denver', 'Washington',
    'Boston', 'El Paso', 'Nashville', 'Detroit', 'Oklahoma City', 'Portland', 'Las Vegas', 'Memphis', 'Louisville', 'Baltimore',
    # Add more as needed for other countries
])

# List of real cities and states/countries for random selection
# Comprehensive city pools for random location selection
US_CITIES_BY_STATE = {
    # Top 5 States by Population (5 cities each)
    "California": ["Los Angeles", "San Diego", "San Jose", "San Francisco", "Fresno"],
    "Texas": ["Houston", "San Antonio", "Dallas", "Austin", "Fort Worth"],
    "Florida": ["Jacksonville", "Miami", "Tampa", "Orlando", "St. Petersburg"],
    "New York": ["New York", "Buffalo", "Rochester", "Yonkers", "Syracuse"],
    "Pennsylvania": ["Philadelphia", "Pittsburgh", "Allentown", "Erie", "Reading"],
    
    # Next 20 States by Population (3 cities each)
    "Illinois": ["Chicago", "Aurora", "Naperville"],
    "Ohio": ["Columbus", "Cleveland", "Cincinnati"],
    "Georgia": ["Atlanta", "Augusta", "Columbus"],
    "North Carolina": ["Charlotte", "Raleigh", "Greensboro"],
    "Michigan": ["Detroit", "Grand Rapids", "Warren"],
    "New Jersey": ["Newark", "Jersey City", "Paterson"],
    "Virginia": ["Virginia Beach", "Richmond", "Norfolk"],
    "Washington": ["Seattle", "Spokane", "Tacoma"],
    "Arizona": ["Phoenix", "Tucson", "Mesa"],
    "Tennessee": ["Nashville", "Memphis", "Knoxville"],
    "Indiana": ["Indianapolis", "Fort Wayne", "Evansville"],
    "Massachusetts": ["Boston", "Worcester", "Springfield"],
    "Missouri": ["Kansas City", "St. Louis", "Springfield"],
    "Maryland": ["Baltimore", "Frederick", "Rockville"],
    "Colorado": ["Denver", "Colorado Springs", "Aurora"],
    "Wisconsin": ["Milwaukee", "Madison", "Green Bay"],
    "Minnesota": ["Minneapolis", "St. Paul", "Rochester"],
    "South Carolina": ["Columbia", "Charleston", "North Charleston"],
    "Alabama": ["Birmingham", "Montgomery", "Huntsville"],
    "Louisiana": ["New Orleans", "Baton Rouge", "Shreveport"],
    "Kentucky": ["Louisville", "Lexington", "Bowling Green"],
    "Oregon": ["Portland", "Salem", "Eugene"],
    
    # Next 20 States by Population (2 cities each)
    "Oklahoma": ["Oklahoma City", "Tulsa"],
    "Connecticut": ["Bridgeport", "New Haven"],
    "Utah": ["Salt Lake City", "West Valley City"],
    "Iowa": ["Des Moines", "Cedar Rapids"],
    "Nevada": ["Las Vegas", "Reno"],
    "Arkansas": ["Little Rock", "Fort Smith"],
    "Mississippi": ["Jackson", "Gulfport"],
    "Kansas": ["Wichita", "Overland Park"],
    "New Mexico": ["Albuquerque", "Las Cruces"],
    "Nebraska": ["Omaha", "Lincoln"],
    "West Virginia": ["Charleston", "Huntington"],
    "Idaho": ["Boise", "Meridian"],
    "Hawaii": ["Honolulu", "Hilo"],
    "New Hampshire": ["Manchester", "Nashua"],
    "Maine": ["Portland", "Lewiston"],
    "Montana": ["Billings", "Missoula"],
    "Rhode Island": ["Providence", "Warwick"],
    "Delaware": ["Wilmington", "Dover"],
    "South Dakota": ["Sioux Falls", "Rapid City"],
    "North Dakota": ["Fargo", "Bismarck"],
    "Alaska": ["Anchorage", "Fairbanks"],
    "Vermont": ["Burlington", "South Burlington"],
    "Wyoming": ["Cheyenne", "Casper"]
}

# International city pools
CANADA_CITIES = ["Toronto", "Montreal", "Vancouver", "Calgary", "Edmonton", "Ottawa", "Winnipeg", "Quebec City"]
AUSTRALIA_CITIES = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Gold Coast", "Newcastle", "Canberra", "Sunshine Coast", "Central Coast", "Wollongong", "Hobart", "Geelong", "Townsville", "Cairns", "Toowoomba", "Darwin", "Ballarat", "Bendigo", "Albury-Wodonga"]
JAPAN_CITIES = ["Tokyo", "Osaka", "Nagoya", "Sapporo", "Fukuoka", "Kobe", "Kyoto", "Kawasaki", "Yokohama", "Saitama", "Hiroshima", "Sendai", "Chiba", "Kitakyushu", "Sakai", "Niigata", "Hamamatsu", "Kumamoto", "Sagamihara", "Shizuoka", "Okayama", "Kagoshima", "Funabashi", "Hachioji", "Matsuyama", "Matsudo", "Nishinomiya", "Kawaguchi", "Kanazawa", "Ichikawa", "Utsunomiya", "Oita", "Kurashiki", "Gifu", "Himeji", "Matsumoto", "Fujisawa", "Koriyama", "Takamatsu", "Toyota", "Toyama", "Wakayama", "Hirakata", "Fukuyama", "Asahikawa", "Machida", "Nara", "Takatsuki", "Iwaki", "Nagano", "Tottori", "Suita"]
SPAIN_CITIES = ["Madrid", "Barcelona", "Valencia", "Seville", "Zaragoza", "Málaga", "Murcia", "Palma", "Las Palmas", "Bilbao", "Alicante", "Córdoba", "Valladolid", "Vigo", "Gijón", "L'Hospitalet", "A Coruña", "Vitoria-Gasteiz", "Granada", "Elche", "Tarrasa", "Badalona", "Cartagena", "Jerez de la Frontera", "Sabadell", "Alcalá de Henares", "Móstoles", "Almería", "Fuenlabrada", "San Sebastián", "Leganés", "Santander", "Castellón", "Burgos", "Albacete", "Alcorcón", "Getafe", "Salamanca", "Logroño", "Huelva", "Marbella", "Lleida", "Tarragona", "León", "Cádiz", "Jaén", "Girona", "Lugo", "Cáceres", "Toledo", "Ceuta", "Melilla"]
FRANCE_CITIES = ["Paris", "Marseille", "Lyon", "Toulouse", "Nice", "Nantes", "Strasbourg", "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims", "Le Havre", "Saint-Étienne", "Toulon", "Angers", "Grenoble", "Dijon", "Nîmes", "Saint-Denis", "Villeurbanne", "Le Mans", "Aix-en-Provence", "Brest", "Nantes", "Limoges", "Clermont-Ferrand", "Tours", "Amiens", "Perpignan", "Metz", "Besançon", "Boulogne-Billancourt", "Orléans", "Mulhouse", "Rouen", "Saint-Denis", "Caen", "Argenteuil", "Saint-Paul", "Montreuil", "Nancy", "Roubaix", "Tourcoing", "Nanterre", "Avignon", "Vitry-sur-Seine", "Créteil", "Dunkerque", "Poitiers", "Asnières-sur-Seine", "Courbevoie", "Versailles"]

# --- Top-level city sets for UK/Ireland ---
ENGLAND_CITIES = set([
    "London", "Birmingham", "Manchester", "Liverpool", "Leeds", "Sheffield", "Bristol", "Newcastle", "Sunderland", "Wolverhampton", "Nottingham", "Derby", "Southampton", "Portsmouth", "Leicester", "Coventry", "Bradford", "Kingston upon Hull", "Stoke-on-Trent", "Middlesbrough", "Reading", "Luton", "Preston", "Huddersfield", "Bolton", "Stockport", "Blackburn", "Walsall", "West Bromwich", "Oldham", "Slough", "Gloucester", "Cambridge", "Watford", "Rotherham", "York", "Blackpool", "Oxford", "Rochdale", "Mansfield", "Basingstoke", "Northampton", "Swindon", "Milton Keynes", "Ipswich", "Telford", "Woking", "Warrington", "Gateshead"
])
SCOTLAND_CITIES = set([
    "Glasgow", "Edinburgh", "Aberdeen", "Dundee", "Paisley", "East Kilbride", "Livingston", "Hamilton", "Cumbernauld", "Dunfermline", "Kirkcaldy", "Perth", "Inverness", "Ayr", "Kilmarnock", "Coatbridge", "Greenock", "Glenrothes", "Stirling", "Airdrie", "Falkirk", "Irvine", "Motherwell", "Rutherglen", "Wishaw", "Cambuslang", "Dumbarton", "Elgin", "Arbroath", "Bathgate", "Musselburgh", "Peterhead", "Clydebank", "Alloa", "Renfrew", "Bellshill", "St Andrews", "Bearsden", "Clarkston", "Forfar", "Montrose", "Kilwinning", "Largs", "Stonehaven", "Broxburn", "Buckhaven", "Bonnyrigg", "Barrhead", "Penicuik"
])
IRELAND_CITIES = set([
    "Dublin", "Cork", "Limerick", "Galway", "Waterford", "Drogheda", "Swords", "Dundalk", "Bray", "Navan", "Ennis", "Tralee", "Carlow", "Newbridge", "Portlaoise", "Balbriggan", "Naas", "Athlone", "Mullingar", "Letterkenny", "Celbridge", "Wexford", "Clonmel", "Killarney", "Sligo", "Greystones", "Leixlip", "Malahide", "Kilkenny", "Cobh", "Castlebar", "Midleton", "Mallow", "Ashbourne", "Laytown-Bettystown-Mornington", "Arklow", "Maynooth", "Ballina", "Tullamore", "Enniscorthy", "Shannon", "Wicklow", "Tramore", "Skerries", "Longford", "Dungarvan", "Gorey", "Edenderry", "Donabate", "Bandon"
])

def get_random_location(country=None, state=None):
    """Get a random city, state, country combination from the full pools, or restrict to a specific country/state if provided."""
    countries = {
        "USA": 0.4,
        "Canada": 0.15,
        "England": 0.1,
        "Scotland": 0.1,
        "Ireland": 0.1,
        "Australia": 0.05,
        "Japan": 0.05,
        "Spain": 0.025,
        "France": 0.025
    }
    if state:
        # US only
        if not country or country.strip().title() not in ["USA", "Usa", "United States", "United States Of America", "Us"]:
            country = "USA"
        # Normalize state name (case-insensitive match)
        state_lookup = {s.lower(): s for s in US_CITIES_BY_STATE.keys()}
        state_key = state.strip().lower()
        if state_key not in state_lookup:
            print(f"Error: State '{state}' not found in US city pool.")
            exit(1)
        state = state_lookup[state_key]
        city = random.choice(US_CITIES_BY_STATE[state])
        return city, state, "USA"
    if country:
        country = country.strip().title()
        # Accept common variants
        country_map = {
            'Uk': 'England', 'United Kingdom': 'England', 'Britain': 'England',
            'England': 'England', 'Scotland': 'Scotland', 'Wales': 'Wales',
            'Northern Ireland': 'Ireland', 'Ireland': 'Ireland',
            'Gb': 'England', 'Great Britain': 'England',
            'Usa': 'USA', 'United States': 'USA', 'United States Of America': 'USA',
            'Us': 'USA',
            'Aus': 'Australia', 'Oz': 'Australia',
            'Espana': 'Spain',
        }
        country = country_map.get(country, country)
        if country == "USA":
            state = random.choice(list(US_CITIES_BY_STATE.keys()))
            city = random.choice(US_CITIES_BY_STATE[state])
            return city, state, country
        elif country == "Canada":
            city = random.choice(CANADA_CITIES)
            province_map = {
                "Toronto": "Ontario", "Ottawa": "Ontario", "Hamilton": "Ontario", "London": "Ontario", "Windsor": "Ontario",
                "Montreal": "Quebec", "Quebec City": "Quebec", "Laval": "Quebec", "Gatineau": "Quebec", "Longueuil": "Quebec",
                "Vancouver": "British Columbia", "Surrey": "British Columbia", "Burnaby": "British Columbia", "Richmond": "British Columbia",
                "Calgary": "Alberta", "Edmonton": "Alberta", "Red Deer": "Alberta", "Lethbridge": "Alberta",
                "Winnipeg": "Manitoba", "Brandon": "Manitoba",
                "Saskatoon": "Saskatchewan", "Regina": "Saskatchewan",
                "Halifax": "Nova Scotia", "Sydney": "Nova Scotia",
                "St. John's": "Newfoundland and Labrador",
                "Charlottetown": "Prince Edward Island",
                "Fredericton": "New Brunswick", "Saint John": "New Brunswick",
                "Whitehorse": "Yukon", "Yellowknife": "Northwest Territories", "Iqaluit": "Nunavut"
            }
            state = province_map.get(city, "Ontario")
            return city, state, country
        elif country == "England":
            city = random.choice(list(ENGLAND_CITIES))
            return city, "", country
        elif country == "Scotland":
            city = random.choice(list(SCOTLAND_CITIES))
            return city, "", country
        elif country == "Ireland":
            city = random.choice(list(IRELAND_CITIES))
            return city, "", country
        elif country == "Australia":
            city = random.choice(AUSTRALIA_CITIES)
            state_map = {
                "Sydney": "New South Wales", "Newcastle": "New South Wales", "Wollongong": "New South Wales", "Central Coast": "New South Wales",
                "Melbourne": "Victoria", "Geelong": "Victoria", "Ballarat": "Victoria", "Bendigo": "Victoria",
                "Brisbane": "Queensland", "Gold Coast": "Queensland", "Sunshine Coast": "Queensland", "Townsville": "Queensland", "Cairns": "Queensland", "Toowoomba": "Queensland",
                "Perth": "Western Australia",
                "Adelaide": "South Australia",
                "Canberra": "Australian Capital Territory",
                "Hobart": "Tasmania",
                "Darwin": "Northern Territory", "Albury-Wodonga": "Victoria"
            }
            state = state_map.get(city, "New South Wales")
            return city, state, country
        elif country == "Japan":
            city = random.choice(JAPAN_CITIES)
            return city, "", country
        elif country == "Spain":
            city = random.choice(SPAIN_CITIES)
            return city, "", country
        elif country == "France":
            city = random.choice(FRANCE_CITIES)
            return city, "", country
        else:
            # fallback to original logic
            return get_random_location()
    # No country specified: use weighted random
    country = random.choices(list(countries.keys()), weights=list(countries.values()))[0]
    return get_random_location(country)

# Keep the original REAL_LOCATIONS as fallback
REAL_LOCATIONS = [
    ("Dallas", "Texas", "USA"),
    ("Los Angeles", "California", "USA"),
    ("Chicago", "Illinois", "USA"),
    ("Miami", "Florida", "USA"),
    ("Boston", "Massachusetts", "USA"),
    ("London", "England", "UK"),
    ("Edinburgh", "Scotland", "UK"),
    ("Dublin", "Ireland", "Ireland"),
    ("Toronto", "Ontario", "Canada"),
    ("Vancouver", "British Columbia", "Canada"),
    ("Sydney", "New South Wales", "Australia"),
    ("Melbourne", "Victoria", "Australia"),
    ("Tokyo", "Tokyo", "Japan"),
    ("Osaka", "Osaka", "Japan"),
    ("Paris", "Île-de-France", "France"),
    ("Madrid", "Madrid", "Spain"),
]

# --- Database Functions ---

def create_course_tables():
    """
    Creates the 'courses' and 'course_characteristics' tables in the database
    if they do not already exist. Connects to the existing golf_players.db.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Courses Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            city TEXT,
            state_country TEXT,
            yardage INTEGER,
            par INTEGER,
            prestige INTEGER,
            est_year INTEGER,
            location TEXT
        )
    ''')

    # Create Course Characteristics Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course_characteristics (
            course_id INTEGER PRIMARY KEY,
            avg_temperature REAL,
            humidity_level REAL,
            wind_factor REAL,
            rain_probability REAL,
            design_strategy REAL,
            course_length REAL,
            narrowness_factor REAL,
            hazard_density REAL,
            green_speed REAL,
            turf_firmness REAL,
            rough_length REAL,
            prestige_level REAL,
            course_age REAL,
            crowd_factor REAL,
            elevation_factor REAL,
            terrain_difficulty REAL,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    ''')

    # Create Holes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            hole_number INTEGER,
            par INTEGER,
            difficulty_modifier REAL,
            handicap INTEGER,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    ''')

    # Create Tournaments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            course_id INTEGER,
            date TEXT,
            format TEXT,
            prize_money INTEGER,
            prestige INTEGER,
            rounds INTEGER,
            global_weather TEXT,
            status TEXT DEFAULT 'not_started',
            FOREIGN KEY(course_id) REFERENCES courses(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_course_to_db(name, city, state, prestige, characteristics):
    """Saves a course and its characteristics to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Insert the main course record
        cursor.execute('INSERT OR IGNORE INTO courses (name, city, state_country, prestige) VALUES (?, ?, ?, ?)', (name, city, state, prestige))
        cursor.execute('SELECT id FROM courses WHERE name = ?', (name,))
        course_id = cursor.fetchone()[0]
        
        # Prepare and insert the characteristics
        char_columns = ', '.join(characteristics.keys())
        char_placeholders = ', '.join('?' for _ in characteristics)
        char_values = [course_id] + list(characteristics.values())
        
        cursor.execute(f'''
            INSERT OR REPLACE INTO course_characteristics (course_id, {char_columns})
            VALUES (?, {char_placeholders})
        ''', char_values)

        conn.commit()
        print(f"✅ Successfully saved course '{name}' with ID: {course_id}")
        return course_id
    finally:
        conn.close()

def insert_single_tournament(course_id):
    name = "Prestige National Invitational"
    date = "2025-07-01"
    format = "stroke play"
    prize_money = 2000000
    prestige = 90
    rounds = 4
    global_weather = json.dumps({
        "wind": 12,  # mph
        "rain": "light",
        "temperature": 78,  # F
        "humidity": 55
    })
    status = 'not_started'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO tournaments (name, course_id, date, format, prize_money, prestige, rounds, global_weather, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, course_id, date, format, prize_money, prestige, rounds, global_weather, status))
    conn.commit()
    print(f"✅ Tournament '{name}' created for course ID {course_id}")
    conn.close()

def insert_course_to_db(course, characteristics, holes):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Insert course
    c.execute('INSERT INTO courses (name, city, state_country, yardage, par, prestige, est_year, location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (course['name'], course['city'], course['state_country'], course['yardage'], course['par'], course['prestige'], course['est_year'], course['location']))
    course_id = c.lastrowid
    # Insert characteristics
    c.execute('''INSERT INTO course_characteristics (
        course_id, avg_temperature, humidity_level, wind_factor, rain_probability, design_strategy, course_length, narrowness_factor, hazard_density, green_speed, turf_firmness, rough_length, prestige_level, course_age, crowd_factor, elevation_factor, terrain_difficulty
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (course_id,
         characteristics['temp_factor'], characteristics['humidity_factor'], characteristics['wind_factor'], characteristics['rain_factor'],
         characteristics['design_strategy'], characteristics['course_length'], characteristics['narrowness_factor'], characteristics['hazard_density'],
         characteristics['green_speed'], characteristics['turf_firmness'], characteristics['rough_length'], characteristics['prestige_level'],
         characteristics['course_age'], characteristics['crowd_factor'], characteristics['elevation_factor'], characteristics['terrain_difficulty'])
    )
    # Insert holes
    for h in holes:
        c.execute('INSERT INTO holes (course_id, hole_number, par, difficulty_modifier, handicap) VALUES (?, ?, ?, ?, ?)',
                  (course_id, h['hole'], h['par'], h.get('difficulty_modifier', 1.0), h.get('handicap', 1)))
    conn.commit()
    conn.close()
    print(f"Inserted course '{course['name']}' (ID: {course_id}) into the database.")

# --- Generation Functions ---

def generate_course_name(country, city=None, state=None):
    # Normalize country input
    country_map = {
        'UK': 'England', 'United Kingdom': 'England', 'Britain': 'England',
        'England': 'England', 'Scotland': 'Scotland', 'Wales': 'Wales',
        'Northern Ireland': 'Ireland', 'Ireland': 'Ireland',
        'GB': 'England', 'Great Britain': 'England',
    }
    orig_country = country
    country = country_map.get(country, country)
    # Naming components
    adjectives = [
        "Old", "New", "Great", "High", "Golden", "White", "Hidden", "Black", "Spotted", "Mount",
        "Astorian", "Elysian", "American", "Southern", "Northern", "Eastern", "Western"
    ]
    plants = [
        "Sycamore", "Pine", "Maple", "Spruce", "Oak", "Willow", "Aspen", "Ash", "Birch", "Cherry", "Cedar", "Walnut", "Cypress", "Woodlands", "Ivy", "Amberwood", "Rose", "Apple", "Heather", "Larkspur", "Bramble", "Pines", "Thistle", "Elder", "Briar"
    ]
    geo = [
        "Cape", "Beach", "Ridge", "Cliffs", "Cove", "Canyon", "Marsh", "Hill", "Valley", "Meadow", "Glen", "Stream", "River", "Creek", "Lake", "Lagoon", "Delta", "Spring", "Highlands", "Dale", "Downs", "Dunes", "Hollow", "Point", "Rock", "Stone", "Grove", "Garden", "Heath", "Wood", "Forest", "Haven", "Fields", "Park", "Vale"
    ]
    animals = [
        "Quail", "Pheasant", "Grouse", "Duck", "Goose", "Swan", "Otter", "Stag", "Elk", "Deer", "Owl", "Kingfisher", "Crow", "Raven", "Lark", "Finch", "Sparrow", "Blackbird", "Warbler", "Cardinal", "Trout", "Salmon"
    ]
    professions = [
        "Hunter", "Fisherman", "Miller", "Cooper", "Earl", "Duke", "Baron", "Baroness"
    ]
    names = [
        "Montgomery", "Cabot", "Carnegie", "Morgan", "Mellon", "Astor", "Lauder", "Washington", "Sherman", "Baker", "Lowell", "Carter", "Nelson", "Lancaster", "Roosevelt", "Coolidge", "Adams", "Forbes", "Hardwick", "Holmes", "Appleton", "Bates", "Buckingham", "Coates", "Emerson", "Gardner", "Lawrence", "Peabody", "Thayer", "Warren", "Winthrop", "Hamilton", "Berkshire", "Bradley", "Stewart"
    ]
    us_structures = [
        "Country Club", "Golf Club", "National", "Resort", "Golf Course", "Links", "Park"
    ]
    uk_structures = [
        "Golf Club", "Links", "Hall", "Manor", "Abbey", "Park"
    ]
    jp_structures = [
        "Golf Club", "Country Club", "Resort", "Golf Course"
    ]
    au_structures = [
        "Golf Club", "Country Club", "Resort"
    ]
    ca_structures = [
        "Golf Club", "Country Club", "Resort"
    ]
    neutral_structures = [
        "Golf Club", "Country Club", "Resort", "Golf Course", "Links"
    ]
    forbidden_us_prefixes = ["Royal", "St.", "Abbey", "Manor", "Chateau", "Palace", "Castle", "Rectory", "Priory", "Friar", "Baron", "Duke"]
    # Country logic
    if country in ["England", "Scotland", "Ireland"]:
        structures = uk_structures
        allow_royal = True
    elif country == "Japan":
        # For Japan, always use [City] Golf Club, [City] Country Club, or [City] Club
        if city:
            return f"{city} {random.choice(['Golf Club', 'Country Club', 'Club'])}"
        else:
            return f"{random.choice(['Golf Club', 'Country Club', 'Club'])}"
    elif country == "Australia":
        structures = au_structures
        allow_royal = False
    elif country == "Canada":
        structures = ca_structures
        allow_royal = False
    elif country == "USA":
        structures = us_structures
        allow_royal = False
    else:
        structures = neutral_structures
        allow_royal = False
    # Patterns
    patterns = []
    # Spain: Spanish naming patterns
    if country == 'Spain':
        if city:
            roll = random.random()
            if roll < 0.15:
                return f"Real Club de Golf {city}"
            elif roll < 0.40:
                return f"Club de Golf {city}"
            elif roll < 0.50:
                return f"{city} Golf Club"
            elif roll < 0.60:
                return f"{city} Golf Resort"
            elif roll < 0.65:
                return f"{city} Golf & Country Club"
            elif roll < 0.80:
                return f"Club de Golf {city}"
            elif roll < 0.90:
                return f"{city} Golf Club"
            else:
                return f"Real Club de Golf {city}"
        else:
            return f"Real Club de Golf {random.choice(names)}"
    # France: French naming patterns
    if country == 'France':
        if city and random.random() < 0.5:
            return f"Golf de {city}"
        elif city and random.random() < 0.8:
            return f"Parc de Golf {city}"
        elif city:
            return f"{city} Golf"
        else:
            return f"Golf de {random.choice(names)}"
    # UK/Ireland: Traditional and estate-style naming logic with top 50 cities/towns
    if country in ["England", "Scotland", "Ireland"]:
        estate_suffixes = ["Park", "Downs", "Hall", "Manor", "Forest", "Heath", "Estate", "Fields", "Grove", "Court", "House", "Gardens"]
        course_variants = ["Old Course", "New Course", "Championship", "East Course", "West Course"]
        is_coastal = city in COASTAL_CITIES if city else False
        roll = random.random()
        name = None
        city_set = ENGLAND_CITIES if country == "England" else SCOTLAND_CITIES if country == "Scotland" else IRELAND_CITIES
        # 60%: [City] Golf Club (only if city is in top 50)
        if city and city in city_set and roll < 0.60:
            name = f"{city} Golf Club"
        # 15%: [City] Golf Links (coastal only, only if city is in top 50)
        elif city and city in city_set and is_coastal and roll < 0.75:
            name = f"{city} Golf Links"
        # 10%: Royal [City] Golf Club (only if city is in top 50)
        elif city and city in city_set and roll < 0.85:
            name = f"Royal {city} Golf Club"
        # 15%: [Estate-Style Name] [Estate Suffix] (strict: never any other suffix)
        else:
            estate_adjectives = adjectives + plants + animals
            estate_name = f"{random.choice(estate_adjectives)} {random.choice(estate_adjectives)} {random.choice(estate_suffixes)}"
            name = estate_name
        # 25% chance to append a course variant
        if random.random() < 0.25:
            name += f" ({random.choice(course_variants)})"
        # Forcibly remove unwanted suffixes
        for bad_suffix in ["Golf Course", "Resort"]:
            if name.endswith(bad_suffix):
                name = name[: -len(bad_suffix)].rstrip()
        print(f"[DEBUG] Country: {orig_country} (normalized: {country}), City: {city}, Generated Name: {name}")
        return name
    else:
        # Only allow 'Links' and 'Beach' if city is coastal
        def structure_filter(s):
            if s == 'Links' and (not city or city not in COASTAL_CITIES):
                return False
            if s == 'Beach' and (not city or city not in COASTAL_CITIES):
                return False
            # Only allow 'Country Club' for US and Australia
            if s == 'Country Club' and country not in ['USA', 'Australia']:
                return False
            # Never allow 'St.' as a suffix
            if s == 'St.':
                return False
            # Never allow 'Resort' for UK/Ireland or large metro cities
            if s == 'Resort' and (country in ['England', 'Scotland', 'Ireland'] or (city and city in LARGE_METRO_CITIES)):
                return False
            return True
        filtered_structures = [s for s in structures if structure_filter(s)]
        # If all structures are filtered out, fallback to all except 'Links', 'Beach', 'Country Club', 'St.', 'Resort'
        if not filtered_structures:
            filtered_structures = [s for s in structures if s not in ['Links', 'Beach', 'Country Club', 'St.', 'Resort']]
        patterns = [
            lambda: f"{random.choice(adjectives)} {random.choice(plants)} {random.choice(geo)} {random.choice(filtered_structures)}",
            lambda: f"{random.choice(plants)} {random.choice(geo)} {random.choice(filtered_structures)}",
            lambda: f"{random.choice(animals)} {random.choice(geo)} {random.choice(filtered_structures)}",
            lambda: f"{random.choice(names)} {random.choice(filtered_structures)}",
            lambda: f"{random.choice(geo)} {random.choice(filtered_structures)}",
            lambda: f"{random.choice(plants)} {random.choice(filtered_structures)}",
            lambda: f"{random.choice(geo)} {random.choice(plants)} {random.choice(filtered_structures)}",
            # 10% chance for St. [Name] [Structure] (never as suffix)
            lambda: f"St. {random.choice(names)} {random.choice(filtered_structures)}" if random.random() < 0.1 else ""
        ]
    # US: filter forbidden prefixes
    def filter_us(name):
        for forbidden in forbidden_us_prefixes:
            if name.startswith(forbidden):
                return False
        return True
    # Generate name
    tries = 0
    forbidden_combinations = [
        "Park Resort", "Resort Park", "Park Park", "Resort Resort", "National Resort", "Resort National"
    ]
    # 7% chance for [City] Golf Club, 93% for creative patterns (except for Japan/UK/Ireland/Spain/France handled above)
    roll = random.random()
    if country not in ["Japan", "England", "Scotland", "Ireland", "Spain", "France"] and city and roll < 0.07:
        name = f"{city} {random.choice(filtered_structures)}"
    else:
        while True:
            name = random.choice(patterns)()
            # Filter out 'Beach' for non-coastal cities in the final name
            if 'Beach' in name and (not city or city not in COASTAL_CITIES):
                continue
            # Never allow names ending with 'St.'
            if name.endswith('St.'):
                continue
            # Only allow 'Resort' for US and Australia
            if 'Resort' in name and country not in ['USA', 'Australia']:
                continue
            # Only allow 'Resort' as a suffix to a substantial name (not 'Park Resort', 'Resort Resort', etc.)
            for forbidden in forbidden_combinations:
                if name == forbidden:
                    break
            else:
                # If not forbidden, check for US prefix rules
                if country == "USA" and not filter_us(name):
                    tries += 1
                    if tries > 10:
                        name = f"{random.choice(geo)} {random.choice(us_structures)}"
                        break
                    continue
                if name:
                    break
    return name

def generate_course_characteristics():
    """
    Generate realistic course characteristics using the correct keys for the DB schema.
    """
    characteristics = {
        'temp_factor': round(random.uniform(55, 90), 1),
        'humidity_factor': round(random.uniform(0.2, 0.9), 2),
        'wind_factor': round(random.uniform(0.1, 0.7), 2),
        'rain_factor': round(random.uniform(0.05, 0.6), 2),
        'cloud_factor': 0,
        'design_strategy': round(random.uniform(0.2, 0.9), 2),
        'course_length': random.randint(6900, 7500),
        'narrowness_factor': round(random.uniform(0.2, 0.9), 2),
        'hazard_density': round(random.uniform(0.2, 0.9), 2),
        'green_speed': round(random.uniform(0.3, 1.0), 2),
        'turf_firmness': round(random.uniform(0.3, 1.0), 2),
        'rough_length': round(random.uniform(0.2, 0.9), 2),
        'prestige_level': round(random.uniform(0.2, 1.0), 2),
        'course_age': round(random.uniform(0.0, 1.0), 2),
        'crowd_factor': round(random.uniform(0.2, 1.0), 2),
        'elevation_factor': round(random.uniform(0.0, 1.0), 2),
        'terrain_difficulty': round(random.uniform(0.1, 0.9), 2)
    }
    return characteristics

def generate_hole_pars():
    while True:
        total_par = random.randint(70, 73)
        num_par3 = random.randint(3, 5)
        num_par5 = random.randint(2, 4)
        num_par4 = 18 - num_par3 - num_par5
        # Check if possible to reach total_par with these counts
        sum_pars = num_par3 * 3 + num_par4 * 4 + num_par5 * 5
        diff = total_par - sum_pars
        if abs(diff) > 1:
            continue  # Too far off, try again
        # Adjust one par 4 if needed
        par_list = [3]*num_par3 + [4]*num_par4 + [5]*num_par5
        # Try to distribute pars with constraints
        for _ in range(100):  # Try up to 100 shuffles
            random.shuffle(par_list)
            # Placeholders for holes
            holes = [None]*18
            # Place at least one par 3 and one par 5 in front and back nine
            front_indices = list(range(0,9))
            back_indices = list(range(9,18))
            # Place par 3s and 5s in both nines
            front_par3 = [i for i in front_indices if i not in [0,1]]
            back_par3 = [i for i in back_indices if i != 17]
            front_par5 = front_indices[:]
            back_par5 = back_indices[:]
            # Assign one par 3 and one par 5 to each nine
            random.shuffle(front_par3)
            random.shuffle(back_par3)
            random.shuffle(front_par5)
            random.shuffle(back_par5)
            holes[front_par3[0]] = 3
            holes[back_par3[0]] = 3
            holes[front_par5[0]] = 5
            holes[back_par5[0]] = 5
            # Remove those from par_list
            used = [holes[i] for i in range(18) if holes[i] is not None]
            temp_par_list = par_list[:]
            for v in used:
                temp_par_list.remove(v)
            # Fill remaining holes
            for i in range(18):
                if holes[i] is None:
                    holes[i] = temp_par_list.pop()
            # Check constraints
            valid = True
            for i in range(17):
                if holes[i] == holes[i+1] and holes[i] in [3,5]:
                    valid = False
                    break
            if holes[0] == 3 or holes[1] == 3 or holes[17] == 3:
                valid = False
            # Check at least one par 3 and 5 in each nine
            if not (3 in holes[:9] and 3 in holes[9:] and 5 in holes[:9] and 5 in holes[9:]):
                valid = False
            if valid:
                # Adjust for total_par if needed
                if diff == 1:
                    # Try to upgrade a par 4 to a par 5 (not consecutive)
                    for i in range(18):
                        if holes[i] == 4:
                            if (i == 0 or holes[i-1] != 5) and (i == 17 or holes[i+1] != 5):
                                holes[i] = 5
                                break
                elif diff == -1:
                    # Try to downgrade a par 4 to a par 3 (not consecutive)
                    for i in range(18):
                        if holes[i] == 4:
                            if (i == 0 or holes[i-1] != 3) and (i == 17 or holes[i+1] != 3):
                                holes[i] = 3
                                break
                if sum(holes) == total_par:
                    return holes, total_par
    # Fallback (should never hit)
    return [4]*18, 72

def normalize_yardage(yards, min_yards=6900, max_yards=7500):
    return (yards - min_yards) / (max_yards - min_yards)

def generate_course_yardage():
    yards = random.randint(6900, 7500)
    norm = normalize_yardage(yards)
    return yards, norm

def generate_static_course_variables(region_env=None):
    # region_env: dict of climate group averages (optional, can influence some variables)
    static_vars = {}
    static_vars['prestige'] = round(random.uniform(0.2, 1.0), 2)  # 0.2-1.0, higher = more pressure
    static_vars['hazard_density'] = round(random.uniform(0.2, 0.9), 2)
    static_vars['narrowness'] = round(random.uniform(0.2, 0.9), 2)
    static_vars['green_speed'] = round(random.uniform(0.3, 1.0), 2)
    static_vars['turf_firmness'] = round(random.uniform(0.3, 1.0), 2)
    static_vars['rough_length'] = round(random.uniform(0.2, 0.9), 2)
    static_vars['course_age'] = round(random.uniform(0.0, 1.0), 2)  # 0=new, 1=historic
    static_vars['crowd_factor'] = round(random.uniform(0.2, 1.0), 2)
    static_vars['elevation_factor'] = round(random.uniform(0.0, 1.0), 2)
    static_vars['terrain_difficulty'] = round(random.uniform(0.1, 0.9), 2)
    static_vars['design_strategy'] = round(random.uniform(0.2, 0.9), 2)
    # Optionally, region_env can influence some variables (e.g., elevation, green_speed)
    if region_env:
        if region_env['avg_temp'] < 65:
            static_vars['turf_firmness'] = min(static_vars['turf_firmness'], 0.7)  # cooler = softer
        if region_env['humidity'] > 0.7:
            static_vars['rough_length'] = max(static_vars['rough_length'], 0.5)  # humid = lusher rough
        if region_env['wind'] > 0.4:
            static_vars['hazard_density'] = max(static_vars['hazard_density'], 0.5)  # windier = more hazards
    return static_vars

# --- Climate Region Mapping and Environmental Averages ---

CLIMATE_GROUPS = {
    'Pacific Northwest': {
        'states': ['Washington', 'Oregon'],
        'avg_temp': 60, 'rain_prob': 0.6, 'wind': 0.4, 'humidity': 0.7
    },
    'California Coast': {
        'states': ['California'],
        'avg_temp': 68, 'rain_prob': 0.15, 'wind': 0.25, 'humidity': 0.5
    },
    'Southwest Desert': {
        'states': ['Arizona', 'Nevada', 'New Mexico'],
        'avg_temp': 90, 'rain_prob': 0.05, 'wind': 0.2, 'humidity': 0.2
    },
    'Mountain West': {
        'states': ['Colorado', 'Utah', 'Idaho', 'Montana', 'Wyoming'],
        'avg_temp': 70, 'rain_prob': 0.15, 'wind': 0.3, 'humidity': 0.3
    },
    'Great Plains': {
        'states': ['Kansas', 'Nebraska', 'Oklahoma', 'South Dakota', 'North Dakota'],
        'avg_temp': 72, 'rain_prob': 0.2, 'wind': 0.5, 'humidity': 0.4
    },
    'Midwest': {
        'states': ['Illinois', 'Indiana', 'Iowa', 'Michigan', 'Minnesota', 'Missouri', 'Ohio', 'Wisconsin'],
        'avg_temp': 68, 'rain_prob': 0.25, 'wind': 0.35, 'humidity': 0.55
    },
    'Northeast': {
        'states': ['New York', 'New Jersey', 'Massachusetts', 'Pennsylvania', 'Connecticut', 'Rhode Island', 'Vermont', 'New Hampshire', 'Maine'],
        'avg_temp': 65, 'rain_prob': 0.3, 'wind': 0.3, 'humidity': 0.6
    },
    'Southeast': {
        'states': ['Florida', 'Georgia', 'Alabama', 'Mississippi', 'Louisiana', 'South Carolina', 'North Carolina', 'Tennessee', 'Arkansas'],
        'avg_temp': 80, 'rain_prob': 0.4, 'wind': 0.25, 'humidity': 0.75
    },
    'Texas': {
        'states': ['Texas'],
        'avg_temp': 85, 'rain_prob': 0.2, 'wind': 0.3, 'humidity': 0.5
    },
    'Alaska': {
        'states': ['Alaska'],
        'avg_temp': 55, 'rain_prob': 0.2, 'wind': 0.3, 'humidity': 0.5
    },
    'Hawaii': {
        'states': ['Hawaii'],
        'avg_temp': 82, 'rain_prob': 0.3, 'wind': 0.2, 'humidity': 0.8
    },
    # International
    'Canada': {
        'countries': ['Canada'],
        'avg_temp': 60, 'rain_prob': 0.25, 'wind': 0.3, 'humidity': 0.6
    },
    'British Isles': {
        'countries': ['England', 'Scotland', 'Ireland'],
        'avg_temp': 62, 'rain_prob': 0.4, 'wind': 0.35, 'humidity': 0.7
    },
    'Japan': {
        'countries': ['Japan'],
        'avg_temp': 70, 'rain_prob': 0.3, 'wind': 0.25, 'humidity': 0.7
    },
    'Australia': {
        'countries': ['Australia'],
        'avg_temp': 78, 'rain_prob': 0.15, 'wind': 0.3, 'humidity': 0.4
    },
}

def get_climate_group(city, state_country):
    # US states
    for group, data in CLIMATE_GROUPS.items():
        if 'states' in data and state_country in data['states']:
            return group, data
        if 'countries' in data and state_country in data['countries']:
            return group, data
    # Default fallback
    return 'Default', {'avg_temp': 70, 'rain_prob': 0.2, 'wind': 0.3, 'humidity': 0.5}

def assign_hole_handicaps(holes):
    if len(holes) != 18:
        raise ValueError(f"Expected 18 holes, got {len(holes)}")
    # Assign a raw difficulty score (par + random noise)
    for h in holes:
        h['difficulty_score'] = h['par'] + random.uniform(-0.3, 0.3)
    # Rank holes by difficulty (descending)
    ranked = sorted(holes, key=lambda h: -h['difficulty_score'])
    # Assign stroke indices 1–18
    for idx, h in enumerate(ranked):
        h['handicap'] = idx + 1
    # Prepare odd and even indices
    odd_indices = list(range(1, 18, 2))  # 1, 3, ..., 17
    even_indices = list(range(2, 19, 2)) # 2, 4, ..., 18
    random.shuffle(odd_indices)
    random.shuffle(even_indices)
    # Randomly assign odds to front or back nine
    if random.choice([True, False]):
        front_indices, back_indices = odd_indices, even_indices
    else:
        front_indices, back_indices = even_indices, odd_indices
    # Assign to holes 1–9 and 10–18
    holes_sorted = sorted(holes, key=lambda h: h['hole'])
    for i in range(9):
        holes_sorted[i]['handicap'] = front_indices[i]
        holes_sorted[i+9]['handicap'] = back_indices[i]
    return holes_sorted

def calculate_course_rating_and_slope(par, yardage_norm, hazard_density, narrowness, green_speed, rough_length, prestige, turf_firmness):
    # Course Rating
    course_rating = par
    course_rating += (yardage_norm * 2.0)  # up to +2 for max length
    course_rating += (hazard_density * 1.0)
    course_rating += (narrowness * 1.0)
    course_rating += (green_speed * 0.5)
    course_rating += (rough_length * 0.5)
    course_rating += (prestige * 0.5)
    course_rating += random.uniform(-0.3, 0.3)
    course_rating = round(course_rating, 1)
    # Slope Rating
    slope = 113
    slope += int((hazard_density + rough_length + narrowness) * 20)
    slope += int((yardage_norm - 0.5) * 30)  # longer = higher slope
    slope += int((green_speed + turf_firmness) * 10)
    slope = max(55, min(155, slope))
    return course_rating, slope

# --- Mappings for abbreviations and codes ---
US_STATE_ABBR = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
    'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
    'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}
CA_PROV_ABBR = {
    'Alberta': 'AB', 'British Columbia': 'BC', 'Manitoba': 'MB', 'New Brunswick': 'NB', 'Newfoundland and Labrador': 'NL',
    'Nova Scotia': 'NS', 'Ontario': 'ON', 'Prince Edward Island': 'PE', 'Quebec': 'QC', 'Saskatchewan': 'SK',
    'Northwest Territories': 'NT', 'Nunavut': 'NU', 'Yukon': 'YT'
}
COUNTRY_CODES = {
    'USA': 'US', 'United States': 'US', 'Canada': 'CAN', 'England': 'UK', 'Scotland': 'UK', 'Ireland': 'Ireland',
    'Japan': 'Japan', 'France': 'France', 'Spain': 'Spain', 'Australia': 'AUS',
}

def format_location(city, state, country):
    code = COUNTRY_CODES.get(country, country)
    if country in ['USA', 'United States']:
        st = US_STATE_ABBR.get(state, state)
        return f"{city}, {st} (US)"
    elif country == 'Canada':
        prov = CA_PROV_ABBR.get(state, state)
        return f"{city}, {prov} (CAN)"
    elif country in ['England', 'Scotland']:
        return f"{city}, {country} (UK)"
    elif country == 'Ireland':
        return f"{city}, Ireland"
    elif country == 'Japan':
        return f"{city}, Japan"
    elif country == 'Australia':
        prov = CA_PROV_ABBR.get(state, state)  # Use province mapping if you want, or just state
        return f"{city}, {prov} (AUS)"
    else:
        return f"{city}, {country}"

def main():
    parser = argparse.ArgumentParser(description="Generate a golf course.")
    parser.add_argument('--city', type=str, help='City for the course')
    parser.add_argument('--state', type=str, help='State/Province for the course')
    parser.add_argument('--country', type=str, help='Country for the course')
    parser.add_argument('--confirm', action='store_true', help='Prompt for confirmation before inserting into the database')
    args = parser.parse_args()

    print("🎯 Golf Course Generator (Single Course)")
    print("\n1. Ensuring database tables exist...")
    create_course_tables()
    print("   -> Tables 'courses', 'course_characteristics', and 'tournaments' are ready.")

    if args.city and args.country:
        city = args.city
        state = args.state if args.state is not None else ''
        country = args.country
        print(f"[DEBUG] Using provided location: {city}, {state}, {country}")
    elif args.state:
        city, state, country = get_random_location(state=args.state)
        print(f"[DEBUG] Using random location in US state {state}: {city}, {state}, {country}")
    elif args.country:
        city, state, country = get_random_location(args.country)
        print(f"[DEBUG] Using random location in {args.country}: {city}, {state}, {country}")
    else:
        city, state, country = get_random_location()
        print(f"[DEBUG] Using random location: {city}, {state}, {country}")

    # Try to generate a unique course name/location
    max_attempts = 10
    orig_city, orig_state, orig_country = city, state, country  # Save originals
    for attempt in range(max_attempts):
        # Only regenerate the course name, not the location
        if orig_country in ["England", "Scotland", "Ireland"]:
            state_country = orig_country
        else:
            state_country = f"{orig_state}, {orig_country}"
        course_name = generate_course_name(orig_country, orig_city, orig_state)
        # Check for uniqueness
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM courses WHERE name = ?', (course_name,))
        exists = cur.fetchone()[0]
        conn.close()
        if not exists:
            break
        if attempt == max_attempts - 1:
            raise Exception("Could not generate a unique course name after 10 attempts.")

    characteristics = generate_course_characteristics()
    prestige = int(70 + 30 * characteristics['prestige_level'])  # Range 70-100

    print("\n--- GENERATED COURSE ---")
    print(f"Name:    {course_name}")
    print(f"Location: {orig_city}, {state_country}")
    print(f"Prestige: {prestige}")
    for key, val in characteristics.items():
        print(f"{key.replace('_', ' ').title():<20}: {val}")
    print("------------------------")

    print("\n5. Generating hole pars...")
    holes, total_par = generate_hole_pars()
    print("Hole pars:", holes)
    print("Total par:", total_par)

    print("\n6. Generating course yardage...")
    yards, norm = generate_course_yardage()
    print(f"Course yardage: {yards} yards (normalized: {norm:.3f})")

    print("\n7. Generating static course variables...")
    _, region_env = get_climate_group(orig_city, state_country)
    static_vars = generate_static_course_variables(region_env)
    for k, v in static_vars.items():
        print(f"{k}: {v}")

    print("\n8. Assigning hole handicaps...")
    holes_list = [{'hole': i+1, 'par': par} for i, par in enumerate(holes)]
    if len(holes_list) != 18:
        raise ValueError(f"Expected 18 holes, got {len(holes_list)}")
    holes_with_handicaps = assign_hole_handicaps(holes_list)
    print("Hole | Par | Handicap")
    for h in holes_with_handicaps:
        print(f"{h['hole']:>2}   | {h['par']}  | {h['handicap']}")

    print("\n9. Calculating course rating and slope...")
    course_rating, slope = calculate_course_rating_and_slope(
        total_par,
        norm,
        static_vars['hazard_density'],
        static_vars['narrowness'],
        static_vars['green_speed'],
        static_vars['rough_length'],
        static_vars['prestige'],
        static_vars['turf_firmness']
    )
    print(f"Course Rating: {course_rating}")
    print(f"Slope Rating: {slope}")

    print("\n10. Generating sample course names...")
    samples = [
        ("USA", "Dallas", "Texas"),
        ("England", "London", None),
        ("Japan", "Tokyo", None),
        ("Australia", "Sydney", None),
        ("Canada", "Toronto", None),
        ("Scotland", "Edinburgh", None),
        ("Ireland", "Dublin", None),
        ("France", "Paris", None),
    ]
    for country, city, state in samples:
        print(f"{country}: {generate_course_name(country, city, state)}")

    # Generate est_year (random between 1890 and 2020)
    est_year = random.randint(1890, 2020)
    # Use the original city, state, country for location
    location = format_location(orig_city, orig_state, orig_country)
    course = {
        'name': course_name,
        'city': orig_city,
        'state_country': state_country,
        'yardage': yards,
        'par': total_par,
        'est_year': est_year,
        'location': location,
        'prestige': prestige
    }
    # Print course details before confirmation
    print("\n--- GENERATED COURSE ---")
    print(f"Name:    {course_name}")
    print(f"Location: {location}")
    print(f"Prestige: {prestige}")
    print(f"Avg Temperature     : {characteristics['temp_factor']}\u00b0F")
    print(f"Humidity Level      : {characteristics['humidity_factor']}")
    print(f"Wind Factor         : {characteristics['wind_factor']}")
    print(f"Rain Probability    : {characteristics['rain_factor']}")
    print(f"Design Strategy     : {characteristics['design_strategy']}")
    print(f"Course Length       : {characteristics['course_length']}")
    print(f"Narrowness Factor   : {characteristics['narrowness_factor']}")
    print(f"Hazard Density      : {characteristics['hazard_density']}")
    print(f"Green Speed         : {characteristics['green_speed']}")
    print(f"Turf Firmness       : {characteristics['turf_firmness']}")
    print(f"Rough Length        : {characteristics['rough_length']}")
    print(f"Prestige Level      : {characteristics['prestige_level']}")
    print(f"Course Age          : {characteristics['course_age']}")
    print(f"Crowd Factor        : {characteristics['crowd_factor']}")
    print(f"Elevation Factor    : {characteristics['elevation_factor']}")
    print(f"Terrain Difficulty  : {characteristics['terrain_difficulty']}")
    print("------------------------")
    # Confirmation prompt
    interactive = sys.stdin.isatty()
    if interactive:
        response = input("\nAdd this course to the database? (y/n): ").strip().lower()
        if response != 'y':
            print("Course not added.")
            return
    insert_course_to_db(course, characteristics, holes_with_handicaps)

if __name__ == "__main__":
    main() 