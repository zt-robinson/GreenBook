#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

def update_course_totals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Get all courses
    cursor.execute('SELECT id, name FROM courses')
    courses = cursor.fetchall()
    updated = 0
    for course_id, name in courses:
        # Sum par and yardage from holes
        cursor.execute('SELECT SUM(par), SUM(yardage) FROM holes WHERE course_id = ?', (course_id,))
        par_sum, yardage_sum = cursor.fetchone()
        if par_sum and yardage_sum:
            cursor.execute('UPDATE courses SET total_par = ?, total_yardage = ? WHERE id = ?', (par_sum, yardage_sum, course_id))
            updated += 1
            print(f"Updated {name}: par={par_sum}, yardage={yardage_sum}")
        else:
            print(f"No hole data for {name}, skipping.")
    conn.commit()
    conn.close()
    print(f"\nUpdated totals for {updated} courses.")

if __name__ == "__main__":
    update_course_totals() 