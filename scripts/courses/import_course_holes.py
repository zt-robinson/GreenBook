#!/usr/bin/env python3
import sqlite3
import os
import csv
import sys

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')
CSV_PATH = os.path.join(os.path.dirname(__file__), 'all_course_holes.csv')

def import_holes(target_course=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Build a mapping from course name to id
    cursor.execute('SELECT id, name FROM courses')
    course_map = {name: cid for cid, name in cursor.fetchall()}
    # If targeting a specific course, clear only its holes
    if target_course:
        course_id = course_map.get(target_course)
        if course_id:
            cursor.execute('DELETE FROM holes WHERE course_id = ?', (course_id,))
        else:
            print(f"Course not found: {target_course}")
            conn.close()
            return
    # Otherwise, clear all holes
    else:
        cursor.execute('DELETE FROM holes')
    # Read CSV and insert (no header)
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            course_name = row[0].strip('"')
            if target_course and course_name != target_course:
                continue
            course_id = course_map.get(course_name)
            if not course_id:
                if not target_course:
                    print(f"Course not found: {course_name}")
                continue
            hole_number = int(row[1])
            par = int(row[2])
            yardage = int(row[3])
            cursor.execute(
                'INSERT INTO holes (course_id, hole_number, par, yardage, handicap, difficulty_modifier) VALUES (?, ?, ?, ?, 0, 1.0)',
                (course_id, hole_number, par, yardage)
            )
    conn.commit()
    conn.close()
    if target_course:
        print(f"Imported holes for {target_course} from CSV.")
    else:
        print("Imported all holes from CSV and overwrote existing data.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        import_holes(sys.argv[1])
    else:
        import_holes() 