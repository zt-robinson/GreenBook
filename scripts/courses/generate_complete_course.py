#!/usr/bin/env python3
"""
Complete Course Generation Script
Generates courses with all components:
- Course naming (PCC, Location-based, Family-based)
- Hole generation with par distribution and placement rules
- Yardage generation with constraints
- Handicap stroke index generation (evens/odds method)
- Hole difficulty calculation (stroke index + yardage relative to par)
- Course factors with weather integration and prestige correlations
"""

import random
import pandas as pd
import os
import numpy as np
import sqlite3
from datetime import datetime

# Data paths
CITIES_DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/cities_with_elevation.csv')
DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/golf_courses.db')

# Family names and naming conventions
FAMILY_NAMES = {
    'old_money': [
        'Adams', 'Livingston', 'Cabot', 'Lowell', 'Winthrop', 'Parkman', 'Schuyler', 'Bayard', 
        'Rensselaer', 'Morris', 'Custis', 'Gerry', 'Harrison', 'Calvert', 'Rockefeller', 
        'Vanderbilt', 'Carnegie', 'Morgan', 'Du Pont', 'Mellon', 'Ford', 'Astor', 'Hearst', 
        'Walton', 'Koch', 'Pew', 'Sloan', 'Bloomberg', 'Gould', 'Harriman', 'Hill', 'Pullman', 
        'Stanford', 'Whitney', 'Woolworth', 'Wrigley', 'Kellogg', 'Heinz', 'Hershey', 'Mars', 
        'Johnson', 'Procter', 'Gamble', 'Swift', 'Armour', 'McCormick', 'Deere', 'Boeing', 
        'Hughes', 'Getty', 'Bass'
    ],
    'early_american': [
        'Beekman', 'Blaine', 'Breckinridge', 'Carroll', 'Choate', 'Clay', 'Fish', 'Griswold', 
        'Hancock', 'Jay', 'Lee', 'Lodge', 'Madison', 'Pinckney', 'Randolph', 'Roosevelt', 
        'Van Buren', 'Appleton', 'Biddle', 'Bowdoin', 'Bradford', 'Brinckerhoff', 'Chauncey', 
        'Crowninshield', 'Dana', 'De Lancey', 'Delafield', 'Dwight', 'Eliot', 'Endicott', 
        'Fiske', 'Gallatin', 'Gardiner', 'Goodhue', 'Grinnell', 'Hallingwell', 'Huntington', 
        'Lawrence', 'Ledyard', 'McLane', 'Ogden', 'Perkins', 'Quincy', 'Ruggles', 'Sedgwick', 
        'Strong', 'Wadsworth', 'Forbes', 'Gardner', 'Otis', 'Peabody', 'Saltonstall', 
        'Sargent', 'Storrow', 'Alden', 'Allerton', 'Billington', 'Brewster', 'Browne', 
        'Carver', 'Chilton', 'Cooke', 'Doty', 'Eaton', 'Fuller', 'Hopkins', 'Howland', 
        'Mullins', 'Priest', 'Rogers', 'Soule', 'Standish', 'Tilley', 'Warren', 'White', 
        'Williams', 'Winslow'
    ]
}

GEOGRAPHIC_TERMS = [
    'Vale', 'Valley', 'Park', 'Woods', 'Fields', 'Trace', 'Heath', 'Prairie', 'Glen', 
    'Meadows', 'Marsh', 'Ridge', 'Hollow', 'Creek', 'Hills', 'Willows', 'Hall', 'Manor', 
    'Estate', 'Springs', 'Bluff', 'Point', 'Landing', 'Grove', 'Chase', 'Commons', 'Terrace'
]

CLUB_SUFFIXES = [
    'Country Club', 'Golf Club', 'Hunt Club', 'Golf & Country Club', 'Cricket Club', 
    'Athletic Club', 'Club', 'National Golf Club', 'Golf & Hunt Club', 'Golf & Tennis Club', 
    'Polo Club', 'Hunt & Country Club'
]

NORTHEAST_STATES = ['ME', 'NH', 'VT', 'MA', 'RI', 'CT', 'NY', 'NJ', 'PA']
SOUTHERN_STATES = ['MD', 'DE', 'VA', 'WV', 'KY', 'TN', 'NC', 'SC', 'GA', 'FL', 'AL', 'MS', 'AR', 'LA']
WEST_COAST_STATES = ['WA', 'OR', 'CA']
MIDWEST_STATES = ['OH', 'IN', 'IL', 'MI', 'WI', 'MN', 'IA', 'MO', 'ND', 'SD', 'NE', 'KS']
MOUNTAIN_STATES = ['MT', 'ID', 'WY', 'CO', 'UT', 'NV', 'AZ', 'NM']
SOUTHWEST_STATES = ['TX', 'OK', 'LA']

