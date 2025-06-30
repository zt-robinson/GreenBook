#!/usr/bin/env python3
"""
Migrate the tournaments table to add new event variables and fix data types.
"""
import sqlite3
import os
import json

def migrate_tournaments_table():
    db_path = os.path.join(os.path.dirname(__file__), '../data/golf_tournaments.db')
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        # 1. Add new columns if they don't exist
        cur.execute("PRAGMA table_info(tournaments)")
        columns = [row[1] for row in cur.fetchall()]
        if 'prestige' not in columns:
            cur.execute('ALTER TABLE tournaments ADD COLUMN prestige REAL')
            print("✅ Added prestige column (0-1 float)")
        if 'cut_line_value' not in columns:
            cur.execute('ALTER TABLE tournaments ADD COLUMN cut_line_value INTEGER')
            print("✅ Added cut_line_value column (int)")
        if 'cut_line_type' not in columns:
            cur.execute('ALTER TABLE tournaments ADD COLUMN cut_line_type TEXT')
            print("✅ Added cut_line_type column (text)")
        if 'points_to_winner' not in columns:
            cur.execute('ALTER TABLE tournaments ADD COLUMN points_to_winner INTEGER')
            print("✅ Added points_to_winner column (int)")
        if 'event_config_json' not in columns:
            cur.execute('ALTER TABLE tournaments ADD COLUMN event_config_json TEXT')
            print("✅ Added event_config_json column (text)")
        conn.commit()
        # 2. Migrate prestige_level to prestige (0-1 scale)
        if 'prestige_level' in columns:
            cur.execute('SELECT id, prestige_level FROM tournaments')
            for row in cur.fetchall():
                tid, prestige_level = row
                # If prestige_level is > 1, assume it's on a 1-10 scale and convert
                if prestige_level is not None:
                    prestige = float(prestige_level)
                    if prestige > 1.0:
                        prestige = round(prestige / 10.0, 3)
                    cur.execute('UPDATE tournaments SET prestige = ? WHERE id = ?', (prestige, tid))
            print("✅ Migrated prestige_level to prestige (0-1 scale)")
        conn.commit()
        # 3. Migrate cutline to cut_line_value/cut_line_type
        if 'cutline' in columns:
            cur.execute('SELECT id, cutline FROM tournaments')
            for row in cur.fetchall():
                tid, cutline = row
                if cutline is None:
                    continue
                cutline_str = str(cutline).strip().lower()
                if cutline_str in ('none', 'no cut', ''):
                    cut_line_type = 'none'
                    cut_line_value = None
                else:
                    # Try to extract a number
                    import re
                    m = re.search(r'(\d+)', cutline_str)
                    cut_line_value = int(m.group(1)) if m else None
                    cut_line_type = 'position' if cut_line_value else None
                cur.execute('UPDATE tournaments SET cut_line_value = ?, cut_line_type = ? WHERE id = ?', (cut_line_value, cut_line_type, tid))
            print("✅ Migrated cutline to cut_line_value/cut_line_type")
        conn.commit()
        # 4. Drop old columns (prestige_level, cutline) if desired (SQLite doesn't support DROP COLUMN directly)
        #    (Optional: leave them for now, or do a full table rebuild if you want to remove them)
        print("⚠️  Old columns prestige_level and cutline are still present (SQLite limitation)")
        print("✅ Migration complete!")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_tournaments_table() 