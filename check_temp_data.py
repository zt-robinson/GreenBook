#!/usr/bin/env python3
import csv

with open('data/07.02.25_new_courses.csv', 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    
    # Find temperature columns
    temp_cols = [i for i, col in enumerate(header) if 'temp_avg' in col]
    print(f"Found {len(temp_cols)} temperature columns:")
    for i in temp_cols:
        print(f"  {i}: {header[i]}")
    
    print("\nTemperature data for first 3 courses:")
    
    for course_num in range(3):
        try:
            data_row = next(reader)
            print(f"\nCourse {course_num + 1}:")
            for j, col_idx in enumerate(temp_cols):
                if j < 12:  # Only show first 12 months
                    print(f"  {header[col_idx]}: {data_row[col_idx]}°F")
        except StopIteration:
            break 