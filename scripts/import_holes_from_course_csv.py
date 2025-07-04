#!/usr/bin/env python3
"""
Import hole data from the main course CSV (07.02.25_new_courses.csv) and insert into the holes table.
"""
import sqlite3
import os
import csv

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'golf_courses.db')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', '07.02.25_new_courses.csv')

# Hole data columns (0-based):
# course_name, location, [h1_par, h1_yards, h1_hcp, ..., h9_par, h9_yards, h9_hcp], OUT_par, OUT_yards,
# [h10_par, h10_yards, h10_hcp, ..., h18_par, h18_yards, h18_hcp], IN_par, IN_yards, total_par, total_yards, ...

FRONT9_START = 2
BACK9_START = 31


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Build a mapping from course name to id (name only)
    cursor.execute('SELECT id, name FROM courses')
    course_map = {name.strip(): cid for cid, name in cursor.fetchall()}

    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        inserted = 0
        skipped = 0
        for row in reader:
            course_name = row[0].strip()
            course_id = course_map.get(course_name)
            if not course_id:
                print(f"Course not found in DB: {course_name}")
                skipped += 1
                continue
            # Delete existing holes for this course
            cursor.execute('DELETE FROM holes WHERE course_id = ?', (course_id,))
            # Insert holes 1-9
            for i in range(9):
                base = FRONT9_START + i * 3
                par = int(row[base])
                yardage = int(row[base + 1])
                handicap = int(row[base + 2])
                cursor.execute(
                    'INSERT INTO holes (course_id, hole_number, par, yardage, handicap, difficulty_modifier) VALUES (?, ?, ?, ?, ?, 1.0)',
                    (course_id, i + 1, par, yardage, handicap)
                )
            # Insert holes 10-18
            for i in range(9):
                base = BACK9_START + i * 3
                par = int(row[base])
                yardage = int(row[base + 1])
                handicap = int(row[base + 2])
                cursor.execute(
                    'INSERT INTO holes (course_id, hole_number, par, yardage, handicap, difficulty_modifier) VALUES (?, ?, ?, ?, ?, 1.0)',
                    (course_id, i + 10, par, yardage, handicap)
                )
            inserted += 1
        conn.commit()
    conn.close()
    print(f"✅ Inserted holes for {inserted} courses. Skipped {skipped}.")

if __name__ == "__main__":
    main() 