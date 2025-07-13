#!/usr/bin/env python3
"""
Generate Players for Prehistory
Generates a specified number of players with random attributes and inserts them into the prehistory database.
Uses the same naming and nationality logic as the main greenbook player generation system.
"""

import sqlite3
import os
import random
import argparse
from datetime import datetime
from faker import Faker

# Path to the prehistory database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'prehistory.db')

# Nationality distribution based on PGA Tour demographics (same as main system)
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

# Locale mapping for name generation (same as main system)
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

# Custom Japanese names for more realistic results (same as main system)
JAPANESE_MALE_FIRST_NAMES = [
    "Hiroshi", "Kenji", "Taro", "Akira", "Jiro", "Kazuki", "Yuki", "Daiki", "Satoshi", "Ryo",
    "Haruto", "Yuto", "Sota", "Yuma", "Ryusei", "Shota", "Kaito", "Ren", "Tsubasa", "Itsuki"
]

JAPANESE_LAST_NAMES = [
    "Sato", "Suzuki", "Takahashi", "Tanaka", "Watanabe", "Ito", "Yamamoto", "Nakamura", "Kobayashi", "Kato",
    "Yoshida", "Yamada", "Sasaki", "Yamaguchi", "Matsumoto", "Inoue", "Kimura", "Shimizu", "Hayashi", "Saito"
]

# Common male first names for problematic locales to ensure male-only generation
MALE_FIRST_NAMES = {
    'es_MX': ['Carlos', 'Miguel', 'Jose', 'Luis', 'Antonio', 'Manuel', 'Francisco', 'David', 'Juan', 'Roberto'],
    'es_ES': ['Carlos', 'Miguel', 'Jose', 'Luis', 'Antonio', 'Manuel', 'Francisco', 'David', 'Juan', 'Roberto'],
    'es_AR': ['Carlos', 'Miguel', 'Jose', 'Luis', 'Antonio', 'Manuel', 'Francisco', 'David', 'Juan', 'Roberto'],
    'es_CL': ['Carlos', 'Miguel', 'Jose', 'Luis', 'Antonio', 'Manuel', 'Francisco', 'David', 'Juan', 'Roberto'],
    'es_CO': ['Carlos', 'Miguel', 'Jose', 'Luis', 'Antonio', 'Manuel', 'Francisco', 'David', 'Juan', 'Roberto'],
    'pt_PT': ['Joao', 'Pedro', 'Miguel', 'Diogo', 'Tiago', 'Andre', 'Ricardo', 'Nuno', 'Paulo', 'Carlos'],
    'pt_BR': ['Joao', 'Pedro', 'Miguel', 'Diogo', 'Tiago', 'Andre', 'Ricardo', 'Nuno', 'Paulo', 'Carlos'],
    'it_IT': ['Marco', 'Alessandro', 'Luca', 'Giuseppe', 'Antonio', 'Roberto', 'Andrea', 'Matteo', 'Paolo', 'Stefano'],
    'fr_FR': ['Pierre', 'Jean', 'Michel', 'Philippe', 'Alain', 'Christian', 'Daniel', 'Bernard', 'Patrick', 'Francois'],
    'fr_CA': ['Pierre', 'Jean', 'Michel', 'Philippe', 'Alain', 'Christian', 'Daniel', 'Bernard', 'Patrick', 'Francois'],
    'fr_BE': ['Pierre', 'Jean', 'Michel', 'Philippe', 'Alain', 'Christian', 'Daniel', 'Bernard', 'Patrick', 'Francois'],
    'nl_NL': ['Jan', 'Piet', 'Klaas', 'Henk', 'Wim', 'Hans', 'Gerard', 'Theo', 'Ronald', 'Frank'],
    'nl_BE': ['Jan', 'Piet', 'Klaas', 'Henk', 'Wim', 'Hans', 'Gerard', 'Theo', 'Ronald', 'Frank'],
    'de_DE': ['Hans', 'Klaus', 'Wolfgang', 'Peter', 'Michael', 'Thomas', 'Andreas', 'Frank', 'Dieter', 'Manfred'],
    'de_AT': ['Hans', 'Klaus', 'Wolfgang', 'Peter', 'Michael', 'Thomas', 'Andreas', 'Frank', 'Dieter', 'Manfred'],
    'de_CH': ['Hans', 'Klaus', 'Wolfgang', 'Peter', 'Michael', 'Thomas', 'Andreas', 'Frank', 'Dieter', 'Manfred'],
    'sv_SE': ['Erik', 'Johan', 'Anders', 'Mikael', 'Lars', 'Karl', 'Per', 'Gustav', 'Fredrik', 'Magnus'],
    'no_NO': ['Erik', 'Johan', 'Anders', 'Mikael', 'Lars', 'Karl', 'Per', 'Gustav', 'Fredrik', 'Magnus'],
    'da_DK': ['Erik', 'Johan', 'Anders', 'Mikael', 'Lars', 'Karl', 'Per', 'Gustav', 'Fredrik', 'Magnus'],
    'fi_FI': ['Mika', 'Jari', 'Antti', 'Pekka', 'Juha', 'Markku', 'Heikki', 'Kari', 'Timo', 'Seppo'],
    'pl_PL': ['Piotr', 'Jan', 'Tomasz', 'Marek', 'Andrzej', 'Krzysztof', 'Jacek', 'Mariusz', 'Wojciech', 'Grzegorz'],
    'hu_HU': ['Istvan', 'Jozsef', 'Laszlo', 'Sandor', 'Ferenc', 'Gabor', 'Zoltan', 'Tamas', 'Mihaly', 'Karoly'],
    'cs_CZ': ['Jan', 'Petr', 'Josef', 'Pavel', 'Martin', 'Tomas', 'Jaroslav', 'Ladislav', 'Milan', 'Vaclav'],
    'sk_SK': ['Jan', 'Petr', 'Josef', 'Pavel', 'Martin', 'Tomas', 'Jaroslav', 'Ladislav', 'Milan', 'Vaclav'],
    'ro_RO': ['Ion', 'Vasile', 'Gheorghe', 'Constantin', 'Mihai', 'Nicolae', 'Dumitru', 'Alexandru', 'Stefan', 'Cristian'],
    'hr_HR': ['Ivan', 'Josip', 'Petar', 'Ante', 'Stjepan', 'Marko', 'Tomislav', 'Zoran', 'Dragan', 'Boris'],
    'sl_SI': ['Ivan', 'Josip', 'Petar', 'Ante', 'Stjepan', 'Marko', 'Tomislav', 'Zoran', 'Dragan', 'Boris'],
    'lt_LT': ['Jonas', 'Petras', 'Vytautas', 'Algirdas', 'Kazys', 'Antanas', 'Juozas', 'Stasys', 'Vladas', 'Rimantas'],
    'lv_LV': ['Janis', 'Peteris', 'Andris', 'Juris', 'Edgars', 'Miks', 'Kristaps', 'Rihards', 'Arturs', 'Dainis'],
    'et_EE': ['Jaan', 'Peeter', 'Andres', 'Tarmo', 'Raivo', 'Mati', 'Priit', 'Urmas', 'Marek', 'Kaur'],
    'is_IS': ['Jon', 'Gunnar', 'Einar', 'Bjorn', 'Arni', 'Sigurdur', 'Olafur', 'Magnus', 'Thor', 'Kristjan'],
    'tr_TR': ['Mehmet', 'Mustafa', 'Ahmet', 'Ali', 'Hasan', 'Huseyin', 'Ibrahim', 'Murat', 'Omer', 'Yusuf'],
    'vi_VN': ['Nguyen', 'Tran', 'Le', 'Pham', 'Hoang', 'Huynh', 'Phan', 'Vu', 'Dang', 'Bui'],
    'id_ID': ['Budi', 'Sutrisno', 'Hendro', 'Bambang', 'Sukarno', 'Suharto', 'Widodo', 'Joko', 'Ahmad', 'Muhammad'],
    'fil_PH': ['Jose', 'Juan', 'Pedro', 'Miguel', 'Antonio', 'Carlos', 'Manuel', 'Francisco', 'Roberto', 'Ricardo']
}

