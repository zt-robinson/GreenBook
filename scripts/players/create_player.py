#!/usr/bin/env python3
"""
Simple Golf Player Generator
Creates a single golf player with realistic attributes
"""

import random
import sqlite3
from datetime import datetime
from faker import Faker

# A mapping from our country names to Faker-supported locales.
LOCALE_MAP = {
    # English-speaking countries
    'USA': 'en_US',
    'England': 'en_GB',
    'Australia': 'en_AU',
    'Canada': 'en_CA',
    'Ireland': 'en_IE',
    'New Zealand': 'en_NZ',
    
    # Spanish-speaking countries
    'Spain': 'es_ES',
    'Mexico': 'es_MX',
    'Argentina': 'es_AR',
    'Chile': 'es_CL',
    'Colombia': 'es_CO',
    
    # German-speaking countries
    'Germany': 'de_DE',
    'Austria': 'de_AT',
    'Switzerland': 'de_CH',
    
    # French-speaking countries
    'France': 'fr_FR',
    'Belgium': 'fr_BE',
    'French Canada': 'fr_CA',
    
    # Italian-speaking countries
    'Italy': 'it_IT',
    
    # Portuguese-speaking countries
    'Portugal': 'pt_PT',
    'Brazil': 'pt_BR',
    
    # Dutch-speaking countries
    'Netherlands': 'nl_NL',
    'Belgium (Dutch)': 'nl_BE',
    
    # Nordic countries
    'Sweden': 'sv_SE',
    'Norway': 'no_NO',
    'Denmark': 'da_DK',
    'Finland': 'fi_FI',
    'Iceland': 'is_IS',
    
    # Slavic countries (Latin alphabet)
    'Poland': 'pl_PL',
    'Czech Republic': 'cs_CZ',
    'Slovakia': 'sk_SK',
    'Croatia': 'hr_HR',
    'Slovenia': 'sl_SI',
    
    # Baltic countries
    'Lithuania': 'lt_LT',
    'Latvia': 'lv_LV',
    'Estonia': 'et_EE',
    
    # Other European countries
    'Romania': 'ro_RO',
    'Hungary': 'hu_HU',
    'Turkey': 'tr_TR',
    
    # Asian countries (Latin alphabet)
    'Indonesia': 'id_ID',
    'Vietnam': 'vi_VN',
    'Philippines': 'fil_PH',
    
    # Special case - Japanese with Romanized names
    'Japan': 'ja_JP'
}

# PGA Tour realistic nationality distribution (weights for random selection)
# Based on actual PGA Tour demographics - USA dominates, followed by English-speaking countries
COUNTRY_WEIGHTS = {
    'USA': 50,
    'England': 12,
    'Scotland': 8,
    'Ireland': 8,
    'Australia': 8,
    'Canada': 2,
    'Japan': 2,
    'Germany': 1,
    'Sweden': 1,
    'New Zealand': 1,
    'France': 1,
    'Italy': 1,
    'Netherlands': 1,
    'Denmark': 1,
    'Norway': 1,
    'Finland': 1,
    'Austria': 1,
    'Switzerland': 1,
    'Belgium': 1,
    'Portugal': 1,
    'Brazil': 1,
    'Mexico': 1,
    'Argentina': 1,
    'Chile': 1,
    'Colombia': 1,
    'Czech Republic': 1,
    'Poland': 1,
    'Hungary': 1,
    'Turkey': 1,
    'Romania': 1,
    'Croatia': 1,
    'Slovenia': 1,
    'Slovakia': 1,
    'Lithuania': 1,
    'Latvia': 1,
    'Estonia': 1,
    'Iceland': 1,
    'Indonesia': 1,
    'Vietnam': 1,
    'Philippines': 1,
    'French Canada': 1,
    'Belgium (Dutch)': 1
}

# Custom lists for believable, Romanized Japanese male names
JAPANESE_MALE_FIRST_NAMES = [
    "Hiroshi", "Kenji", "Taro", "Akira", "Jiro", "Kazuki", "Yuki", "Daiki", "Satoshi", "Ryo",
    "Haruto", "Yuto", "Sota", "Yuma", "Ryusei", "Shota", "Kaito", "Ren", "Tsubasa", "Itsuki"
]
JAPANESE_LAST_NAMES = [
    "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto", "Nakamura", "Kobayashi", "Kato",
    "Yoshida", "Yamada", "Sasaki", "Yamaguchi", "Matsumoto", "Inoue", "Kimura", "Shimizu", "Hayashi", "Saito"
]

