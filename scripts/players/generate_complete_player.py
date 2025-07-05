#!/usr/bin/env python3
"""
Complete Golf Player Generation System
Creates players with realistic attributes for tournament simulation
"""

import random
import sqlite3
import os
import sys
from datetime import datetime
from faker import Faker

# Add the greenbook directory to the path so we can import config
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from config import PLAYER_DB_PATH

# Nationality distribution based on PGA Tour demographics
NATIONALITY_WEIGHTS = {
    'USA': 50,           # 50% American players
    'England': 12,       # British players
    'Scotland': 8,       # Scottish players
    'Ireland': 8,        # Irish players
    'Australia': 8,      # Australian players
    'Canada': 4,         # Canadian players
    'Japan': 2,          # Japanese players
    'Germany': 2,        # German players
    'South Africa': 2,   # South African players
    'Spain': 1,          # Spanish players
    'Sweden': 1,         # Swedish players
    'New Zealand': 1,    # New Zealand players
    'France': 1,         # French players
    'Italy': 1,          # Italian players
    'Netherlands': 1,    # Dutch players
    'Denmark': 1,        # Danish players
    'Norway': 1,         # Norwegian players
    'Finland': 1,        # Finnish players
    'Austria': 1,        # Austrian players
    'Switzerland': 1,    # Swiss players
    'Belgium': 1,        # Belgian players
    'Portugal': 1,       # Portuguese players
    'Brazil': 1,         # Brazilian players
    'Mexico': 1,         # Mexican players
    'Argentina': 1,      # Argentine players
    'Chile': 1,          # Chilean players
    'Colombia': 1,       # Colombian players
    'Czech Republic': 1, # Czech players
    'Poland': 1,         # Polish players
    'Hungary': 1,        # Hungarian players
    'Turkey': 1,         # Turkish players
    'Romania': 1,        # Romanian players
    'Croatia': 1,        # Croatian players
    'Slovenia': 1,       # Slovenian players
    'Slovakia': 1,       # Slovakian players
    'Lithuania': 1,      # Lithuanian players
    'Latvia': 1,         # Latvian players
    'Estonia': 1,        # Estonian players
    'Iceland': 1,        # Icelandic players
    'Indonesia': 1,      # Indonesian players
    'Vietnam': 1,        # Vietnamese players
    'Philippines': 1,    # Filipino players
    'French Canada': 1,  # French Canadian players
    'Belgium (Dutch)': 1 # Dutch Belgian players
}

# Locale mapping for name generation
LOCALE_MAP = {
    'USA': 'en_US',
    'England': 'en_GB',
    'Scotland': 'en_GB',  # Scottish names from GB locale
    'Ireland': 'en_IE',
    'Australia': 'en_AU',
    'Canada': 'en_CA',
    'Japan': 'ja_JP',
    'Germany': 'de_DE',
    'South Africa': 'en_US',  # Use US names for South African players
    'Spain': 'es_ES',
    'Sweden': 'sv_SE',
    'New Zealand': 'en_NZ',
    'France': 'fr_FR',
    'Italy': 'it_IT',
    'Netherlands': 'nl_NL',
    'Denmark': 'da_DK',
    'Norway': 'no_NO',
    'Finland': 'fi_FI',
    'Austria': 'de_AT',
    'Switzerland': 'de_CH',
    'Belgium': 'fr_BE',
    'Portugal': 'pt_PT',
    'Brazil': 'pt_BR',
    'Mexico': 'es_MX',
    'Argentina': 'es_AR',
    'Chile': 'es_CL',
    'Colombia': 'es_CO',
    'Czech Republic': 'cs_CZ',
    'Poland': 'pl_PL',
    'Hungary': 'hu_HU',
    'Turkey': 'tr_TR',
    'Romania': 'ro_RO',
    'Croatia': 'hr_HR',
    'Slovenia': 'sl_SI',
    'Slovakia': 'sk_SK',
    'Lithuania': 'lt_LT',
    'Latvia': 'lv_LV',
    'Estonia': 'et_EE',
    'Iceland': 'is_IS',
    'Indonesia': 'id_ID',
    'Vietnam': 'vi_VN',
    'Philippines': 'fil_PH',
    'French Canada': 'fr_CA',
    'Belgium (Dutch)': 'nl_BE'
}

# Custom Japanese names for more realistic results
JAPANESE_MALE_FIRST_NAMES = [
    "Hiroshi", "Kenji", "Taro", "Akira", "Jiro", "Kazuki", "Yuki", "Daiki", "Satoshi", "Ryo",
    "Haruto", "Yuto", "Sota", "Yuma", "Ryusei", "Shota", "Kaito", "Ren", "Tsubasa", "Itsuki"
]

