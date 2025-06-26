#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

# Weights for bogey golfer difficulty (higher than for course rating)
BOGEY_WEIGHTS = {
    'hazard_density': 1.3,
    'narrowness_factor': 1.3,
    'green_speed': 0.9,
    'terrain_difficulty': 0.75,
    'turf_firmness': 0.45,
    'elevation_factor': 0.35,
    'design_strategy': 0.6,
}

BOGEY_BASE = 24.0  # Reduced from 27.0
SLOPE_MULTIPLIER = 5.381
SLOPE_MIN = 55
SLOPE_MAX = 155


def get_factor_value(row, colnames, factor):
    try:
        idx = colnames.index(factor)
        return float(row[idx]) if row[idx] is not None else 0.0
    except Exception:
        return 0.0

def assign_slope_ratings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all courses and their characteristics
    cursor.execute('''
        SELECT c.id, c.name, c.course_rating, cc.hazard_density, cc.narrowness_factor, cc.green_speed, cc.terrain_difficulty, cc.turf_firmness, cc.elevation_factor, cc.design_strategy
        FROM courses c
        JOIN course_characteristics cc ON c.id = cc.course_id
    ''')
    colnames = [desc[0] for desc in cursor.description]
    courses = cursor.fetchall()

    results = []

    for row in courses:
        course_id = row[0]
        name = row[1]
        course_rating = row[2]
        # Weighted sum of difficulty factors
        diff_adj = 0.0
        for factor, weight in BOGEY_WEIGHTS.items():
            value = get_factor_value(row, colnames, factor)
            diff_adj += value * weight
        # Estimate bogey rating
        bogey_rating = course_rating + BOGEY_BASE + diff_adj
        # Calculate slope rating
        slope_rating = SLOPE_MULTIPLIER * (bogey_rating - course_rating)
        slope_rating = max(SLOPE_MIN, min(SLOPE_MAX, round(slope_rating)))
        # Update DB
        cursor.execute('UPDATE courses SET slope_rating = ? WHERE id = ?', (slope_rating, course_id))
        results.append((name, slope_rating, course_rating, bogey_rating, diff_adj))

    conn.commit()
    conn.close()

    # Show a sample of 5 results
    print("Sample slope ratings:")
    for r in results[:5]:
        print(f"{r[0]}: Slope={r[1]}, Course Rating={r[2]}, Bogey Rating={r[3]:.2f}, Diff Adj={r[4]:.2f}")

if __name__ == "__main__":
    assign_slope_ratings() 