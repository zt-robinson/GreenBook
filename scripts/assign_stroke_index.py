#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

# Difficulty formula: yardage + 40*par

def assign_stroke_index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM courses')
    courses = cursor.fetchall()
    for course_id, course_name in courses:
        # Get holes for this course
        cursor.execute('SELECT id, hole_number, par, yardage FROM holes WHERE course_id = ?', (course_id,))
        holes = cursor.fetchall()
        if len(holes) != 18:
            print(f"Skipping {course_name}: not 18 holes")
            continue
        # Calculate difficulty for each hole
        hole_difficulties = []
        for h in holes:
            hid, hnum, par, yard = h
            difficulty = (yard or 0) + 40 * (par or 0)
            hole_difficulties.append({'id': hid, 'hole_number': hnum, 'difficulty': difficulty})
        # Split into front and back nine
        front = [h for h in hole_difficulties if 1 <= h['hole_number'] <= 9]
        back = [h for h in hole_difficulties if 10 <= h['hole_number'] <= 18]
        front_total = sum(h['difficulty'] for h in front)
        back_total = sum(h['difficulty'] for h in back)
        # Decide which nine is harder
        if front_total >= back_total:
            odd_nine, even_nine = front, back
            odd_label, even_label = 'front', 'back'
        else:
            odd_nine, even_nine = back, front
            odd_label, even_label = 'back', 'front'
        # Assign odd stroke indexes to harder nine
        odd_nine_sorted = sorted(odd_nine, key=lambda h: -h['difficulty'])
        even_nine_sorted = sorted(even_nine, key=lambda h: -h['difficulty'])
        # Assign indexes
        for i, h in enumerate(odd_nine_sorted):
            stroke_index = 1 + 2 * i  # 1, 3, 5, ... 17
            cursor.execute('UPDATE holes SET handicap = ? WHERE id = ?', (stroke_index, h['id']))
        for i, h in enumerate(even_nine_sorted):
            stroke_index = 2 + 2 * i  # 2, 4, 6, ... 18
            cursor.execute('UPDATE holes SET handicap = ? WHERE id = ?', (stroke_index, h['id']))
        print(f"{course_name}: {odd_label} nine gets odd indexes, {even_label} gets even.")
    conn.commit()
    conn.close()
    print("Stroke index assignment complete.")

if __name__ == "__main__":
    assign_stroke_index() 