def load_data():
    """Load cities data"""
    try:
        cities_df = pd.read_csv(CITIES_DATA_PATH)
        return cities_df
    except FileNotFoundError as e:
        print(f"❌ Data file not found: {e}")
        return None

def generate_founding_year(naming_type, state_code, prestige):
    """Generate founding year based on historical patterns, naming type, region, and prestige"""
    
    # Base year ranges by era
    ERA_RANGES = {
        'early_boom': (1890, 1920),      # Early golf boom
        'depression_era': (1920, 1950),   # Depression and WWII
        'post_war': (1950, 1980),        # Post-war boom
        'modern': (1980, 2000)           # Modern era
    }
    
    # Determine region
    if state_code in NORTHEAST_STATES:
        region = 'northeast'
    elif state_code in SOUTHERN_STATES:
        region = 'south'
    elif state_code in WEST_COAST_STATES:
        region = 'west_coast'
    elif state_code in MIDWEST_STATES:
        region = 'midwest'
    elif state_code in MOUNTAIN_STATES:
        region = 'mountain'
    elif state_code in SOUTHWEST_STATES:
        region = 'southwest'
    else:
        region = 'other'
    
    # Regional era preferences (probability of each era)
    REGIONAL_ERAS = {
        'northeast': {
            'early_boom': 0.6,      # Northeast had early golf boom
            'depression_era': 0.25,
            'post_war': 0.1,
            'modern': 0.05
        },
        'south': {
            'early_boom': 0.4,      # Some early clubs, but more post-war
            'depression_era': 0.3,
            'post_war': 0.2,
            'modern': 0.1
        },
        'west_coast': {
            'early_boom': 0.1,      # West Coast golf came later
            'depression_era': 0.2,
            'post_war': 0.4,
            'modern': 0.3
        },
        'midwest': {
            'early_boom': 0.3,
            'depression_era': 0.3,
            'post_war': 0.3,
            'modern': 0.1
        },
        'mountain': {
            'early_boom': 0.05,     # Mountain golf is mostly modern
            'depression_era': 0.1,
            'post_war': 0.3,
            'modern': 0.55
        },
        'southwest': {
            'early_boom': 0.1,
            'depression_era': 0.2,
            'post_war': 0.4,
            'modern': 0.3
        },
        'other': {
            'early_boom': 0.2,
            'depression_era': 0.3,
            'post_war': 0.3,
            'modern': 0.2
        }
    }
    
    # Naming type era preferences
    NAMING_TYPE_ERAS = {
        'family': {
            'early_boom': 0.7,      # Family clubs tend to be older
            'depression_era': 0.2,
            'post_war': 0.1,
            'modern': 0.0
        },
        'pcc': {
            'early_boom': 0.0,      # PCC clubs are modern
            'depression_era': 0.1,
            'post_war': 0.6,
            'modern': 0.3
        },
        'location': {
            'early_boom': 0.2,      # Location-based are mixed
            'depression_era': 0.3,
            'post_war': 0.3,
            'modern': 0.2
        }
    }
    
    # Combine regional and naming type preferences
    era_weights = {}
    for era in ERA_RANGES.keys():
        regional_weight = REGIONAL_ERAS[region][era]
        naming_weight = NAMING_TYPE_ERAS[naming_type][era]
        # Average the weights, with slight preference for naming type
        era_weights[era] = (regional_weight * 0.4) + (naming_weight * 0.6)
    
    # Normalize weights
    total_weight = sum(era_weights.values())
    era_weights = {era: weight/total_weight for era, weight in era_weights.items()}
    
    # Select era based on weights
    rand = random.random()
    cumulative = 0
    selected_era = None
    for era, weight in era_weights.items():
        cumulative += weight
        if rand <= cumulative:
            selected_era = era
            break
    
    # Get year range for selected era
    min_year, max_year = ERA_RANGES[selected_era]
    
    # Adjust for prestige (higher prestige = slightly older within era)
    prestige_adjustment = (prestige - 0.5) * 10  # ±5 years based on prestige
    target_year = (min_year + max_year) / 2 + prestige_adjustment
    
    # Add some randomness within the era
    year_range = max_year - min_year
    random_offset = random.uniform(-year_range * 0.3, year_range * 0.3)
    
    final_year = int(target_year + random_offset)
    
    # Clamp to era bounds
    final_year = max(min_year, min(max_year, final_year))
    
    return final_year

