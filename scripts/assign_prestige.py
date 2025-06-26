#!/usr/bin/env python3
import sqlite3
import os
import re

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

NAME_PATTERNS = [
    (re.compile(r"royal|national|championship", re.I), 0.5),
    (re.compile(r"country club|resort", re.I), 0.3),
]
DEFAULT_BASE = 0.1

SLOPE_MIN = 135
SLOPE_MAX = 155
SLOPE_BONUS_SCALE = 0.5

def assign_prestige():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, slope_rating FROM courses')
    courses = cursor.fetchall()
    results = []
    for course_id, name, slope in courses:
        # Name-based base
        base = DEFAULT_BASE
        for pattern, score in NAME_PATTERNS:
            if pattern.search(name):
                base = score
                break
        # Slope bonus
        slope_bonus = 0.0
        if slope and slope > SLOPE_MIN:
            slope_bonus = ((min(slope, SLOPE_MAX) - SLOPE_MIN) / (SLOPE_MAX - SLOPE_MIN)) * SLOPE_BONUS_SCALE
        prestige = min(1.0, base + slope_bonus)
        cursor.execute('UPDATE courses SET prestige_level = ? WHERE id = ?', (prestige, course_id))
        results.append((name, prestige, base, slope, slope_bonus))
    conn.commit()
    conn.close()
    print("Full prestige values:")
    for r in results:
        print(f"{r[0]}: Prestige={r[1]:.2f} (base={r[2]:.2f}, slope={r[3]}, bonus={r[4]:.2f})")

if __name__ == "__main__":
    assign_prestige() 