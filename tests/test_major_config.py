#!/usr/bin/env python3
"""
Test script to verify major tournament configurations
"""

import json
import random
from pathlib import Path

def test_major_configurations():
    """Test major tournament configurations"""
    
    # Load configurations
    config_dir = Path("config")
    
    with open(config_dir / "tournament_overrides.json", "r") as f:
        overrides = json.load(f)
    
    with open(config_dir / "event_types.json", "r") as f:
        event_types = json.load(f)
    
    print("=== MAJOR TOURNAMENT CONFIGURATION TEST ===\n")
    
    # Test each major
    majors = overrides.get("majors", {})
    base_major_config = event_types.get("major", {})
    
    for major_name, major_config in majors.items():
        print(f"Testing: {major_name}")
        print("-" * 50)
        
        # Test purse configuration
        purse_config = major_config.get("purse_base", base_major_config.get("purse_base"))
        if purse_config and purse_config.get("type") == "random":
            min_purse = purse_config["min"] / 1_000_000
            max_purse = purse_config["max"] / 1_000_000
            round_to = purse_config.get("round_to", 1_000_000) / 1_000_000
            
            print(f"Purse: Random ${min_purse}M - ${max_purse}M (rounded to ${round_to}M)")
            
            # Generate a sample purse
            sample_purse = random.randint(purse_config["min"], purse_config["max"])
            rounded_purse = round(sample_purse / purse_config["round_to"]) * purse_config["round_to"]
            print(f"Sample purse: ${sample_purse:,} → ${rounded_purse:,} (${rounded_purse/1_000_000:.0f}M)")
        else:
            print(f"Purse: Fixed ${purse_config/1_000_000:.0f}M" if isinstance(purse_config, (int, float)) else f"Purse: {purse_config}")
        
        # Test prestige configuration
        prestige_config = major_config.get("prestige", base_major_config.get("prestige"))
        if prestige_config:
            if prestige_config.get("type") == "fixed":
                prestige_value = prestige_config["value"]
                print(f"Prestige: Fixed {prestige_value}")
            elif prestige_config.get("type") == "random":
                min_prestige = prestige_config["min"]
                max_prestige = prestige_config["max"]
                print(f"Prestige: Random {min_prestige} - {max_prestige}")
                
                # Generate a sample prestige
                sample_prestige = random.uniform(min_prestige, max_prestige)
                print(f"Sample prestige: {sample_prestige:.2f}")
        
        # Test field size
        field_size = major_config.get("field_size", base_major_config.get("field_size"))
        print(f"Field size: {field_size}")
        
        # Test cut line
        cut_line = major_config.get("cut_line", base_major_config.get("cut_line"))
        if cut_line:
            cut_type = cut_line.get("type", "unknown")
            cut_value = cut_line.get("value", "unknown")
            print(f"Cut line: {cut_type} - {cut_value}")
        
        print()
    
    print("=== CONFIGURATION SUMMARY ===")
    print(f"Total majors configured: {len(majors)}")
    print("All majors should have:")
    print("- Random purse: $21M - $25M (rounded to $1M)")
    print("- Fixed prestige: 10.0 (maximum)")
    print("- Field size: 156 (default) or custom")
    print("- Cut line: Top 70 and ties (default) or custom")

if __name__ == "__main__":
    test_major_configurations() 