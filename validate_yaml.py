#!/usr/bin/env python3
"""
Simple validation script for the YAML file
"""

import yaml
import sys

def validate_yaml(file_path):
    """Validate the YAML file structure"""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        print(f"✅ Successfully loaded {file_path}")
        
        # Check required sections
        required_sections = [
            'id_base', 'building_file', 'weather_specification', 
            'variables', 'actuators', 'action_space'
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
        
        # Check building file reference
        building_file = data.get('building_file', '')
        if building_file == '5ZoneAutoDXVAV_5zone_individual_fixed.epJSON':
            print("✅ Building file correctly referenced")
        else:
            print(f"❌ Building file incorrect: {building_file}")
            return False
        
        # Check actuators
        actuators = data.get('actuators', {})
        expected_actuators = [
            'SPACE1-1-Htg-SetP-Sch', 'SPACE1-1-Clg-SetP-Sch',
            'SPACE2-1-Htg-SetP-Sch', 'SPACE2-1-Clg-SetP-Sch',
            'SPACE3-1-Htg-SetP-Sch', 'SPACE3-1-Clg-SetP-Sch',
            'SPACE4-1-Htg-SetP-Sch', 'SPACE4-1-Clg-SetP-Sch',
            'SPACE5-1-Htg-SetP-Sch', 'SPACE5-1-Clg-SetP-Sch'
        ]
        
        missing_actuators = []
        for actuator in expected_actuators:
            if actuator not in actuators:
                missing_actuators.append(actuator)
        
        if missing_actuators:
            print(f"❌ Missing actuators: {missing_actuators}")
            return False
        else:
            print("✅ All individual zone actuators present")
        
        # Check action space
        action_space = data.get('action_space', '')
        if 'gym.spaces.Box' in action_space and 'shape=(10,)' in action_space:
            print("✅ Action space correctly configured for 10 dimensions")
        else:
            print(f"❌ Action space incorrect: {action_space}")
            return False
        
        print("🎉 All validations passed! The YAML file is ready for use.")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    file_path = "/workspace/5zone_individual_simple.yaml"
    success = validate_yaml(file_path)
    sys.exit(0 if success else 1)