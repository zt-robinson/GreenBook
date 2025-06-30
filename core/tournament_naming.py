#!/usr/bin/env python3
"""
Tournament naming utilities
"""

import json
import os
import random

def load_company_names():
    """Load company names from config file"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'company_names.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {config_path} not found, using default company names")
        return ["Acme", "Blue Ridge", "Cedar Valley", "Delta", "Eagle Crest"]

def load_event_suffixes():
    """Load event suffixes from config file"""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'event_suffixes.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {config_path} not found, using default suffixes")
        return ["Championship", "Invitational", "Open", "Tournament", "Classic"]

def generate_standard_event_name():
    """Generate a random standard event name"""
    companies = load_company_names()
    suffixes = load_event_suffixes()
    
    company = random.choice(companies)
    suffix = random.choice(suffixes)
    
    return f"{company} {suffix}"

def generate_invitational_event_name():
    """Generate a random invitational event name"""
    companies = load_company_names()
    suffixes = load_event_suffixes()
    
    company = random.choice(companies)
    suffix = random.choice(suffixes)
    
    return f"{company} {suffix}"

def get_major_names():
    """Return the fixed names for majors"""
    return {
        "sovereign": "The Sovereign Tournament",
        "american_open": "The American Open", 
        "royal_open": "The Royal Open",
        "aga_championship": "The AGA Championship"
    } 