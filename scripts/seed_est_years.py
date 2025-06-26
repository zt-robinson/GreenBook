#!/usr/bin/env python3
import sqlite3
import os
import random

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

def seed_est_years():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM courses')
    for (course_id,) in cursor.fetchall():
        est_year = random.randint(1890, 2010)
        cursor.execute('UPDATE courses SET est_year = ? WHERE id = ?', (est_year, course_id))
    conn.commit()
    conn.close()
    print("Randomly assigned est_years to all courses.")

if __name__ == "__main__":
    seed_est_years() 