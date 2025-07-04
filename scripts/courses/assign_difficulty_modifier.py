#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')
ALPHA = 0.5

def assign_difficulty_modifier():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM courses')
    courses = cursor.fetchall()
    for course_id, course_name in courses:
        cursor.execute('SELECT id, par, yardage FROM holes WHERE course_id = ?', (course_id,))
        holes = cursor.fetchall()
        if not holes:
            continue
        # Calculate difficulty for each hole
        hole_difficulties = []
        for h in holes:
            hid, par, yard = h
            difficulty = (yard or 0) + 40 * (par or 0)
            hole_difficulties.append({'id': hid, 'difficulty': difficulty})
        avg_difficulty = sum(h['difficulty'] for h in hole_difficulties) / len(hole_difficulties)
        # Assign modifier
        for h in hole_difficulties:
            rel = (h['difficulty'] - avg_difficulty) / avg_difficulty
            modifier = round(1.0 + ALPHA * rel, 3)
            cursor.execute('UPDATE holes SET difficulty_modifier = ? WHERE id = ?', (modifier, h['id']))
        # Print a sample for the first course
        if course_id == courses[0][0]:
            print(f"Sample for {course_name}:")
            for i, h in enumerate(hole_difficulties):
                print(f"Hole {i+1}: difficulty={h['difficulty']}, modifier={round(1.0 + ALPHA * ((h['difficulty'] - avg_difficulty) / avg_difficulty), 3)}")
    conn.commit()
    conn.close()
    print("Difficulty modifier assignment complete.")

if __name__ == "__main__":
    assign_difficulty_modifier() 