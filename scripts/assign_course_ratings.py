#!/usr/bin/env python3
import sqlite3
import os
import random

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

# Weights for course-specific factors
FACTOR_WEIGHTS = {
    'green_speed': 0.5,
    'hazard_density': 0.7,
    'narrowness_factor': 0.7,
    'terrain_difficulty': 0.4,
    'turf_firmness': 0.2,
    'elevation_factor': 0.2,
    'design_strategy': 0.3,
}

BASE = 68  # for par 72, 6500 yards
YARDAGE_DIVISOR = 150
RANDOM_RANGE = 0.3


def get_factor_value(row, colnames, factor):
    try:
        idx = colnames.index(factor)
        return float(row[idx]) if row[idx] is not None else 0.0
    except Exception:
        return 0.0

def assign_course_ratings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all courses and their characteristics
    cursor.execute('''
        SELECT c.id, c.name, c.total_par, c.total_yardage, cc.green_speed, cc.hazard_density, cc.narrowness_factor, cc.terrain_difficulty, cc.turf_firmness, cc.elevation_factor, cc.design_strategy
        FROM courses c
        JOIN course_characteristics cc ON c.id = cc.course_id
    ''')
    colnames = [desc[0] for desc in cursor.description]
    courses = cursor.fetchall()

    results = []

    for row in courses:
        course_id = row[0]
        name = row[1]
        par = row[2]
        yardage = row[3]
        # Calculate base rating
        base = BASE + (par - 72) + ((yardage - 6500) / YARDAGE_DIVISOR)
        # Weighted sum of factors
        factor_adj = 0.0
        for factor, weight in FACTOR_WEIGHTS.items():
            value = get_factor_value(row, colnames, factor)
            factor_adj += value * weight
        # Scale factor adjustment to max ±1.0
        factor_adj = (factor_adj - 2.0) * 1.0  # 2.0 is a rough mid value for these weights
        # Add random adjustment
        rand_adj = random.uniform(-RANDOM_RANGE, RANDOM_RANGE)
        course_rating = round(base + factor_adj + rand_adj, 1)
        # Update DB
        cursor.execute('UPDATE courses SET course_rating = ? WHERE id = ?', (course_rating, course_id))
        results.append((name, course_rating, base, factor_adj, rand_adj))

    conn.commit()
    conn.close()

    # Show the full list of results
    print("Full course ratings:")
    for r in results:
        print(f"{r[0]}: {r[1]} (base={r[2]:.2f}, factor_adj={r[3]:.2f}, rand={r[4]:+.2f})")

if __name__ == "__main__":
    assign_course_ratings() 