def generate_course_name(city_name, state_code, naming_type='random'):
    """Generate course name based on naming convention"""
    if naming_type == 'random':
        rand = random.random()
        if rand < 0.1:
            naming_type = 'pcc'
        elif rand < 0.6:
            naming_type = 'location'
        else:
            naming_type = 'family'
    
    if naming_type == 'pcc':
        return f"PCC {city_name}", 'pcc'
    elif naming_type == 'location':
        if random.random() < 0.3:
            geo_term = random.choice(GEOGRAPHIC_TERMS)
            suffix = random.choice(CLUB_SUFFIXES)
            return f"{city_name} {geo_term} {suffix}", 'location'
        else:
            suffix = random.choice(CLUB_SUFFIXES)
            return f"{city_name} {suffix}", 'location'
    elif naming_type == 'family':
        if state_code in NORTHEAST_STATES:
            family_pool = FAMILY_NAMES['old_money'] + FAMILY_NAMES['early_american']
        elif state_code in SOUTHERN_STATES:
            family_pool = FAMILY_NAMES['early_american']
        else:
            family_pool = FAMILY_NAMES['old_money'] + FAMILY_NAMES['early_american']
        
        family_name = random.choice(family_pool)
        geo_term = random.choice(GEOGRAPHIC_TERMS)
        suffix = random.choice(CLUB_SUFFIXES)
        return f"{family_name} {geo_term} {suffix}", 'family'



def generate_holes():
    """Generate 18 holes with par distribution and placement rules"""
    max_attempts = 1000
    
    for attempt in range(max_attempts):
        # Generate par distribution
        par_4s = random.randint(8, 12)
        remaining_holes = 18 - par_4s
        
        # Ensure equal-ish split of par 3s and 5s
        if remaining_holes % 2 == 0:
            par_3s = par_5s = remaining_holes // 2
        else:
            # Slight variation allowed
            par_3s = remaining_holes // 2
            par_5s = remaining_holes - par_3s
        
        # Create par list
        pars = [3] * par_3s + [4] * par_4s + [5] * par_5s
        random.shuffle(pars)
        
        # Try to place pars while respecting rules
        holes = [None] * 18
        
        # Place par 3s and 5s first
        par_3_positions = []
        par_5_positions = []
        
        for i, par in enumerate(pars):
            if par == 3:
                par_3_positions.append(i)
            elif par == 5:
                par_5_positions.append(i)
        
        # Try to place par 3s and 5s
        success = True
        
        # Place par 3s (avoiding holes 1, 9, 10, 18)
        forbidden_holes = [0, 8, 9, 17]  # 0-indexed
        available_holes = [i for i in range(18) if i not in forbidden_holes]
        
        if len(par_3_positions) > len(available_holes):
            success = False
        else:
            par_3_placements = random.sample(available_holes, len(par_3_positions))
            for pos in par_3_placements:
                holes[pos] = 3
        
        # Place par 5s in remaining positions
        if success:
            remaining_positions = [i for i in range(18) if holes[i] is None]
            if len(par_5_positions) <= len(remaining_positions):
                par_5_placements = random.sample(remaining_positions, len(par_5_positions))
                for pos in par_5_placements:
                    holes[pos] = 5
            else:
                success = False
        
        # Fill remaining holes with par 4s
        if success:
            for i in range(18):
                if holes[i] is None:
                    holes[i] = 4
        
        # Validate rules
        if success and validate_hole_rules(holes):
            return holes
    
    # If we can't generate valid holes after max attempts, return None
    return None

def validate_hole_rules(holes):
    """Validate all hole placement rules"""
    
    # Check for consecutive par 3s or par 5s
    for i in range(17):
        if holes[i] == holes[i+1] and holes[i] in [3, 5]:
            return False
    
    # Check for 3-5-3 or 5-3-5 sequences
    for i in range(16):
        if (holes[i] == 3 and holes[i+1] == 5 and holes[i+2] == 3) or \
           (holes[i] == 5 and holes[i+1] == 3 and holes[i+2] == 5):
            return False
    
    # Check nine-hole balance
    front_nine = holes[:9]
    back_nine = holes[9:]
    
    front_par = sum(front_nine)
    back_par = sum(back_nine)
    
    if abs(front_par - back_par) > 2:
        return False
    
    # Check for at least 1 par 3 and 1 par 5 on each nine
    if 3 not in front_nine or 5 not in front_nine:
        return False
    if 3 not in back_nine or 5 not in back_nine:
        return False
    
    # Check total par is in range
    total_par = sum(holes)
    if total_par < 69 or total_par > 73:
        return False
    
    return True

