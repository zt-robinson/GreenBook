import os
import glob
import csv
import sqlite3

# Paths
EVENT_HISTORY_DIR = os.path.join(os.path.dirname(__file__), '..', 'prehistory', 'event_history')
PLAYER_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_players.db')

# 1. Count wins and top-10s for each player by name
win_counts = {}
top10_counts = {}
for csv_file in glob.glob(os.path.join(EVENT_HISTORY_DIR, '*.csv')):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Count win
            winner = row.get('first_place')
            if winner:
                win_counts[winner] = win_counts.get(winner, 0) + 1
            # Count top 10s
            for i in range(1, 11):
                key = [
                    'first_place', 'second_place', 'third_place', 'fourth_place', 'fifth_place',
                    'sixth_place', 'seventh_place', 'eighth_place', 'ninth_place', 'tenth_place'
                ][i-1]
                name = row.get(key)
                if name:
                    top10_counts[name] = top10_counts.get(name, 0) + 1

# 2. Connect to the player database
conn = sqlite3.connect(PLAYER_DB_PATH)
cursor = conn.cursor()

# 3. Update each player's career_wins and top_10s fields
updated = 0
for name in set(list(win_counts.keys()) + list(top10_counts.keys())):
    wins = win_counts.get(name, 0)
    top10s = top10_counts.get(name, 0)
    cursor.execute("UPDATE players SET career_wins = ?, top_10s = ? WHERE name = ?", (wins, top10s, name))
    if cursor.rowcount > 0:
        updated += 1

conn.commit()
conn.close()

print(f"Updated career_wins and top_10s for {updated} players.") 