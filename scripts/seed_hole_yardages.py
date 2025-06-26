import sqlite3
import random

DB_PATH = 'golf_players.db'

# Par boundaries
par_ranges = {3: (100, 250), 4: (280, 503), 5: (504, 677)}
min_diff = 5
min_pct = 0.48
max_pct = 0.52
max_attempts = 1000

def valid_par_sequence(pars):
    if pars[0] == 3 or pars[1] == 3 or pars[17] == 3:
        return False
    for i in range(len(pars) - 2):
        trio = [pars[i], pars[i+1], pars[i+2]]
        if 4 not in trio:
            return False
        if all(p in (3, 5) for p in trio):
            return False
        if trio == [3, 5, 3] or trio == [5, 3, 5]:
            return False
    return True

def has_bad_consecutive_pars(pars):
    for i in range(len(pars) - 2):
        trio = [pars[i], pars[i+1], pars[i+2]]
        if all(p in (3, 5) for p in trio):
            return True
        if trio == [3, 5, 3] or trio == [5, 3, 5]:
            return True
    return False

def assign_nine_yardages_no_clump(holes, target_yardage, par_ranges, min_diff=5, max_attempts=1000):
    n = len(holes)
    pars = [h['par'] for h in holes]
    par_indices = {par: [i for i, h in enumerate(holes) if h['par'] == par] for par in par_ranges}
    par_counts = {par: len(par_indices[par]) for par in par_ranges}
    for attempt in range(max_attempts):
        yardages = [None] * n
        for par, count in par_counts.items():
            min_y, max_y = par_ranges[par]
            if count == 0:
                continue
            possible = list(range(min_y, max_y+1))
            random.shuffle(possible)
            group = []
            for y in possible:
                if len(group) == count:
                    break
                if all(abs(y - g) >= min_diff for g in group):
                    group.append(y)
            if len(group) < count:
                break
            random.shuffle(group)
            for idx, hole_idx in enumerate(par_indices[par]):
                yardages[hole_idx] = group[idx]
        if None in yardages:
            continue
        diff = target_yardage - sum(yardages)
        for adjust_attempt in range(200):
            if diff == 0:
                break
            idx = random.randint(0, n-1)
            par = holes[idx]['par']
            min_y, max_y = par_ranges[par]
            new_y = yardages[idx] + (1 if diff > 0 else -1)
            if (min_y <= new_y <= max_y and
                all(abs(new_y - yardages[j]) >= min_diff for j in range(n) if j != idx)):
                yardages[idx] = new_y
                diff += -1 if diff > 0 else 1
        if sum(yardages) == target_yardage:
            if not has_bad_consecutive_pars(pars):
                return yardages
    yardages = [None] * n
    for par, indices in par_indices.items():
        min_y, max_y = par_ranges[par]
        count = len(indices)
        if count == 0:
            continue
        step = max((max_y - min_y) // max(1, count-1), min_diff)
        group = [min_y + i*step for i in range(count)]
        random.shuffle(group)
        for idx, hole_idx in enumerate(indices):
            yardages[hole_idx] = group[idx]
    return yardages

def swap_to_balance_nines(front9_holes, back9_holes, min_pct, max_pct, total_yardage):
    for _ in range(100):
        f9 = sum(h['yardage'] for h in front9_holes)
        b9 = sum(h['yardage'] for h in back9_holes)
        f9_pct = f9 / total_yardage
        b9_pct = b9 / total_yardage
        if min_pct <= f9_pct <= max_pct and min_pct <= b9_pct <= max_pct:
            return
        for par in [5, 4, 3]:
            f9_candidates = sorted([h for h in front9_holes if h['par'] == par], key=lambda h: h['yardage'])
            b9_candidates = sorted([h for h in back9_holes if h['par'] == par], key=lambda h: h['yardage'], reverse=True)
            for f in f9_candidates:
                for b in b9_candidates:
                    f['yardage'], b['yardage'] = b['yardage'], f['yardage']
                    new_f9 = sum(h['yardage'] for h in front9_holes)
                    new_b9 = sum(h['yardage'] for h in back9_holes)
                    new_f9_pct = new_f9 / total_yardage
                    new_b9_pct = new_b9 / total_yardage
                    if min_pct <= new_f9_pct <= max_pct and min_pct <= new_b9_pct <= max_pct:
                        return
                    if abs(new_f9_pct - 0.5) + abs(new_b9_pct - 0.5) >= abs(f9_pct - 0.5) + abs(b9_pct - 0.5):
                        f['yardage'], b['yardage'] = b['yardage'], f['yardage']
    return

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT id FROM courses')
    course_ids = [row['id'] for row in cur.fetchall()]
    for course_id in course_ids:
        cur.execute('SELECT * FROM holes WHERE course_id = ? ORDER BY hole_number', (course_id,))
        holes = [dict(row) for row in cur.fetchall()]
        total_par = sum(h['par'] for h in holes)
        total_yardage = random.randint(total_par * 90, total_par * 110)  # Placeholder, replace with actual course yardage if available
        # If you have a course yardage column, use it:
        cur.execute('SELECT yardage FROM courses WHERE id = ?', (course_id,))
        row = cur.fetchone()
        if row and row['yardage']:
            total_yardage = row['yardage']
        pct = random.uniform(0.48, 0.52)
        front9_target = int(round(total_yardage * pct))
        back9_target = total_yardage - front9_target
        max_attempts = 1000
        for attempt in range(max_attempts):
            front9_holes = holes[:9]
            back9_holes = holes[9:]
            pars = [h['par'] for h in holes]
            if not valid_par_sequence(pars):
                random.shuffle(pars)
                for i, h in enumerate(holes):
                    h['par'] = pars[i]
                continue
            front9_yardages = assign_nine_yardages_no_clump(front9_holes, front9_target, par_ranges, min_diff)
            back9_yardages = assign_nine_yardages_no_clump(back9_holes, back9_target, par_ranges, min_diff)
            for i, h in enumerate(front9_holes):
                h['yardage'] = front9_yardages[i]
            for i, h in enumerate(back9_holes):
                h['yardage'] = back9_yardages[i]
            swap_to_balance_nines(front9_holes, back9_holes, min_pct, max_pct, total_yardage)
            f9 = sum(h['yardage'] for h in front9_holes)
            b9 = sum(h['yardage'] for h in back9_holes)
            f9_pct = f9 / total_yardage
            b9_pct = b9 / total_yardage
            if min_pct <= f9_pct <= max_pct and min_pct <= b9_pct <= max_pct:
                break
        # Save yardages to DB
        for h in holes:
            cur.execute('UPDATE holes SET yardage = ? WHERE id = ?', (h['yardage'], h['id']))
        print(f"Course {course_id}: yardages assigned and saved.")
    conn.commit()
    conn.close()
    print("All courses updated.")

if __name__ == '__main__':
    main() 