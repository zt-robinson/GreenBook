#!/usr/bin/env python3
"""
Export Players Sample to Markdown
Queries the first 20 players from the prehistory database and outputs their data as a markdown table.
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'prehistory.db')
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports', 'gauntlet_season', 'players_sample.md')

COLUMNS = [
    'id', 'name', 'age', 'nationality',
    'driving_power', 'driving_accuracy', 'approach_accuracy', 'short_game', 'putting',
    'composure', 'confidence', 'focus', 'risk_tolerance', 'mental_fatigue', 'consistency', 'resilience',
    'introduction_season', 'introduction_event'
]

HEADERS = [
    'ID', 'Name', 'Age', 'Nationality',
    'Driving Power', 'Driving Accuracy', 'Approach Accuracy', 'Short Game', 'Putting',
    'Composure', 'Confidence', 'Focus', 'Risk Tolerance', 'Mental Fatigue', 'Consistency', 'Resilience',
    'Intro Season', 'Intro Event'
]

def fetch_players(limit=20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT {', '.join(COLUMNS)} FROM players ORDER BY id ASC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def to_markdown_table(rows):
    lines = []
    # Header
    lines.append('| ' + ' | '.join(HEADERS) + ' |')
    lines.append('|' + '|'.join(['---'] * len(HEADERS)) + '|')
    # Rows
    for row in rows:
        lines.append('| ' + ' | '.join(str(x) for x in row) + ' |')
    return '\n'.join(lines)

def main():
    rows = fetch_players()
    md = to_markdown_table(rows)
    with open(OUTPUT_PATH, 'w') as f:
        f.write('# Sample of First 20 Players in Prehistory Database\n\n')
        f.write(md)
        f.write('\n')
    print(f"✅ Exported sample player data to {OUTPUT_PATH}")

if __name__ == "__main__":
    main() 