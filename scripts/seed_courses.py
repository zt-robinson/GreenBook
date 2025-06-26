#!/usr/bin/env python3
"""
Seed the golf_courses.db with course names and locations only.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'golf_courses.db')

courses = [
    ("Bathgate Golf Club", "Bathgate, Scotland (UK)"),
    ("Berkshire Country Club", "Mesa, AZ (US)"),
    ("Bramble Heath Golf Club", "Columbus, GA (US)"),
    ("Cape National", "Portland, ME (US)"),
    ("Cardinal Park Golf Club", "Rochester, MN (US)"),
    ("Cherry Highlands National", "San Francisco, CA (US)"),
    ("Cherry Hollow Golf Course", "Yonkers, NY (US)"),
    ("Coolidge Country Club", "Overland Park, KS (US)"),
    ("Dale Aspen Golf Club", "Albuquerque, NM (US)"),
    ("Deer Heath Golf Club", "Vancouver, BC (CAN)"),
    ("Emerson Country Club", "Charleston, SC (US)"),
    ("Fresno Country Club", "Fresno, CA (US)"),
    ("Grouse Meadow National", "Syracuse, NY (US)"),
    ("Heather Wood Resort", "Omaha, NE (US)"),
    ("Highlands Country Club", "Buffalo, NY (US)"),
    ("Jaén Golf Club", "Jaén, Spain"),
    ("Kilkenny Golf Club", "Kilkenny, Ireland"),
    ("Lake Amberwood Country Club", "Newcastle, New South Wales (AU)"),
    ("Larkspur Golf Club", "Houston, TX (US)"),
    ("Milton Keynes Golf Club (Championship)", "Milton Keynes, England (UK)"),
    ("Nelson Country Club", "Providence, RI (US)"),
    ("Nelson Park", "Salem, OR (US)"),
    ("Otter Cove Park", "Chicago, IL (US)"),
    ("Pheasant Valley Country Club", "Madison, WI (US)"),
    ("Royal Broxburn Golf Club", "Broxburn, Scotland (UK)"),
    ("Royal Rochdale Golf Club", "Rochdale, England (UK)"),
    ("Royal Telford Golf Club", "Telford, England (UK)"),
    ("Shizuoka Country Club", "Shizuoka, Japan"),
    ("Springfield Country Club", "Springfield, MA (US)"),
    ("Trout Fields Golf Club", "Seattle, WA (US)"),
    ("Vale Sycamore Country Club", "Huntsville, AL (US)"),
    ("Walnut Creek Country Club", "Aurora, CO (US)"),
    ("Woodlands Country Club", "Cheyenne, WY (US)")
]

def seed_courses():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for name, location in courses:
        cursor.execute(
            "INSERT INTO courses (name, location, total_par, total_yardage) VALUES (?, ?, ?, ?)",
            (name, location, 0, 0)
        )
    conn.commit()
    conn.close()
    print(f"Seeded {len(courses)} courses into {DB_PATH}")

if __name__ == "__main__":
    seed_courses() 