def generate_yardages(holes):
    """Generate yardages for holes with specific requirements"""
    max_attempts = 1000
    
    for attempt in range(max_attempts):
        yardages = []
        used_yardages = set()
        
        for par in holes:
            # Generate yardage based on par
            if par == 3:
                min_yardage, max_yardage = 120, 251
            elif par == 4:
                min_yardage, max_yardage = 290, 503
            else:  # par 5
                min_yardage, max_yardage = 504, 677
            
            # Try to find a yardage that's at least 10 yards different from any existing yardage
            valid_yardage = None
            for _ in range(50):  # Try 50 times to find a valid yardage
                yardage = random.randint(min_yardage, max_yardage)
                
                # Check if this yardage is at least 10 yards different from all used yardages
                valid = True
                for used_yardage in used_yardages:
                    if abs(yardage - used_yardage) < 10:
                        valid = False
                        break
                
                if valid:
                    valid_yardage = yardage
                    break
            
            if valid_yardage is None:
                # If we can't find a valid yardage, try adjusting existing ones
                for used_yardage in list(used_yardages):
                    if abs(used_yardage - min_yardage) < 10:
                        # Remove yardages that are too close to the minimum
                        used_yardages.remove(used_yardage)
                        yardages = [y for y in yardages if y != used_yardage]
                
                # Try again with adjusted ranges
                yardage = random.randint(min_yardage, max_yardage)
                valid_yardage = yardage
            
            yardages.append(valid_yardage)
            used_yardages.add(valid_yardage)
        
        # Check total yardage
        total_yardage = sum(yardages)
        if total_yardage < 6900 or total_yardage > 7600:
            continue
        
        # Check front/back nine split
        front_nine_yardage = sum(yardages[:9])
        back_nine_yardage = sum(yardages[9:])
        
        front_percentage = front_nine_yardage / total_yardage
        if front_percentage < 0.485 or front_percentage > 0.515:
            continue
        
        return yardages
    
    # If we can't generate valid yardages, adjust them
    return adjust_yardages(holes)

def adjust_yardages(holes):
    """Adjust yardages to meet requirements"""
    # Start with random yardages
    yardages = []
    for par in holes:
        if par == 3:
            yardage = random.randint(120, 251)
        elif par == 4:
            yardage = random.randint(290, 503)
        else:  # par 5
            yardage = random.randint(504, 677)
        yardages.append(yardage)
    
    # Adjust to meet total yardage requirement
    total_yardage = sum(yardages)
    target_yardage = random.randint(6900, 7600)
    
    if total_yardage < 6900:
        # Need to increase yardages
        while total_yardage < 6900:
            # Find a hole that can be lengthened
            for i in range(18):
                par = holes[i]
                current_yardage = yardages[i]
                
                if par == 3 and current_yardage < 251:
                    yardages[i] = min(251, current_yardage + 10)
                    break
                elif par == 4 and current_yardage < 503:
                    yardages[i] = min(503, current_yardage + 10)
                    break
                elif par == 5 and current_yardage < 677:
                    yardages[i] = min(677, current_yardage + 10)
                    break
            
            total_yardage = sum(yardages)
    
    elif total_yardage > 7600:
        # Need to decrease yardages
        while total_yardage > 7600:
            # Find a hole that can be shortened
            for i in range(18):
                par = holes[i]
                current_yardage = yardages[i]
                
                if par == 3 and current_yardage > 120:
                    yardages[i] = max(120, current_yardage - 10)
                    break
                elif par == 4 and current_yardage > 290:
                    yardages[i] = max(290, current_yardage - 10)
                    break
                elif par == 5 and current_yardage > 504:
                    yardages[i] = max(504, current_yardage - 10)
                    break
            
            total_yardage = sum(yardages)
    
    # Adjust front/back nine split
    front_nine_yardage = sum(yardages[:9])
    back_nine_yardage = sum(yardages[9:])
    total_yardage = front_nine_yardage + back_nine_yardage
    
    target_front_percentage = 0.51  # Aim for 51%
    target_front_yardage = total_yardage * target_front_percentage
    
    if front_nine_yardage < target_front_yardage:
        # Move yardage from back to front
        needed_yardage = target_front_yardage - front_nine_yardage
        for i in range(9, 18):
            if needed_yardage <= 0:
                break
            par = holes[i]
            current_yardage = yardages[i]
            
            if par == 3 and current_yardage > 120:
                reduction = min(needed_yardage, current_yardage - 120)
                yardages[i] -= reduction
                needed_yardage -= reduction
            elif par == 4 and current_yardage > 290:
                reduction = min(needed_yardage, current_yardage - 290)
                yardages[i] -= reduction
                needed_yardage -= reduction
            elif par == 5 and current_yardage > 504:
                reduction = min(needed_yardage, current_yardage - 504)
                yardages[i] -= reduction
                needed_yardage -= reduction
        
        # Add yardage to front nine
        for i in range(9):
            if needed_yardage <= 0:
                break
            par = holes[i]
            current_yardage = yardages[i]
            
            if par == 3 and current_yardage < 251:
                addition = min(needed_yardage, 251 - current_yardage)
                yardages[i] += addition
                needed_yardage -= addition
            elif par == 4 and current_yardage < 503:
                addition = min(needed_yardage, 503 - current_yardage)
                yardages[i] += addition
                needed_yardage -= addition
            elif par == 5 and current_yardage < 677:
                addition = min(needed_yardage, 677 - current_yardage)
                yardages[i] += addition
                needed_yardage -= addition
    
    return yardages

