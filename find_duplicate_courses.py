import csv
from collections import Counter

with open('greenbook/data/07.02.25_new_courses.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    names = [row[0].strip() for row in reader]
    counts = Counter(names)
    dups = [name for name, count in counts.items() if count > 1]
    print(f'Duplicate course names ({len(dups)}):')
    for name in dups:
        print(name) 