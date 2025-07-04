#!/usr/bin/env python3
"""
Calculate weather factors from raw weather data and update CSV file.
"""

import csv
import os
import tempfile
import shutil

def calculate_elevation_factor(elevation_str):
    """Convert elevation in feet to elevation_factor (0.0-1.0 scale)."""
    try:
        if elevation_str and elevation_str.strip() and elevation_str.strip() != "###":
            elevation_feet = float(elevation_str.strip())
            # Convert to 0-1 scale: elevation_factor = elevation_feet / 7724
            elevation_factor = elevation_feet / 7724.0
            # Clamp to 0-1 range
            return max(0.0, min(1.0, elevation_factor))
        else:
            return 0.3  # Default elevation factor
    except (ValueError, TypeError):
        return 0.3  # Default on error

def calculate_temp_factor(temp_values):
    """Calculate temperature factor from monthly average temperatures."""
    try:
        # Convert to float and filter out invalid values
        temps = [float(t) for t in temp_values if t and t.strip() and t.strip() != "###"]
        if not temps:
            return 0.5  # Default if no valid data
        
        avg_temp = sum(temps) / len(temps)
        # Normalize: 32°F = 0.0, 100°F = 1.0
        temp_factor = (avg_temp - 32) / 68.0
        return max(0.0, min(1.0, temp_factor))
    except (ValueError, TypeError):
        return 0.5

def calculate_humidity_factor(humidity_values):
    """Calculate humidity factor from monthly average humidity."""
    try:
        # Convert to float and filter out invalid values
        humidities = [float(h) for h in humidity_values if h and h.strip() and h.strip() != "###"]
        if not humidities:
            return 0.5  # Default if no valid data
        
        avg_humidity = sum(humidities) / len(humidities)
        # Direct percentage to 0-1 scale
        humidity_factor = avg_humidity / 100.0
        return max(0.0, min(1.0, humidity_factor))
    except (ValueError, TypeError):
        return 0.5

def calculate_wind_factor(wind_values):
    """Calculate wind factor from monthly average wind speeds."""
    try:
        # Convert to float and filter out invalid values
        winds = [float(w) for w in wind_values if w and w.strip() and w.strip() != "###"]
        if not winds:
            return 0.3  # Default if no valid data
        
        avg_wind = sum(winds) / len(winds)
        # Normalize: 0 mph = 0.0, 30+ mph = 1.0
        wind_factor = avg_wind / 30.0
        return max(0.0, min(1.0, wind_factor))
    except (ValueError, TypeError):
        return 0.3

def calculate_rain_factor(rain_values):
    """Calculate rain factor from monthly rain probabilities."""
    try:
        # Convert to float and filter out invalid values
        rains = [float(r) for r in rain_values if r and r.strip() and r.strip() != "###"]
        if not rains:
            return 0.2  # Default if no valid data
        
        avg_rain = sum(rains) / len(rains)
        # Direct percentage to 0-1 scale
        rain_factor = avg_rain / 100.0
        return max(0.0, min(1.0, rain_factor))
    except (ValueError, TypeError):
        return 0.2

def calculate_cloud_factor(cloud_values):
    """Calculate cloud factor from monthly average cloud cover."""
    try:
        # Convert to float and filter out invalid values
        clouds = [float(c) for c in cloud_values if c and c.strip() and c.strip() != "###"]
        if not clouds:
            return 0.5  # Default if no valid data
        
        avg_cloud = sum(clouds) / len(clouds)
        # Direct percentage to 0-1 scale
        cloud_factor = avg_cloud / 100.0
        return max(0.0, min(1.0, cloud_factor))
    except (ValueError, TypeError):
        return 0.5