JAPANESE_LAST_NAMES = [
    "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto", "Nakamura", "Kobayashi", "Kato",
    "Yoshida", "Yamada", "Sasaki", "Yamaguchi", "Matsumoto", "Inoue", "Kimura", "Shimizu", "Hayashi", "Saito"
]

def generate_player_name(nationality):
    """Generate a realistic male golf player name based on nationality"""
    
    # Special handling for Japanese names
    if nationality == 'Japan':
        return f"{random.choice(JAPANESE_MALE_FIRST_NAMES)} {random.choice(JAPANESE_LAST_NAMES)}"
    
    # Get locale for the nationality
    locale = LOCALE_MAP.get(nationality, 'en_US')
    fake = Faker(locale)
    
    return f"{fake.first_name_male()} {fake.last_name()}"

def generate_player_skills():
    """Generate random skills for a player (0-100 scale)"""
    
    # Generate random physical skills with wide variety but no obvious winners/losers
    physical_skills = {
        'driving_power': random.uniform(30, 95),
        'driving_accuracy': random.uniform(30, 95),
        'approach_accuracy': random.uniform(30, 95),
        'short_game': random.uniform(30, 95),
        'putting': random.uniform(30, 95)
    }
    
    # Generate mental game attributes
    mental_skills = {
        'composure': random.uniform(30, 95),
        'confidence': random.uniform(40, 90),  # Start with moderate confidence
        'focus': random.uniform(30, 95),
        'risk_tolerance': random.uniform(20, 85),  # Conservative to aggressive
        'mental_fatigue': random.uniform(30, 95),
        'consistency': random.uniform(30, 95),
        'resilience': random.uniform(30, 95)
    }
    
    # Combine all skills
    all_skills = {**physical_skills, **mental_skills}
    
    # Clamp all values to 0-100 range
    for skill in all_skills:
        all_skills[skill] = max(0, min(100, all_skills[skill]))
    
    return all_skills

