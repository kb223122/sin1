#!/usr/bin/env python3
"""
Validate actuator mapping between YAML and epJSON
"""

import json
import yaml

def validate_actuator_mapping():
    """Validate that actuator names in YAML match epJSON schedule names"""
    
    # Load epJSON
    with open('/workspace/5ZoneAutoDXVAV_5zone_individual_fixed.epJSON', 'r') as f:
        epjson_data = json.load(f)
    
    # Load YAML
    with open('/workspace/5zone_individual_corrected_final.yaml', 'r') as f:
        yaml_data = yaml.safe_load(f)
    
    # Get schedule names from epJSON
    schedules = epjson_data.get('Schedule:Compact', {})
    epjson_schedule_names = [name for name in schedules.keys() if 'SPACE' in name and 'SetP-Sch' in name]
    
    # Get actuator names from YAML
    actuators = yaml_data.get('actuators', {})
    yaml_actuator_names = list(actuators.keys())
    
    print("🔍 EpJSON Schedule Names:")
    for name in sorted(epjson_schedule_names):
        print(f"  - {name}")
    
    print("\n🔍 YAML Actuator Names:")
    for name in sorted(yaml_actuator_names):
        print(f"  - {name}")
    
    # Check for matches
    matches = []
    mismatches = []
    
    for yaml_name in yaml_actuator_names:
        if yaml_name in epjson_schedule_names:
            matches.append(yaml_name)
        else:
            mismatches.append(yaml_name)
    
    print(f"\n✅ Matches: {len(matches)}")
    for match in matches:
        print(f"  ✓ {match}")
    
    print(f"\n❌ Mismatches: {len(mismatches)}")
    for mismatch in mismatches:
        print(f"  ✗ {mismatch}")
    
    # Check for missing schedules in YAML
    missing_in_yaml = []
    for epjson_name in epjson_schedule_names:
        if epjson_name not in yaml_actuator_names:
            missing_in_yaml.append(epjson_name)
    
    if missing_in_yaml:
        print(f"\n⚠️  Missing in YAML: {len(missing_in_yaml)}")
        for missing in missing_in_yaml:
            print(f"  - {missing}")
    
    return len(mismatches) == 0 and len(missing_in_yaml) == 0

if __name__ == "__main__":
    success = validate_actuator_mapping()
    if success:
        print("\n🎉 All actuator mappings are correct!")
    else:
        print("\n❌ There are actuator mapping issues to fix.")