def update_csv_with_weather_factors(csv_file_path):
    """Update CSV file with calculated weather factors."""
    
    # Create temporary file
    temp_file = csv_file_path + '.tmp'
    
    with open(csv_file_path, 'r') as infile, open(temp_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read header
        header = next(reader)
        writer.writerow(header)
        
        # Find column indices
        elevation_idx = header.index('elevation') if 'elevation' in header else None
        
        # Temperature columns (monthly averages)
        temp_cols = [i for i, col in enumerate(header) if 'temp_avg_' in col and len(col) == 11]  # temp_avg_jan, etc.
        
        # Humidity columns (monthly averages)
        humidity_cols = [i for i, col in enumerate(header) if 'humidity_avg_' in col and len(col) == 14]  # humidity_avg_jan, etc.
        
        # Wind columns (monthly averages)
        wind_cols = [i for i, col in enumerate(header) if 'wind_speed_avg_' in col and len(col) == 16]  # wind_speed_avg_jan, etc.
        
        # Rain columns (monthly probabilities)
        rain_cols = [i for i, col in enumerate(header) if 'rain_prop_' in col and len(col) == 12]  # rain_prop_jan, etc.
        
        # Cloud columns (monthly averages)
        cloud_cols = [i for i, col in enumerate(header) if 'cloud_cover_avg_' in col and len(col) == 18]  # cloud_cover_avg_jan, etc.
        
        # Factor columns to update
        factor_cols = {
            'elevation_factor': None,
            'temp_factor': None,
            'humidity_factor': None,
            'wind_factor': None,
            'rain_factor': None,
            'cloud_factor': None
        }
        
        # Find factor column indices
        for factor_name in factor_cols:
            try:
                factor_cols[factor_name] = header.index(factor_name)
            except ValueError:
                print(f"Warning: {factor_name} column not found")
        
        print(f"Processing {sum(1 for row in reader)} rows...")
        infile.seek(0)
        next(reader)  # Skip header again
        
        processed = 0
        for row in reader:
            # Calculate weather factors
            elevation_factor = calculate_elevation_factor(row[elevation_idx]) if elevation_idx is not None else 0.3
            
            temp_values = [row[i] for i in temp_cols if i < len(row)]
            temp_factor = calculate_temp_factor(temp_values)
            
            humidity_values = [row[i] for i in humidity_cols if i < len(row)]
            humidity_factor = calculate_humidity_factor(humidity_values)
            
            wind_values = [row[i] for i in wind_cols if i < len(row)]
            wind_factor = calculate_wind_factor(wind_values)
            
            rain_values = [row[i] for i in rain_cols if i < len(row)]
            rain_factor = calculate_rain_factor(rain_values)
            
            cloud_values = [row[i] for i in cloud_cols if i < len(row)]
            cloud_factor = calculate_cloud_factor(cloud_values)
            
            # Update factor values in row
            if factor_cols['elevation_factor'] is not None:
                row[factor_cols['elevation_factor']] = f"{elevation_factor:.3f}"
            if factor_cols['temp_factor'] is not None:
                row[factor_cols['temp_factor']] = f"{temp_factor:.3f}"
            if factor_cols['humidity_factor'] is not None:
                row[factor_cols['humidity_factor']] = f"{humidity_factor:.3f}"
            if factor_cols['wind_factor'] is not None:
                row[factor_cols['wind_factor']] = f"{wind_factor:.3f}"
            if factor_cols['rain_factor'] is not None:
                row[factor_cols['rain_factor']] = f"{rain_factor:.3f}"
            if factor_cols['cloud_factor'] is not None:
                row[factor_cols['cloud_factor']] = f"{cloud_factor:.3f}"
            
            writer.writerow(row)
            processed += 1
            
            if processed % 50 == 0:
                print(f"Processed {processed} rows...")
    
    # Replace original file with updated file
    shutil.move(temp_file, csv_file_path)
    print(f"✅ Updated {processed} rows with calculated weather factors")

if __name__ == "__main__":
    csv_file = "data/07.02.25_new_courses.csv"
    print("🌤️  Weather Factor Calculator")
    print("=" * 40)
    update_csv_with_weather_factors(csv_file) 