def create_database():
    """Create the players database if it doesn't exist"""
    conn = sqlite3.connect(PLAYER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            nationality TEXT,
            status TEXT DEFAULT 'active',
            career_wins INTEGER DEFAULT 0,
            season_money REAL DEFAULT 0,
            driving_power REAL,
            driving_accuracy REAL,
            approach_accuracy REAL,
            short_game REAL,
            putting REAL,
            composure REAL,
            confidence REAL,
            focus REAL,
            risk_tolerance REAL,
            mental_fatigue REAL,
            consistency REAL,
            resilience REAL,
            force_retirement INTEGER,
            peak_adder REAL,
            peak_age INTEGER,
            peak_duration INTEGER,
            peak_start INTEGER,
            peak_stop INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            world_ranking INTEGER,
            tour_rank INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database created (or already exists)")

def save_player_to_db(player_data, world_ranking=None, tour_rank=None):
    """Save a player to the database"""
    conn = sqlite3.connect(PLAYER_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO players (
            name, age, nationality, status, career_wins, season_money, 
            driving_power, driving_accuracy, approach_accuracy, short_game, putting,
            composure, confidence, focus, risk_tolerance, mental_fatigue, consistency, resilience,
            force_retirement, peak_adder, peak_age, peak_duration, peak_start, peak_stop,
            world_ranking, tour_rank
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    ''', (
        player_data['name'], player_data['age'], player_data['nationality'], player_data['status'],
        player_data['career_wins'], player_data['season_money'], player_data['driving_power'],
        player_data['driving_accuracy'], player_data['approach_accuracy'], player_data['short_game'],
        player_data['putting'], player_data['composure'], player_data['confidence'], player_data['focus'],
        player_data['risk_tolerance'], player_data['mental_fatigue'], player_data['consistency'],
        player_data['resilience'], player_data['force_retirement'], player_data['peak_adder'],
        player_data['peak_age'], player_data['peak_duration'], player_data['peak_start'], player_data['peak_stop'],
        world_ranking, tour_rank
    ))
    conn.commit()
    player_id = cursor.lastrowid
    conn.close()
    print(f"✅ Player saved to database with ID: {player_id}")
    return player_id

def generate_single_player(world_ranking=None, tour_rank=None):
    """Generate a single player with all attributes"""
    # Select nationality based on weights
    nationality = random.choices(list(NATIONALITY_WEIGHTS.keys()), 
                               weights=list(NATIONALITY_WEIGHTS.values()))[0]
    # Generate player data
    age = random.randint(20, 23)
    force_retirement = random.randint(45, 50)
    peak_adder = round(random.uniform(0.4, 0.7), 3)
    peak_age = random.randint(29, 33)
    peak_duration = random.randint(2, 3)
    peak_start = peak_age - random.randint(1, 2)
    peak_stop = (peak_age + (peak_duration - 1)) + random.randint(1, 2)
    player = {
        'name': generate_player_name(nationality),
        'age': age,
        'nationality': nationality,
        'status': 'active',
        'career_wins': 0,
        'season_money': 0.0,
        'skills': generate_player_skills(),
        'force_retirement': force_retirement,
        'peak_adder': peak_adder,
        'peak_age': peak_age,
        'peak_duration': peak_duration,
        'peak_start': peak_start,
        'peak_stop': peak_stop
    }
    # Prepare data for database
    player_data = {
        'name': player['name'],
        'age': player['age'],
        'nationality': player['nationality'],
        'status': player['status'],
        'career_wins': player['career_wins'],
        'season_money': player['season_money'],
        **player['skills'],
        'force_retirement': player['force_retirement'],
        'peak_adder': player['peak_adder'],
        'peak_age': player['peak_age'],
        'peak_duration': player['peak_duration'],
        'peak_start': player['peak_start'],
        'peak_stop': player['peak_stop']
    }
    player_id = save_player_to_db(player_data, world_ranking=world_ranking, tour_rank=tour_rank)
    return player_id, player_data

def display_player(player):
    """Display player information in a nice format"""
    print("\n" + "="*50)
    print(f"🏌️  GOLF PLAYER GENERATED")
    print("="*50)
    print(f"Name: {player['name']}")
    print(f"Age: {player['age']}")
    print(f"Nationality: {player['nationality']}")
    print(f"Career Wins: {player['career_wins']}")
    print(f"Season Money: ${player['season_money']:,.2f}")
    print("\nPHYSICAL SKILLS (0-100 scale):")
    print("-" * 30)
    physical_skills = ['driving_power', 'driving_accuracy', 'approach_accuracy', 'short_game', 'putting']
    for skill in physical_skills:
        skill_name = skill.replace('_', ' ').title()
        print(f"{skill_name}: {player['skills'][skill]:.1f}")
    
    print("\nMENTAL ATTRIBUTES (0-100 scale):")
    print("-" * 30)
    mental_skills = ['composure', 'confidence', 'focus', 'risk_tolerance', 'mental_fatigue', 'consistency', 'resilience']
    for skill in mental_skills:
        skill_name = skill.replace('_', ' ').title()
        print(f"{skill_name}: {player['skills'][skill]:.1f}")
    print("="*50)

def main():
    """Generate a single player"""
    print("🎯 Complete Golf Player Generator")
    print("\nCreating database...")
    create_database()
    
    # Find the next available world ranking and tour rank
    conn = sqlite3.connect(PLAYER_DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT MAX(world_ranking) FROM players')
    row = cur.fetchone()
    next_ranking = (row[0] or 0) + 1
    
    cur.execute('SELECT MAX(tour_rank) FROM players')
    row = cur.fetchone()
    next_tour_rank = (row[0] or 0) + 1
    conn.close()
    
    print(f"\nGenerating player {next_ranking} (Tour Rank: {next_tour_rank})...")
    player_id, player_data = generate_single_player(world_ranking=next_ranking, tour_rank=next_tour_rank)
    
    # Display the generated player
    player = {
        'name': player_data['name'],
        'age': player_data['age'],
        'nationality': player_data['nationality'],
        'career_wins': player_data['career_wins'],
        'season_money': player_data['season_money'],
        'skills': {
            'driving_power': player_data['driving_power'],
            'driving_accuracy': player_data['driving_accuracy'],
            'approach_accuracy': player_data['approach_accuracy'],
            'short_game': player_data['short_game'],
            'putting': player_data['putting'],
            'composure': player_data['composure'],
            'confidence': player_data['confidence'],
            'focus': player_data['focus'],
            'risk_tolerance': player_data['risk_tolerance'],
            'mental_fatigue': player_data['mental_fatigue'],
            'consistency': player_data['consistency'],
            'resilience': player_data['resilience']
        }
    }
    
    display_player(player)
    print(f"Player saved with ID: {player_id}")

if __name__ == "__main__":
    main() 