def generate_handicap_indexes():
    """Generate handicap stroke indexes using evens/odds method"""
    # Split 1-18 into evens and odds
    evens = [2, 4, 6, 8, 10, 12, 14, 16, 18]
    odds = [1, 3, 5, 7, 9, 11, 13, 15, 17]
    
    # Randomly assign one group to front nine, other to back nine
    if random.random() < 0.5:
        front_indexes = evens.copy()
        back_indexes = odds.copy()
    else:
        front_indexes = odds.copy()
        back_indexes = evens.copy()
    
    # Randomly shuffle the indexes within each nine
    random.shuffle(front_indexes)
    random.shuffle(back_indexes)
    
    # Combine front and back indexes
    all_indexes = front_indexes + back_indexes
    
    return all_indexes

def generate_hole_difficulties(holes, yardages, handicap_indexes):
    """Generate hole difficulties using stroke index (40%) and yardage relative to par (60%)"""
    difficulties = []
    
    # Calculate average yardages by par type for this course
    par_3_yardages = [yardages[i] for i, par in enumerate(holes) if par == 3]
    par_4_yardages = [yardages[i] for i, par in enumerate(holes) if par == 4]
    par_5_yardages = [yardages[i] for i, par in enumerate(holes) if par == 5]
    
    avg_par_3_yardage = sum(par_3_yardages) / len(par_3_yardages) if par_3_yardages else 180
    avg_par_4_yardage = sum(par_4_yardages) / len(par_4_yardages) if par_4_yardages else 400
    avg_par_5_yardage = sum(par_5_yardages) / len(par_5_yardages) if par_5_yardages else 550
    
    for i, (par, yardage, handicap_index) in enumerate(zip(holes, yardages, handicap_indexes)):
        # Base difficulty from stroke index (40% weight)
        # Convert stroke index 1-18 to 0-1 scale (1 = hardest = 1.0, 18 = easiest = 0.0)
        stroke_difficulty = (19 - handicap_index) / 18
        stroke_weighted = stroke_difficulty * 0.4
        
        # Yardage difficulty relative to par average (60% weight)
        if par == 3:
            avg_yardage = avg_par_3_yardage
            min_yardage, max_yardage = 120, 251
        elif par == 4:
            avg_yardage = avg_par_4_yardage
            min_yardage, max_yardage = 290, 503
        else:  # par 5
            avg_yardage = avg_par_5_yardage
            min_yardage, max_yardage = 504, 677
        
        # Calculate yardage difficulty relative to average for this par type
        yardage_range = max_yardage - min_yardage
        yardage_deviation = yardage - avg_yardage
        yardage_difficulty = 0.5 + (yardage_deviation / yardage_range)  # Center at 0.5, scale by range
        yardage_difficulty = max(0.0, min(1.0, yardage_difficulty))  # Clamp to 0-1
        yardage_weighted = yardage_difficulty * 0.6
        
        # Combine stroke and yardage difficulties
        base_difficulty = stroke_weighted + yardage_weighted
        
        # Add randomization (±10%)
        random_factor = random.uniform(-0.1, 0.1)
        final_difficulty = base_difficulty + random_factor
        final_difficulty = max(0.0, min(1.0, final_difficulty))  # Clamp to 0-1
        
        difficulties.append(final_difficulty)
    
    return difficulties