def generate_player_name(nationality):
    """Generate a realistic male golf player name based on nationality (same as main system)"""
    
    # Special handling for Japanese names
    if nationality == 'Japan':
        return f"{random.choice(JAPANESE_MALE_FIRST_NAMES)} {random.choice(JAPANESE_LAST_NAMES)}"
    
    # Get locale for the nationality
    locale = LOCALE_MAP.get(nationality, 'en_US')
    fake = Faker(locale)
    
    # Use explicit male name lists for problematic locales
    if locale in MALE_FIRST_NAMES:
        first_name = random.choice(MALE_FIRST_NAMES[locale])
    else:
        # For other locales, use faker with male-specific generation
        first_name = fake.first_name_male()
    
    last_name = fake.last_name()
    
    return f"{first_name} {last_name}"

def weighted_random_nationality():
    """Select nationality based on weights (same as main system)"""
    nationalities = list(NATIONALITY_WEIGHTS.keys())
    weights = list(NATIONALITY_WEIGHTS.values())
    return random.choices(nationalities, weights=weights)[0]

def generate_player_attributes():
    """Generate random skills for a player (0-100 scale) - same as main system"""
    
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

def insert_player(conn, player_data):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO players (
            name, age, nationality,
            driving_power, driving_accuracy, approach_accuracy, short_game, putting,
            composure, confidence, focus, risk_tolerance, mental_fatigue, consistency, resilience,
            introduction_season, introduction_event, current_status, created_at, last_updated
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        player_data['name'], player_data['age'], player_data['nationality'],
        player_data['driving_power'], player_data['driving_accuracy'], player_data['approach_accuracy'],
        player_data['short_game'], player_data['putting'],
        player_data['composure'], player_data['confidence'], player_data['focus'],
        player_data['risk_tolerance'], player_data['mental_fatigue'], player_data['consistency'], player_data['resilience'],
        player_data['introduction_season'], player_data['introduction_event'], player_data['current_status'],
        player_data['created_at'], player_data['last_updated']
    ))
    conn.commit()