def generate_player_name(country):
    """Generate a realistic, male-only golf player name based on the player's country."""
    if country == 'Japan':
        return f"{random.choice(JAPANESE_MALE_FIRST_NAMES)} {random.choice(JAPANESE_LAST_NAMES)}"
    
    # Handle South Africa case (since en_ZA doesn't work with Faker for names)
    if country == 'South Africa':
        # Use English names for South African players (common in golf)
        fake = Faker('en_US')
        return f"{fake.first_name_male()} {fake.last_name()}"

    locale = LOCALE_MAP.get(country, 'en_US')
    local_fake = Faker(locale)
    return f"{local_fake.first_name_male()} {local_fake.last_name()}"

def generate_player_skills():
    """Generate realistic golf skills (0-100 scale)"""
    # Base skill level (50-85 range for most players)
    base_skill = random.uniform(50, 85)
    
    # Individual skills with some variation
    skills = {
        'driving_power': base_skill + random.uniform(-10, 10),
        'driving_accuracy': base_skill + random.uniform(-15, 15),
        'approach_long': base_skill + random.uniform(-12, 12),
        'approach_short': base_skill + random.uniform(-8, 8),
        'scrambling': base_skill + random.uniform(-10, 10),
        'putting': base_skill + random.uniform(-15, 15),
        'consistency': base_skill + random.uniform(-10, 10),
        'composure': base_skill + random.uniform(-8, 8),
        'resilience': base_skill + random.uniform(-12, 12)
    }
    
    # Clamp values to 0-100 range
    for skill in skills:
        skills[skill] = max(0, min(100, skills[skill]))
    
    return skills

def create_database():
    """Create a simple database for players"""
    conn = sqlite3.connect('golf_players.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            country TEXT,
            status TEXT DEFAULT 'active',
            career_wins INTEGER DEFAULT 0,
            season_money REAL DEFAULT 0,
            driving_power REAL,
            driving_accuracy REAL,
            approach_long REAL,
            approach_short REAL,
            scrambling REAL,
            putting REAL,
            consistency REAL,
            composure REAL,
            resilience REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            world_ranking INTEGER,
            tour_rank INTEGER
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database created successfully")

def save_player_to_db(player_data, world_ranking=None, tour_rank=None):
    """Save a player to the database"""
    conn = sqlite3.connect('golf_players.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO players (name, age, country, status, career_wins, season_money, driving_power, driving_accuracy, approach_long, approach_short, scrambling, putting, consistency, composure, resilience, world_ranking, tour_rank)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        player_data['name'], player_data['age'], player_data['country'], player_data['status'],
        player_data['career_wins'], player_data['season_money'], player_data['driving_power'],
        player_data['driving_accuracy'], player_data['approach_long'], player_data['approach_short'],
        player_data['scrambling'], player_data['putting'], player_data['consistency'],
        player_data['composure'], player_data['resilience'], world_ranking, tour_rank
    ))
    
    conn.commit()
    player_id = cursor.lastrowid
    conn.close()
    
    print(f"✅ Player saved to database with ID: {player_id}")
    return player_id

def generate_single_player(world_ranking=None, tour_rank=None):
    """Generate a single player with all attributes"""
    country = random.choices(list(COUNTRY_WEIGHTS.keys()), weights=list(COUNTRY_WEIGHTS.values()))[0]
    
    player = {
        'name': generate_player_name(country),
        'age': random.randint(22, 45),
        'country': country,
        'status': 'active',
        'career_wins': 0,
        'season_money': 0.0,
        'skills': generate_player_skills()
    }
    
    player_data = {
        'name': player['name'],
        'age': player['age'],
        'country': player['country'],
        'status': player['status'],
        'career_wins': player['career_wins'],
        'season_money': player['season_money'],
        **player['skills']
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
    print(f"Country: {player['country']}")
    print(f"Career Wins: {player['career_wins']}")
    print(f"Season Money: ${player['season_money']:,.2f}")
    print("\nSKILLS (0-100 scale):")
    print("-" * 30)
    for skill, value in player['skills'].items():
        skill_name = skill.replace('_', ' ').title()
        print(f"{skill_name}: {value:.1f}")
    print("="*50)

def main():
    print("🎯 Golf Player Generator")
    print("\nCreating database...")
    create_database()
    print("✅ Database created successfully\n")
    # Find the next available world ranking and tour rank
    conn = sqlite3.connect('golf_players.db')
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
    print(f"Player saved with ID: {player_id}")

if __name__ == "__main__":
    main() 