def generate_course_factors(naming_type):
    """Generate course factors based on naming type only."""
    # Generate base factors with some randomness
    factors = {
        'width_index': np.random.beta(4, 2),  # Slightly wider fairways
        'hazard_density': np.random.beta(2, 4),  # Fewer hazards
        'green_speed': np.random.beta(3, 2),
        'turf_firmness': np.random.beta(2, 3),
        'rough_length': np.random.beta(2, 3),
        'terrain_difficulty': np.random.beta(2, 4)
    }

    # Prestige based on naming type
    if naming_type == 'pcc':
        factors['prestige'] = np.random.beta(3, 2)  # Higher prestige for PCC
    elif naming_type == 'family':
        factors['prestige'] = np.random.beta(4, 2)  # Highest prestige for family clubs
    else:
        factors['prestige'] = np.random.beta(2, 3)  # Lower prestige for location-based

    # Prestige correlations
    prestige_factor = factors['prestige']
    # Higher prestige = faster greens, firmer turf, longer rough
    factors['green_speed'] = min(1.0, factors['green_speed'] * (1 + prestige_factor * 0.2))
    factors['turf_firmness'] = min(1.0, factors['turf_firmness'] * (1 + prestige_factor * 0.2))
    factors['rough_length'] = min(1.0, factors['rough_length'] * (1 + prestige_factor * 0.2))

    # Calculate strategic_penal_index based on other factors
    penal_elements = (
        factors['hazard_density'] + factors['green_speed'] +
        factors['turf_firmness'] + factors['rough_length'] + factors['terrain_difficulty']
    ) / 5
    strategic_elements = (1 - factors['width_index']) * 0.5
    factors['strategic_penal_index'] = penal_elements + strategic_elements
    # Clamp to 0-1
    factors['strategic_penal_index'] = max(0.0, min(1.0, factors['strategic_penal_index']))
    return factors

def calculate_course_rating_and_slope(course_data):
    """
    Calculate Course Rating and Slope Rating for PGA Tour-level courses.
    All courses are designed to be professional tour quality.
    """
    # Extract course variables
    par = course_data['total_par']
    yardage = course_data['total_yardage']
    spi = course_data['strategic_penal_index']
    green_speed = course_data['green_speed']
    rough_length = course_data['rough_length']
    hazard_density = course_data['hazard_density']
    terrain_difficulty = course_data['terrain_difficulty']
    prestige = course_data['prestige']
    
    # --- Course Rating (Scratch Golfer) ---
    # Base: start with par
    course_rating = par
    
    # Yardage adjustment: 0.15 strokes per 100 yards over 6500 (more aggressive for tour courses)
    yardage_adj = max(0, (yardage - 6500) / 100) * 0.15
    
    # Strategic/Penal index: up to +3.0 strokes for most penal (more aggressive)
    spi_adj = spi * 3.0
    
    # Other factors: each can add up to 0.6 strokes (more aggressive)
    green_adj = green_speed * 0.6
    rough_adj = rough_length * 0.6
    hazard_adj = hazard_density * 0.6
    terrain_adj = terrain_difficulty * 0.6
    
    # Prestige: higher prestige = slightly lower rating (better conditioning)
    prestige_adj = (0.5 - prestige) * 0.2
    
    course_rating += yardage_adj + spi_adj + green_adj + rough_adj + hazard_adj + terrain_adj + prestige_adj
    
    # All courses are PGA Tour level: 74-78 range
    course_rating = max(74.0, min(78.0, course_rating))
    
    # --- Bogey Rating (Bogey Golfer) ---
    # Start with par + 22 (tour courses are harder for bogey golfers)
    bogey_base = par + 22
    
    # Yardage: 0.3 strokes per 100 yards over 6000 (bigger effect on bogey golfers)
    yardage_adj_bogey = max(0, (yardage - 6000) / 100) * 0.3
    
    # Strategic/Penal index: up to +6 strokes for most penal (bigger effect)
    spi_adj_bogey = spi * 6.0
    
    # Other factors: each can add up to 1.2 strokes (bigger effect)
    green_adj_bogey = green_speed * 1.2
    rough_adj_bogey = rough_length * 1.2
    hazard_adj_bogey = hazard_density * 1.2
    terrain_adj_bogey = terrain_difficulty * 1.2
    
    # Prestige: higher prestige = slightly lower rating
    prestige_adj_bogey = (0.5 - prestige) * 0.4
    
    bogey_rating = bogey_base + yardage_adj_bogey + spi_adj_bogey + green_adj_bogey + rough_adj_bogey + hazard_adj_bogey + terrain_adj_bogey + prestige_adj_bogey
    
    # Ensure bogey rating is at least 20 strokes higher than course rating (tour courses are harder)
    bogey_rating = max(course_rating + 20, bogey_rating)
    
    # All courses are PGA Tour level: bogey rating should be 95-105 range
    bogey_rating = max(95.0, min(105.0, bogey_rating))
    
    # --- Slope Rating ---
    # USGA formula: Slope Rating = (Bogey Rating - Course Rating) × 5.381
    slope_rating = int(round((bogey_rating - course_rating) * 5.381))
    
    # All courses are PGA Tour level: 145-150 range
    slope_rating = max(145, min(150, slope_rating))
    
    return round(course_rating, 1), slope_rating