def generate_players(
    num_players=600, 
    age_min=19, age_max=22, 
    introduction_season=0, introduction_event=0, 
    name_suffix=None
):
    conn = sqlite3.connect(DB_PATH)
    
    # Age up all existing players by 1 year before generating new ones
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET age = age + 1")
    aged_count = cursor.rowcount
    print(f"✅ Aged up {aged_count} existing players by 1 year")
    
    created = 0
    new_player_ids = []
    for _ in range(num_players):
        nationality = weighted_random_nationality()
        name = generate_player_name(nationality)
        if name_suffix:
            name = f"{name} {name_suffix}"
        age = random.randint(age_min, age_max)
        attrs = generate_player_attributes()
        now = datetime.now().isoformat()
        player_data = {
            'name': name,
            'age': age,
            'nationality': nationality,
            **attrs,
            'introduction_season': introduction_season,
            'introduction_event': introduction_event,
            'current_status': 'active',
            'created_at': now,
            'last_updated': now
        }
        insert_player(conn, player_data)
        # Get the last inserted player id
        new_player_ids.append(conn.execute('SELECT last_insert_rowid()').fetchone()[0])
        created += 1
    conn.close()
    print(f"✅ Generated and inserted {created} players into the prehistory database.")
    # Generate markdown report
    generate_full_player_pool_report(new_player_ids)


def generate_full_player_pool_report(new_player_ids):
    """Generate a markdown report of the full player pool, highlighting new players."""
    db_path = DB_PATH
    output_path = os.path.join(os.path.dirname(__file__), '..', '..', 'reports', 'player_pool_with_new_players_latest.md')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, age, nationality, introduction_season, introduction_event, created_at
        FROM players
        WHERE current_status = 'active'
        ORDER BY introduction_season, introduction_event, created_at
    ''')
    players = cursor.fetchall()
    conn.close()
    
    # Prepare markdown
    markdown = []
    markdown.append("# 🏌️ Full Player Pool (with New Players Highlighted)")
    markdown.append("")
    markdown.append(f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    markdown.append("")
    markdown.append(f"- **Total players:** {len(players)}")
    markdown.append(f"- **New players added:** {len(new_player_ids)}")
    markdown.append("")
    markdown.append("| # | Player | Age | Nationality | Season | Event | Status |")
    markdown.append("|---|--------|-----|-------------|--------|-------|--------|")
    for i, (pid, name, age, nat, season, event, created_at) in enumerate(players, 1):
        if pid in new_player_ids:
            status = "🆕 **NEW**"
        else:
            status = ""
        markdown.append(f"| {i} | {name} | {age} | {nat} | {season} | {event} | {status} |")
    # Nationality breakdown
    markdown.append("")
    markdown.append("## 🌍 Nationality Breakdown")
    from collections import Counter
    nat_counts = Counter([p[3] for p in players])
    for nat, count in nat_counts.most_common():
        markdown.append(f"- **{nat}:** {count}")
    # Age breakdown
    markdown.append("")
    markdown.append("## 🎂 Age Breakdown")
    age_counts = Counter([p[2] for p in players])
    for age, count in sorted(age_counts.items()):
        markdown.append(f"- **Age {age}:** {count}")
    # Write to file
    with open(output_path, 'w') as f:
        f.write('\n'.join(markdown))
    print(f"✅ Full player pool report saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate players for prehistory simulation.")
    parser.add_argument('--num', type=int, default=600, help='Number of players to generate (default: 600)')
    parser.add_argument('--age-min', type=int, default=19, help='Minimum age (default: 19)')
    parser.add_argument('--age-max', type=int, default=22, help='Maximum age (default: 22)')
    parser.add_argument('--season', type=int, default=0, help='Introduction season (default: 0 for Gauntlet)')
    parser.add_argument('--event', type=int, default=0, help='Introduction event (default: 0)')
    parser.add_argument('--suffix', type=str, default=None, help='Optional name suffix (e.g., S1)')
    args = parser.parse_args()

    generate_players(
        num_players=args.num,
        age_min=args.age_min,
        age_max=args.age_max,
        introduction_season=args.season,
        introduction_event=args.event,
        name_suffix=args.suffix
    )

if __name__ == "__main__":
    main() 