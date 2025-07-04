#!/usr/bin/env python3
import csv

def check_data_quality():
    with open('data/07.02.25_new_courses.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        
        # Find key columns
        elevation_idx = header.index('elevation') if 'elevation' in header else None
        temp_cols = [i for i, col in enumerate(header) if 'temp_avg' in col]
        rain_cols = [i for i, col in enumerate(header) if 'rain_prop' in col]
        humidity_cols = [i for i, col in enumerate(header) if 'humidity_avg' in col]
        
        print("=== DATA QUALITY CHECK ===")
        print(f"Total rows: {sum(1 for row in reader)}")
        file.seek(0)
        next(reader)  # Skip header again
        
        print(f"\nElevation column: {'Found' if elevation_idx else 'NOT FOUND'}")
        print(f"Temperature columns: {len(temp_cols)} found")
        print(f"Rain probability columns: {len(rain_cols)} found")
        print(f"Humidity columns: {len(humidity_cols)} found")
        
        # Check first 5 courses
        print("\n=== SAMPLE DATA (First 5 courses) ===")
        
        for course_num in range(5):
            try:
                data_row = next(reader)
                print(f"\nCourse {course_num + 1}:")
                
                if elevation_idx:
                    elevation = data_row[elevation_idx]
                    print(f"  Elevation: {elevation} ft")
                
                # Show temperature range
                temps = [float(data_row[i]) for i in temp_cols[:12] if data_row[i] and data_row[i].strip()]
                if temps:
                    print(f"  Temperature range: {min(temps):.1f}°F - {max(temps):.1f}°F")
                
                # Show rain probabilities
                rains = [float(data_row[i]) for i in rain_cols[:12] if data_row[i] and data_row[i].strip()]
                if rains:
                    print(f"  Rain probability range: {min(rains):.1f}% - {max(rains):.1f}%")
                
                # Show humidity
                humidities = [float(data_row[i]) for i in humidity_cols[:12] if data_row[i] and data_row[i].strip()]
                if humidities:
                    print(f"  Humidity range: {min(humidities):.1f}% - {max(humidities):.1f}%")
                    
            except StopIteration:
                break
            except ValueError as e:
                print(f"  Error parsing data: {e}")

if __name__ == "__main__":
    check_data_quality() 