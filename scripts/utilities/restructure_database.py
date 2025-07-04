#!/usr/bin/env python3
"""
Golf Course Database Restructuring Script
Creates a clean, well-structured database for golf courses with proper relationships.
"""

import sqlite3
import os
import math

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_players.db')
BACKUP_PATH = os.path.join(os.path.dirname(__file__), 'golf_players_backup.db')

def backup_database():
    """Create a backup of the current database."""
    import shutil
    shutil.copy2(DB_PATH, BACKUP_PATH)
    print(f"Database backed up to {BACKUP_PATH}")

def create_clean_schema():
    """Create a clean, well-structured database schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # First, read all existing data before dropping tables
    cursor.execute('''
        SELECT id, name, city, state_country, location, yardage, par, prestige, est_year
        FROM courses
    ''')
    old_courses = cursor.fetchall()
    
    cursor.execute('SELECT * FROM course_characteristics')
    old_characteristics = cursor.fetchall()
    
    cursor.execute('SELECT * FROM holes')
    old_holes = cursor.fetchall()
    
    # Now drop existing tables
    cursor.execute("DROP TABLE IF EXISTS holes")
    cursor.execute("DROP TABLE IF EXISTS course_characteristics")
    cursor.execute("DROP TABLE IF EXISTS courses")
    
    # Create clean courses table
    cursor.execute('''
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            city TEXT,
            state_country TEXT,
            location TEXT,
            total_par INTEGER NOT NULL,
            total_yardage INTEGER NOT NULL,
            slope_rating INTEGER,
            course_rating REAL,
            prestige_level INTEGER DEFAULT 50,
            est_year INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create clean course_characteristics table
    cursor.execute('''
        CREATE TABLE course_characteristics (
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
    
    # Create clean holes table
    cursor.execute('''
        CREATE TABLE holes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER NOT NULL,
            hole_number INTEGER NOT NULL,
            par INTEGER NOT NULL,
            yardage INTEGER NOT NULL,
            handicap INTEGER,
            difficulty_modifier REAL DEFAULT 1.0,
            FOREIGN KEY(course_id) REFERENCES courses(id),
            UNIQUE(course_id, hole_number)
        )
    ''')
    
    # Insert courses into new structure
    for course in old_courses:
        cursor.execute('''
            INSERT INTO courses (id, name, city, state_country, location, total_par, total_yardage, prestige_level, est_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (course[0], course[1], course[2], course[3], course[4], course[6], course[5], course[7], course[8]))
    
    # Insert characteristics into new structure
    for char in old_characteristics:
        cursor.execute('''
            INSERT INTO course_characteristics (
                course_id, avg_temperature, humidity_level, wind_factor, rain_probability,
                design_strategy, narrowness_factor, hazard_density, green_speed,
                turf_firmness, rough_length, course_age, crowd_factor,
                elevation_factor, terrain_difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (char[0], char[1], char[2], char[3], char[4], char[5], char[7], char[8], char[9], char[10], char[11], char[13], char[14], char[15], char[16]))
    
    # Insert holes into new structure
    for hole in old_holes:
        cursor.execute('''
            INSERT INTO holes (course_id, hole_number, par, yardage, handicap, difficulty_modifier)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (hole[1], hole[2], hole[3], hole[6], hole[5], hole[4]))
    
    conn.commit()
    conn.close()
    print("Clean database schema created and data migrated")

def migrate_existing_data():
    """This function is now handled in create_clean_schema()"""
    pass

def calculate_course_ratings():
    """Calculate slope rating and course rating for each course."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM courses')
    course_ids = cursor.fetchall()
    
    for (course_id,) in course_ids:
        # Get hole data for this course
        cursor.execute('''
            SELECT par, yardage, handicap, difficulty_modifier 
            FROM holes 
            WHERE course_id = ? 
            ORDER BY hole_number
        ''', (course_id,))
        holes = cursor.fetchall()
        
        if len(holes) == 18:  # Only calculate for complete courses
            # Calculate course rating (simplified formula)
            total_yardage = sum(hole[1] for hole in holes)
            total_par = sum(hole[0] for hole in holes)
            
            # Basic course rating calculation
            # This is a simplified version - real USGA ratings are more complex
            course_rating = 71.0 + (total_yardage - 7100) / 100.0
            
            # Basic slope rating calculation
            # This is a simplified version - real slope ratings are more complex
            difficulty_factor = sum(hole[3] for hole in holes) / 18.0  # average difficulty modifier
            slope_rating = int(113 + (difficulty_factor - 1.0) * 50)
            
            # Update the course
            cursor.execute('''
                UPDATE courses 
                SET course_rating = ?, slope_rating = ?
                WHERE id = ?
            ''', (round(course_rating, 1), slope_rating, course_id))
    
    conn.commit()
    conn.close()
    print("Course ratings calculated")

def verify_database():
    """Verify the database structure and data integrity."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check course count
    cursor.execute('SELECT COUNT(*) FROM courses')
    course_count = cursor.fetchone()[0]
    print(f"Total courses: {course_count}")
    
    # Check holes per course
    cursor.execute('''
        SELECT c.name, COUNT(h.id) as hole_count, c.total_par, c.total_yardage
        FROM courses c
        LEFT JOIN holes h ON c.id = h.course_id
        GROUP BY c.id
        ORDER BY c.name
    ''')
    courses = cursor.fetchall()
    
    print("\nCourse Summary:")
    for course in courses:
        print(f"  {course[0]}: {course[1]} holes, Par {course[2]}, {course[3]} yards")
    
    # Check for courses with characteristics
    cursor.execute('SELECT COUNT(*) FROM course_characteristics')
    char_count = cursor.fetchone()[0]
    print(f"\nCourses with characteristics: {char_count}")
    
    conn.close()

def main():
    """Main function to restructure the database."""
    print("Golf Course Database Restructuring")
    print("=" * 40)
    
    # Create backup
    backup_database()
    
    # Create new schema
    create_clean_schema()
    
    # Migrate data
    migrate_existing_data()
    
    # Calculate ratings
    calculate_course_ratings()
    
    # Verify results
    verify_database()
    
    print("\nDatabase restructuring completed successfully!")

if __name__ == "__main__":
    main() 