def generate_complete_course(city_name=None, state_code=None, naming_type='random'):
    """Generate a complete course with all components"""
    
    # Load data
    cities_df = load_data()
    if cities_df is None:
        return None
    
    # Select city if not provided
    if city_name is None or state_code is None:
        city_row = cities_df.sample(n=1).iloc[0]
        city_name = city_row['city']
        state_code = city_row['state']
    
    # Get elevation data for the selected city
    city_data = cities_df[(cities_df['city'] == city_name) & (cities_df['state'] == state_code)]
    if city_data.empty:
        print(f"❌ No data found for {city_name}, {state_code}")
        return None
    
    elevation_ft = city_data.iloc[0]['elevation_ft']
    
    # Generate course name
    course_name, naming_type = generate_course_name(city_name, state_code, naming_type)
    
    # Generate holes
    holes = generate_holes()
    if holes is None:
        print(f"❌ Failed to generate valid holes for {course_name}")
        return None
    
    # Generate yardages
    yardages = generate_yardages(holes)
    if yardages is None:
        print(f"❌ Failed to generate valid yardages for {course_name}")
        return None
    
    # Generate handicap indexes
    handicap_indexes = generate_handicap_indexes()
    
    # Generate hole difficulties
    difficulties = generate_hole_difficulties(holes, yardages, handicap_indexes)
    
    # Generate course factors
    factors = generate_course_factors(naming_type)
    
    # Calculate summary totals
    total_par = sum(holes)
    total_yardage = sum(yardages)
    front_nine_par = sum(holes[:9])
    back_nine_par = sum(holes[9:])
    front_nine_yardage = sum(yardages[:9])
    back_nine_yardage = sum(yardages[9:])
    
    # Determine founding year based on historical patterns, naming type, region, and prestige
    founding_year = generate_founding_year(naming_type, state_code, factors['prestige'])
    
    # Create complete course data
    course_data = {
        'name': course_name,
        'city': city_name,
        'state': state_code,
        'location': f"{city_name}, {state_code} (US)",
        'founding_year': founding_year,
        'naming_type': naming_type,
        'elevation_ft': elevation_ft,
        'holes': holes,
        'yardages': yardages,
        'handicap_indexes': handicap_indexes,
        'difficulties': difficulties,
        'total_par': total_par,
        'total_yardage': total_yardage,
        'front_nine_par': front_nine_par,
        'back_nine_par': back_nine_par,
        'front_nine_yardage': front_nine_yardage,
        'back_nine_yardage': back_nine_yardage,
        **factors
    }
    
    # Calculate Course Rating and Slope Rating
    course_rating, slope_rating = calculate_course_rating_and_slope(course_data)
    course_data['course_rating'] = course_rating
    course_data['slope_rating'] = slope_rating
    
    return course_data

