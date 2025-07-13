#!/usr/bin/env python3
"""
Age Up Players Script for GreenBook Prehistory

Increments the age of all players (active and inactive) by 1 year in the prehistory database.
"""
import sqlite3
import os

def age_up_players():
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'prehistory.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE players SET age = age + 1")
        conn.commit()
        print("✅ All players have been aged up by 1 year.")
    except Exception as e:
        print(f"❌ Error aging up players: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    age_up_players() 