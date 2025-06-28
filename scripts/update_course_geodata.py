import sqlite3
import csv
import os

# Paths
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/golf_courses.db')
CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/course_geodata.csv')

def update_course_geodata(db_path, csv_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    updated = 0
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['course'].strip()
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            elev = float(row['elevation'])
            cur.execute(
                "UPDATE courses SET latitude = ?, longitude = ?, elevation = ? WHERE name = ?",
                (lat, lon, elev, name)
            )
            if cur.rowcount > 0:
                print(f"Updated: {name} ({lat}, {lon}, {elev})")
                updated += 1
            else:
                print(f"WARNING: No match for course name: {name}")
    conn.commit()
    conn.close()
    print(f"Done. Updated {updated} courses.")

if __name__ == "__main__":
    update_course_geodata(DB_PATH, CSV_PATH)