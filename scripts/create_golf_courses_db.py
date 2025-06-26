#!/usr/bin/env python3
"""
Script to create a new golf_courses.db SQLite database with the finalized schema for golf courses, characteristics, and holes.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

def create_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Courses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            city TEXT,
            state_country TEXT,
            location TEXT,
            total_par INTEGER NOT NULL,
            total_yardage INTEGER NOT NULL,
            slope_rating REAL,
            course_rating REAL,
            prestige_level INTEGER,
            est_year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Course characteristics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course_characteristics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            avg_temperature REAL,
            humidity_level REAL,
            wind_factor REAL,
            rain_probability REAL,
            design_strategy REAL,
            narrowness_factor REAL,
            hazard_density REAL,
            green_speed REAL,
            turf_firmness REAL,
            rough_length REAL,
            course_age REAL,
            crowd_factor REAL,
            elevation_factor REAL,
            terrain_difficulty REAL,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            UNIQUE(course_id)
        )
    ''')

    # Holes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS holes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            hole_number INTEGER NOT NULL,
            par INTEGER NOT NULL,
            yardage INTEGER NOT NULL,
            handicap INTEGER,
            difficulty_modifier REAL,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            UNIQUE(course_id, hole_number)
        )
    ''')

    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH} with the finalized schema.")

if __name__ == "__main__":
    create_schema() 