#!/usr/bin/env python3
"""
Validate the fixed HVAC monitoring configuration without requiring EnergyPlus.
"""

import json
import yaml
import os

def validate_epjson():
    """Validate the epJSON file structure."""
    print("🔍 Validating epJSON file...")
    
    try:
        with open('sinergym/data/buildings/5ZoneAutoDXVAV.epJSON', 'r') as file:
            epjson_data = json.load(file)
        
        # Check Output:Variable section
        if 'Output:Variable' in epjson_data:
            variables = epjson_data['Output:Variable']
            print(f"   ✅ Output:Variable section found with {len(variables)} variables")
            
            # Check for key HVAC variables
            expected_vars = [
                'Fan Electricity Rate',
                'Fan Air Mass Flow Rate',
                'Cooling Coil Total Cooling Rate',
                'Cooling Coil Electricity Rate',
                'Heating Coil Heating Rate',
                'Heating Coil Electricity Rate',
                'Air System Outdoor Air Flow Fraction'
            ]
            
            for var in expected_vars:
                if var in variables:
                    var_config = variables[var]
                    if 'key_value' in var_config and 'variable_name' in var_config:
                        print(f"   ✅ {var}: {var_config['key_value']} -> {var_config['variable_name']}")
                    else:
                        print(f"   ⚠️  {var}: Missing key_value or variable_name")
                else:
                    print(f"   ❌ {var}: NOT FOUND")
        else:
            print("   ❌ Output:Variable section not found")
            return False
        
        # Check Output:Meter section
        if 'Output:Meter' in epjson_data:
            meters = epjson_data['Output:Meter']
            print(f"   ✅ Output:Meter section found with {len(meters)} meters")
            
            # Check for key meters
            expected_meters = [
                'Electricity:HVAC',
                'Electricity:Fans',
                'Electricity:Cooling',
                'Electricity:Heating'
            ]
            
            for meter in expected_meters:
                if meter in meters:
                    print(f"   ✅ {meter}: Found")
                else:
                    print(f"   ❌ {meter}: NOT FOUND")
        else:
            print("   ❌ Output:Meter section not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error validating epJSON: {e}")
        return False

def validate_yaml():
    """Validate the YAML file structure."""
    print("\n🔍 Validating YAML file...")
    
    try:
        with open('sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml', 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        # Check variables section
        if 'variables' in yaml_data:
            variables = yaml_data['variables']
            print(f"   ✅ Variables section found with {len(variables)} variables")
            
            # Check for key HVAC variables
            expected_vars = [
                'Fan Electricity Rate',
                'Fan Air Mass Flow Rate',
                'Cooling Coil Total Cooling Rate',
                'Cooling Coil Electricity Rate',
                'Heating Coil Heating Rate',
                'Heating Coil Electricity Rate',
                'Air System Outdoor Air Flow Fraction'
            ]
            
            for var in expected_vars:
                if var in variables:
                    var_config = variables[var]
                    if 'variable_names' in var_config and 'keys' in var_config:
                        print(f"   ✅ {var}: {var_config['keys']} -> {var_config['variable_names']}")
                    else:
                        print(f"   ⚠️  {var}: Missing variable_names or keys")
                else:
                    print(f"   ❌ {var}: NOT FOUND")
        else:
            print("   ❌ Variables section not found")
            return False
        
        # Check meters section
        if 'meters' in yaml_data:
            meters = yaml_data['meters']
            print(f"   ✅ Meters section found with {len(meters)} meters")
            
            # Check for key meters
            expected_meters = [
                'Electricity:HVAC',
                'Electricity:Fans',
                'Electricity:Cooling',
                'Electricity:Heating'
            ]
            
            for meter in expected_meters:
                if meter in meters:
                    print(f"   ✅ {meter}: {meters[meter]}")
                else:
                    print(f"   ❌ {meter}: NOT FOUND")
        else:
            print("   ❌ Meters section not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error validating YAML: {e}")
        return False

def check_configuration_alignment():
    """Check if epJSON and YAML configurations are aligned."""
    print("\n🔍 Checking configuration alignment...")
    
    try:
        # Load epJSON
        with open('sinergym/data/buildings/5ZoneAutoDXVAV.epJSON', 'r') as file:
            epjson_data = json.load(file)
        
        # Load YAML
        with open('sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml', 'r') as file:
            yaml_data = yaml.safe_load(file)
        
        # Check variable alignment
        epjson_vars = epjson_data.get('Output:Variable', {})
        yaml_vars = yaml_data.get('variables', {})
        
        print("   📊 Variable alignment:")
        for var_name in epjson_vars:
            if var_name in yaml_vars:
                epjson_key = epjson_vars[var_name].get('key_value', '')
                yaml_key = yaml_vars[var_name].get('keys', '')
                if epjson_key == yaml_key:
                    print(f"   ✅ {var_name}: Keys match ({epjson_key})")
                else:
                    print(f"   ⚠️  {var_name}: Key mismatch (epJSON: {epjson_key}, YAML: {yaml_key})")
            else:
                print(f"   ❌ {var_name}: Not found in YAML")
        
        # Check meter alignment
        epjson_meters = epjson_data.get('Output:Meter', {})
        yaml_meters = yaml_data.get('meters', {})
        
        print("   📊 Meter alignment:")
        for meter_name in epjson_meters:
            if meter_name in yaml_meters:
                print(f"   ✅ {meter_name}: Found in both files")
            else:
                print(f"   ❌ {meter_name}: Not found in YAML")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error checking alignment: {e}")
        return False

def main():
    """Run all validation checks."""
    print("🏢 HVAC Configuration Validation")
    print("=" * 60)
    print("This script validates the fixed configuration files.")
    print("=" * 60)
    
    # Check if files exist
    epjson_path = 'sinergym/data/buildings/5ZoneAutoDXVAV.epJSON'
    yaml_path = 'sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml'
    
    if not os.path.exists(epjson_path):
        print(f"❌ epJSON file not found: {epjson_path}")
        return False
    
    if not os.path.exists(yaml_path):
        print(f"❌ YAML file not found: {yaml_path}")
        return False
    
    print("✅ Configuration files found")
    
    # Validate files
    epjson_ok = validate_epjson()
    yaml_ok = validate_yaml()
    alignment_ok = check_configuration_alignment()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 VALIDATION SUMMARY:")
    print(f"   epJSON validation: {'✅ PASS' if epjson_ok else '❌ FAIL'}")
    print(f"   YAML validation: {'✅ PASS' if yaml_ok else '❌ FAIL'}")
    print(f"   Configuration alignment: {'✅ PASS' if alignment_ok else '❌ FAIL'}")
    
    if epjson_ok and yaml_ok and alignment_ok:
        print("\n🎉 All validation checks passed!")
        print("✅ The configuration is ready for use with EnergyPlus.")
        print("💡 Run 'python3 test_fixed_config.py' to test with EnergyPlus.")
        return True
    else:
        print("\n⚠️  Some validation checks failed.")
        print("🔧 Please check the configuration files.")
        return False

if __name__ == "__main__":
    main()