def insert_course_to_database(course_data):
    """Insert a course and its characteristics into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Insert main course record
        cursor.execute('''
            INSERT INTO courses (
                name, city, state_country, location, total_par, total_yardage,
                slope_rating, course_rating, prestige_level, est_year, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            course_data['name'],
            course_data['city'],
            course_data['state'],
            course_data['location'],
            course_data['total_par'],
            course_data['total_yardage'],
            course_data['slope_rating'],
            course_data['course_rating'],
            int(course_data['prestige'] * 100),  # Convert to 0-100 scale
            course_data['founding_year'],
            datetime.now().isoformat()
        ))
        course_id = cursor.lastrowid
        # Insert characteristics
        cursor.execute('''
            INSERT INTO course_characteristics (
                course_id, design_strategy, narrowness_factor, hazard_density, green_speed,
                turf_firmness, rough_length, elevation, terrain_difficulty
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            course_id,
            course_data['strategic_penal_index'],
            1 - course_data['width_index'],  # narrowness_factor is inverse of width_index
            course_data['hazard_density'],
            course_data['green_speed'],
            course_data['turf_firmness'],
            course_data['rough_length'],
            course_data['elevation_ft'],  # Use real elevation data
            course_data['terrain_difficulty']
        ))
        # Insert holes
        for i, (par, yardage, handicap) in enumerate(zip(course_data['holes'], course_data['yardages'], course_data['handicap_indexes']), 1):
            cursor.execute('''
                INSERT INTO holes (course_id, hole_number, par, yardage, handicap, difficulty_modifier)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (course_id, i, par, yardage, handicap, 1.0))
        conn.commit()
        print(f"✅ Inserted course: {course_data['name']} (ID: {course_id})")
        return course_id
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            print(f"⚠️  Course '{course_data['name']}' already exists, skipping...")
            return None
        else:
            raise e
    finally:
        conn.close()

def print_complete_course(course_data):
    """Print complete course information"""
    print(f"\n🏌️  {course_data['name']}")
    print("=" * 100)
    print(f"📍 Location: {course_data['location']}")
    print(f"🏗️  Founded: {course_data['founding_year']}")
    print(f"📋 Naming Type: {course_data['naming_type'].title()}")
    print(f"🏔️  Elevation: {course_data['elevation_ft']:.0f} feet")
    
    print(f"\n📊 Course Summary:")
    print(f"Total Par: {course_data['total_par']} | Total Yardage: {course_data['total_yardage']:,}")
    print(f"Front Nine: {course_data['front_nine_par']} par | {course_data['front_nine_yardage']:,} yards")
    print(f"Back Nine:  {course_data['back_nine_par']} par | {course_data['back_nine_yardage']:,} yards")
    print(f"Par 3s: {course_data['holes'].count(3)} | Par 4s: {course_data['holes'].count(4)} | Par 5s: {course_data['holes'].count(5)}")
    
    print(f"\n🎯 Course Factors:")
    print(f"Strategic/Penal Index: {course_data['strategic_penal_index']:.3f}")
    print(f"Width Index:           {course_data['width_index']:.3f}")
    print(f"Hazard Density:        {course_data['hazard_density']:.3f}")
    print(f"Green Speed:           {course_data['green_speed']:.3f}")
    print(f"Turf Firmness:         {course_data['turf_firmness']:.3f}")
    print(f"Rough Length:          {course_data['rough_length']:.3f}")
    print(f"Terrain Difficulty:    {course_data['terrain_difficulty']:.3f}")
    print(f"Prestige:              {course_data['prestige']:.3f}")
    
    print(f"\n🏆 USGA Ratings:")
    print(f"Course Rating:         {course_data['course_rating']}")
    print(f"Slope Rating:          {course_data['slope_rating']}")
    
    # Interpret strategic/penal index
    spi = course_data['strategic_penal_index']
    if spi < 0.3:
        spi_type = "Strategic"
    elif spi < 0.7:
        spi_type = "Balanced"
    else:
        spi_type = "Penal"
    
    print(f"\n🏌️  Course Type: {spi_type} ({spi:.3f})")
    
    print(f"\n🕳️  Holes:")
    front_nine = course_data['holes'][:9]
    back_nine = course_data['holes'][9:]
    front_yardages = course_data['yardages'][:9]
    back_yardages = course_data['yardages'][9:]
    front_handicaps = course_data['handicap_indexes'][:9]
    back_handicaps = course_data['handicap_indexes'][9:]
    front_difficulties = course_data['difficulties'][:9]
    back_difficulties = course_data['difficulties'][9:]
    
    print("Front Nine:")
    for i, (par, yardage, handicap, difficulty) in enumerate(zip(front_nine, front_yardages, front_handicaps, front_difficulties), 1):
        print(f"  {i:2d}: Par {par} | {yardage:3d} yards | Index {handicap:2d} | Difficulty {difficulty:.3f}")
    
    print("\nBack Nine:")
    for i, (par, yardage, handicap, difficulty) in enumerate(zip(back_nine, back_yardages, back_handicaps, back_difficulties), 10):
        print(f"  {i:2d}: Par {par} | {yardage:3d} yards | Index {handicap:2d} | Difficulty {difficulty:.3f}")
    
    # Difficulty analysis
    avg_difficulty = sum(course_data['difficulties']) / len(course_data['difficulties'])
    min_difficulty = min(course_data['difficulties'])
    max_difficulty = max(course_data['difficulties'])
    
    print(f"\n🎯 Difficulty Analysis:")
    print(f"Average difficulty: {avg_difficulty:.3f}")
    print(f"Range: {min_difficulty:.3f} - {max_difficulty:.3f}")
    print(f"Hardest hole: {course_data['difficulties'].index(max_difficulty) + 1} (Index {course_data['handicap_indexes'][course_data['difficulties'].index(max_difficulty)]})")
    print(f"Easiest hole: {course_data['difficulties'].index(min_difficulty) + 1} (Index {course_data['handicap_indexes'][course_data['difficulties'].index(min_difficulty)]})")

def main():
    """Generate a sample complete course and insert it into the database"""
    print("🏌️  Complete Course Generation")
    print("=" * 100)
    
    # Generate a complete course
    course = generate_complete_course()
    
    if course:
        print_complete_course(course)
        
        # Insert into database
        course_id = insert_course_to_database(course)
        if course_id:
            print(f"🎉 Successfully created and inserted course with ID: {course_id}")
        else:
            print("❌ Failed to insert course into database")
        
        return course
    else:
        print("❌ Failed to generate complete course")
        return None

if __name__ == "__main__":
    main() 