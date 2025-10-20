#!/usr/bin/env python3
"""
Simple validation script for the epJSON file
"""

import json
import sys

def validate_epjson(file_path):
    """Validate the epJSON file structure"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print(f"✅ Successfully loaded {file_path}")
        print(f"📊 File contains {len(data)} top-level sections")
        
        # Check for required sections
        required_sections = [
            'RunPeriod', 'Schedule:Compact', 'ThermostatSetpoint:DualSetpoint',
            'ThermostatSetpoint:SingleCooling', 'ThermostatSetpoint:SingleHeating',
            'ZoneControl:Thermostat', 'Building', 'Version'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in data:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Missing required sections: {missing_sections}")
            return False
        else:
            print("✅ All required sections present")
        
        # Check for individual zone schedules
        schedule_section = data.get('Schedule:Compact', {})
        individual_schedules = [
            'SPACE1-1-Htg-SetP-Sch', 'SPACE1-1-Clg-SetP-Sch',
            'SPACE2-1-Htg-SetP-Sch', 'SPACE2-1-Clg-SetP-Sch',
            'SPACE3-1-Htg-SetP-Sch', 'SPACE3-1-Clg-SetP-Sch',
            'SPACE4-1-Htg-SetP-Sch', 'SPACE4-1-Clg-SetP-Sch',
            'SPACE5-1-Htg-SetP-Sch', 'SPACE5-1-Clg-SetP-Sch'
        ]
        
        missing_schedules = []
        for schedule in individual_schedules:
            if schedule not in schedule_section:
                missing_schedules.append(schedule)
        
        if missing_schedules:
            print(f"❌ Missing individual zone schedules: {missing_schedules}")
            return False
        else:
            print("✅ All individual zone schedules present")
        
        # Check thermostat controls
        thermostat_section = data.get('ZoneControl:Thermostat', {})
        zones = ['SPACE1-1', 'SPACE2-1', 'SPACE3-1', 'SPACE4-1', 'SPACE5-1']
        
        for zone in zones:
            control_name = f"{zone} Control"
            if control_name in thermostat_section:
                control = thermostat_section[control_name]
                if (f"{zone}-CoolingSetpoint" in control.get('control_1_name', '') and
                    f"{zone}-HeatingSetpoint" in control.get('control_2_name', '') and
                    f"{zone}-DualSetPoint" in control.get('control_3_name', '')):
                    print(f"✅ {zone} control properly configured")
                else:
                    print(f"❌ {zone} control not properly configured")
                    return False
            else:
                print(f"❌ Missing {control_name}")
                return False
        
        print("🎉 All validations passed! The epJSON file is ready for use.")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON syntax error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    file_path = "/workspace/5ZoneAutoDXVAV_5zone_individual_fixed.epJSON"
    success = validate_epjson(file_path)
    sys.exit(0 if success else 1)