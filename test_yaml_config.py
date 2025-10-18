#!/usr/bin/env python3
"""
Test script to validate YAML configuration without running EnergyPlus.
"""

import yaml
import os

def test_yaml_syntax():
    """Test if the YAML file has valid syntax."""
    yaml_path = 'sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml'
    
    try:
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        print("✅ YAML syntax is valid")
        return True
    except yaml.YAMLError as e:
        print(f"❌ YAML syntax error: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ YAML file not found: {yaml_path}")
        return False

def test_variable_structure():
    """Test if the variables section has the correct structure."""
    yaml_path = 'sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml'
    
    try:
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        
        variables = config.get('variables', {})
        print(f"📊 Found {len(variables)} variables")
        
        # Check for key HVAC variables
        hvac_vars = [
            'Fan Electricity Rate',
            'Fan Air Mass Flow Rate',
            'Cooling Coil Total Cooling Rate',
            'Cooling Coil Electricity Rate',
            'Heating Coil Heating Rate',
            'Heating Coil Electricity Rate',
            'Air System Outdoor Air Flow Fraction'
        ]
        
        missing_vars = []
        for var in hvac_vars:
            if var not in variables:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing variables: {missing_vars}")
        else:
            print("✅ All key HVAC variables found")
        
        # Check variable structure
        for var_name, var_config in variables.items():
            if not isinstance(var_config, dict):
                print(f"⚠️  Variable {var_name} is not a dictionary")
                continue
            
            if 'variable_names' not in var_config:
                print(f"⚠️  Variable {var_name} missing 'variable_names'")
            if 'keys' not in var_config:
                print(f"⚠️  Variable {var_name} missing 'keys'")
        
        return len(missing_vars) == 0
        
    except Exception as e:
        print(f"❌ Error testing variable structure: {e}")
        return False

def test_meters_structure():
    """Test if the meters section has the correct structure."""
    yaml_path = 'sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml'
    
    try:
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        
        meters = config.get('meters', {})
        print(f"📊 Found {len(meters)} meters")
        
        # Check for key HVAC meters
        hvac_meters = [
            'Electricity:HVAC',
            'Fan Electricity Energy',
            'Cooling Coil Total Cooling Energy',
            'Cooling Coil Electricity Energy',
            'Heating Coil Heating Energy',
            'Heating Coil Electricity Energy'
        ]
        
        missing_meters = []
        for meter in hvac_meters:
            if meter not in meters:
                missing_meters.append(meter)
        
        if missing_meters:
            print(f"⚠️  Missing meters: {missing_meters}")
        else:
            print("✅ All key HVAC meters found")
        
        return len(missing_meters) == 0
        
    except Exception as e:
        print(f"❌ Error testing meters structure: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing YAML Configuration")
    print("=" * 50)
    
    # Test 1: YAML syntax
    syntax_ok = test_yaml_syntax()
    
    # Test 2: Variable structure
    variables_ok = test_variable_structure()
    
    # Test 3: Meters structure
    meters_ok = test_meters_structure()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")
    print(f"   YAML Syntax: {'✅ PASS' if syntax_ok else '❌ FAIL'}")
    print(f"   Variables Structure: {'✅ PASS' if variables_ok else '❌ FAIL'}")
    print(f"   Meters Structure: {'✅ PASS' if meters_ok else '❌ FAIL'}")
    
    if syntax_ok and variables_ok and meters_ok:
        print("\n🎉 All YAML configuration tests passed!")
        return True
    else:
        print("\n⚠️  Some YAML configuration tests failed.")
        return False

if __name__ == "__main__":
    main()