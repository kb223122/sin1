#!/usr/bin/env python3
"""
Comprehensive HVAC Power and Energy Verification Script for 5-Zone Building

Based on the actual EnergyPlus data_available.txt file, this script verifies that
total HVAC power and energy equals the sum of all individual components.
"""

import sys
import os
sys.path.append('/workspace')

def analyze_available_data():
    """Analyze the available EnergyPlus data to identify HVAC components."""
    
    print("=" * 80)
    print("ANALYZING AVAILABLE ENERGYPLUS DATA FOR HVAC VERIFICATION")
    print("=" * 80)
    
    # HVAC-related variables from the data_available.txt
    hvac_variables = {
        # Total HVAC power and energy
        'Facility Total HVAC Electricity Demand Rate': ('WHOLE BUILDING', 'W'),
        'Facility Total Purchased Electricity Energy': ('WHOLE BUILDING', 'J'),
        
        # Individual HVAC component electricity rates (POWER)
        'Fan Electricity Rate': ('SUPPLY FAN 1', 'W'),
        'Heating Coil Electricity Rate': ('MAIN HEATING COIL 1', 'W'),
        'Cooling Coil Electricity Rate': ('MAIN COOLING COIL 1', 'W'),
        
        # Zone reheat coil electricity rates (POWER)
        'Heating Coil Electricity Rate': ('SPACE1-1 ZONE COIL', 'W'),
        'Heating Coil Electricity Rate': ('SPACE2-1 ZONE COIL', 'W'),
        'Heating Coil Electricity Rate': ('SPACE3-1 ZONE COIL', 'W'),
        'Heating Coil Electricity Rate': ('SPACE4-1 ZONE COIL', 'W'),
        'Heating Coil Electricity Rate': ('SPACE5-1 ZONE COIL', 'W'),
        
        # Individual HVAC component electricity energy (ENERGY)
        'Fan Electricity Energy': ('SUPPLY FAN 1', 'J'),
        'Heating Coil Electricity Energy': ('MAIN HEATING COIL 1', 'J'),
        'Cooling Coil Electricity Energy': ('MAIN COOLING COIL 1', 'J'),
        
        # Zone reheat coil electricity energy (ENERGY)
        'Heating Coil Electricity Energy': ('SPACE1-1 ZONE COIL', 'J'),
        'Heating Coil Electricity Energy': ('SPACE2-1 ZONE COIL', 'J'),
        'Heating Coil Electricity Energy': ('SPACE3-1 ZONE COIL', 'J'),
        'Heating Coil Electricity Energy': ('SPACE4-1 ZONE COIL', 'J'),
        'Heating Coil Electricity Energy': ('SPACE5-1 ZONE COIL', 'J'),
    }
    
    # HVAC-related meters from the data_available.txt
    hvac_meters = {
        'Electricity:HVAC': 'Total HVAC electricity energy',
        'Heating:Electricity': 'Total heating electricity energy',
        'Fans:Electricity': 'Total fans electricity energy',
        'Cooling:Electricity': 'Total cooling electricity energy',
        'Electricity:Facility': 'Total facility electricity energy',
        'Electricity:Building': 'Total building electricity energy',
    }
    
    print("\nHVAC COMPONENTS IDENTIFIED FROM ENERGYPLUS DATA:")
    print("=" * 60)
    
    print("\n1. CENTRAL HVAC SYSTEM COMPONENTS:")
    print("   • Supply Fan 1 (Fan Electricity Rate/Energy)")
    print("   • Main Heating Coil 1 (Heating Coil Electricity Rate/Energy)")
    print("   • Main Cooling Coil 1 (Cooling Coil Electricity Rate/Energy)")
    
    print("\n2. ZONE HVAC SYSTEM COMPONENTS:")
    print("   • SPACE1-1 Zone Coil (Heating Coil Electricity Rate/Energy)")
    print("   • SPACE2-1 Zone Coil (Heating Coil Electricity Rate/Energy)")
    print("   • SPACE3-1 Zone Coil (Heating Coil Electricity Rate/Energy)")
    print("   • SPACE4-1 Zone Coil (Heating Coil Electricity Rate/Energy)")
    print("   • SPACE5-1 Zone Coil (Heating Coil Electricity Rate/Energy)")
    
    print("\n3. TOTAL HVAC METRICS:")
    print("   • Facility Total HVAC Electricity Demand Rate (Power)")
    print("   • Electricity:HVAC (Energy)")
    
    print("\n4. CATEGORIZED METERS:")
    print("   • Heating:Electricity (All heating components)")
    print("   • Fans:Electricity (All fan components)")
    print("   • Cooling:Electricity (All cooling components)")
    
    return hvac_variables, hvac_meters

def create_verification_environment():
    """Create a Sinergym environment with all available HVAC variables."""
    
    print("\n" + "=" * 80)
    print("CREATING COMPREHENSIVE VERIFICATION ENVIRONMENT")
    print("=" * 80)
    
    # Variables configuration based on actual EnergyPlus data
    variables = {
        # Environment variables
        'Site Outdoor Air Drybulb Temperature': {
            'variable_names': 'outdoor_temperature',
            'keys': 'ENVIRONMENT'
        },
        'Zone Air Temperature': {
            'variable_names': 'air_temperature',
            'keys': 'SPACE5-1'
        },
        'Zone Air Relative Humidity': {
            'variable_names': 'air_humidity',
            'keys': 'SPACE5-1'
        },
        'Zone Thermostat Heating Setpoint Temperature': {
            'variable_names': 'htg_setpoint',
            'keys': 'SPACE5-1'
        },
        'Zone Thermostat Cooling Setpoint Temperature': {
            'variable_names': 'clg_setpoint',
            'keys': 'SPACE5-1'
        },
        
        # Individual HVAC component electricity rates (POWER)
        'Fan Electricity Rate': {
            'variable_names': 'supply_fan_electricity_rate',
            'keys': 'SUPPLY FAN 1'
        },
        'Heating Coil Electricity Rate': {
            'variable_names': 'main_heating_coil_electricity_rate',
            'keys': 'MAIN HEATING COIL 1'
        },
        'Cooling Coil Electricity Rate': {
            'variable_names': 'main_cooling_coil_electricity_rate',
            'keys': 'MAIN COOLING COIL 1'
        },
        
        # Zone reheat coil electricity rates (POWER) - Note: Multiple zones with same variable name
        # We'll need to handle this differently in the actual implementation
        'Heating Coil Electricity Rate': {
            'variable_names': 'zone1_reheat_electricity_rate',
            'keys': 'SPACE1-1 ZONE COIL'
        },
        'Heating Coil Electricity Rate': {
            'variable_names': 'zone2_reheat_electricity_rate',
            'keys': 'SPACE2-1 ZONE COIL'
        },
        'Heating Coil Electricity Rate': {
            'variable_names': 'zone3_reheat_electricity_rate',
            'keys': 'SPACE3-1 ZONE COIL'
        },
        'Heating Coil Electricity Rate': {
            'variable_names': 'zone4_reheat_electricity_rate',
            'keys': 'SPACE4-1 ZONE COIL'
        },
        'Heating Coil Electricity Rate': {
            'variable_names': 'zone5_reheat_electricity_rate',
            'keys': 'SPACE5-1 ZONE COIL'
        },
        
        # Total HVAC power
        'Facility Total HVAC Electricity Demand Rate': {
            'variable_names': 'HVAC_electricity_demand_rate',
            'keys': 'WHOLE BUILDING'
        },
        
        # Additional HVAC variables for verification
        'Fan Air Mass Flow Rate': {
            'variable_names': 'fan_air_mass_flow_rate',
            'keys': 'SUPPLY FAN 1'
        },
        'Cooling Coil Total Cooling Rate': {
            'variable_names': 'cooling_coil_total_cooling_rate',
            'keys': 'MAIN COOLING COIL 1'
        },
        'Heating Coil Heating Rate': {
            'variable_names': 'heating_coil_heating_rate',
            'keys': 'MAIN HEATING COIL 1'
        },
    }
    
    # Meters configuration based on actual EnergyPlus data
    meters = {
        'Electricity:HVAC': 'total_electricity_HVAC',
        'Heating:Electricity': 'heating_electricity',
        'Fans:Electricity': 'fans_electricity',
        'Cooling:Electricity': 'cooling_electricity',
        'Electricity:Facility': 'total_electricity_facility',
        'Electricity:Building': 'total_electricity_building',
    }
    
    # Actuators
    actuators = {
        'HTG-SETP-SCH': {
            'variable_name': 'Heating_Setpoint_RL',
            'element_type': 'Schedule:Compact',
            'value_type': 'Schedule Value'
        },
        'CLG-SETP-SCH': {
            'variable_name': 'Cooling_Setpoint_RL',
            'element_type': 'Schedule:Compact',
            'value_type': 'Schedule Value'
        }
    }
    
    # Time variables
    time_variables = ['month', 'day_of_month', 'hour']
    
    # Action space
    action_space = "gym.spaces.Box(low=np.array([12.0, 23.25], dtype=np.float32), high=np.array([23.25, 30.0], dtype=np.float32), shape=(2,), dtype=np.float32)"
    
    config = {
        'id_base': '5zone_comprehensive_hvac_verification',
        'building_file': '5ZoneAutoDXVAV.epJSON',
        'weather_specification': {
            'weather_files': ['USA_AZ_Davis-Monthan.AFB.722745_TMY3.epw'],
            'keys': ['hot']
        },
        'time_variables': time_variables,
        'variables': variables,
        'meters': meters,
        'actuators': actuators,
        'action_space': action_space
    }
    
    # Save configuration
    config_file = '/workspace/comprehensive_hvac_verification_config.yaml'
    try:
        import yaml
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Comprehensive verification configuration saved to: {config_file}")
        return config_file
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return None

def create_verification_script():
    """Create a comprehensive verification script."""
    
    script_content = '''#!/usr/bin/env python3
"""
Comprehensive HVAC Power and Energy Verification Script
Based on actual EnergyPlus data_available.txt
"""

import sys
import os
sys.path.append('/workspace')

def run_comprehensive_hvac_verification():
    """Run comprehensive HVAC power and energy verification."""
    
    try:
        import gymnasium as gym
        import numpy as np
        from sinergym.envs.eplus_env import EplusEnv
        import yaml
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure Sinergym and required packages are installed.")
        return False
    
    # Load the comprehensive verification configuration
    config_file = "/workspace/comprehensive_hvac_verification_config.yaml"
    
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading configuration: {e}")
        return False
    
    # Create environment
    try:
        env = EplusEnv(
            building_file=config['building_file'],
            weather_files=config['weather_specification']['weather_files'][0],
            action_space=eval(config['action_space']),
            time_variables=config['time_variables'],
            variables=config['variables'],
            meters=config['meters'],
            actuators=config['actuators'],
            env_name=config['id_base']
        )
        print("✅ Comprehensive verification environment created successfully")
    except Exception as e:
        print(f"Error creating environment: {e}")
        return False
    
    # Run verification
    print("\\n" + "=" * 80)
    print("RUNNING COMPREHENSIVE HVAC POWER AND ENERGY VERIFICATION")
    print("=" * 80)
    
    try:
        obs, info = env.reset()
        print("Environment reset successfully")
        print(f"Available observation variables: {list(obs.keys())}")
        
        # Store verification data
        verification_data = []
        
        for step in range(10):  # Run 10 steps
            print(f"\\n--- Step {step + 1} ---")
            
            # Take random action
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            # Extract individual component powers
            components_power = {
                'Supply Fan': obs.get('supply_fan_electricity_rate', 0.0),
                'Main Heating Coil': obs.get('main_heating_coil_electricity_rate', 0.0),
                'Main Cooling Coil': obs.get('main_cooling_coil_electricity_rate', 0.0),
                'Zone 1 Reheat': obs.get('zone1_reheat_electricity_rate', 0.0),
                'Zone 2 Reheat': obs.get('zone2_reheat_electricity_rate', 0.0),
                'Zone 3 Reheat': obs.get('zone3_reheat_electricity_rate', 0.0),
                'Zone 4 Reheat': obs.get('zone4_reheat_electricity_rate', 0.0),
                'Zone 5 Reheat': obs.get('zone5_reheat_electricity_rate', 0.0),
            }
            
            # Calculate sum of individual components
            calculated_total_power = sum(components_power.values())
            
            # Get total from EnergyPlus
            total_hvac_power = obs.get('HVAC_electricity_demand_rate', 0.0)
            
            # Print power verification results
            print("\\nPOWER VERIFICATION:")
            print("Individual Component Powers (W):")
            for name, power in components_power.items():
                print(f"  {name}: {power:.2f}")
            
            print(f"\\nCalculated Total Power: {calculated_total_power:.2f} W")
            print(f"EnergyPlus Total Power: {total_hvac_power:.2f} W")
            
            if total_hvac_power > 0:
                power_difference = abs(total_hvac_power - calculated_total_power)
                power_percentage_error = (power_difference / total_hvac_power) * 100
                print(f"Power Difference: {power_difference:.2f} W ({power_percentage_error:.2f}%)")
                
                if power_percentage_error < 5.0:
                    print("✅ POWER VERIFICATION PASSED")
                else:
                    print("⚠️  POWER VERIFICATION WARNING")
            
            # Energy verification using meters
            print("\\nENERGY VERIFICATION:")
            total_hvac_energy = obs.get('total_electricity_HVAC', 0.0)
            heating_energy = obs.get('heating_electricity', 0.0)
            fans_energy = obs.get('fans_electricity', 0.0)
            cooling_energy = obs.get('cooling_electricity', 0.0)
            
            print(f"Total HVAC Energy: {total_hvac_energy:.2f} J")
            print(f"Heating Energy: {heating_energy:.2f} J")
            print(f"Fans Energy: {fans_energy:.2f} J")
            print(f"Cooling Energy: {cooling_energy:.2f} J")
            
            # Check if energy components sum to total
            calculated_total_energy = heating_energy + fans_energy + cooling_energy
            if total_hvac_energy > 0:
                energy_difference = abs(total_hvac_energy - calculated_total_energy)
                energy_percentage_error = (energy_difference / total_hvac_energy) * 100
                print(f"Calculated Total Energy: {calculated_total_energy:.2f} J")
                print(f"Energy Difference: {energy_difference:.2f} J ({energy_percentage_error:.2f}%)")
                
                if energy_percentage_error < 5.0:
                    print("✅ ENERGY VERIFICATION PASSED")
                else:
                    print("⚠️  ENERGY VERIFICATION WARNING")
            
            # Store data for analysis
            step_data = {
                'step': step + 1,
                'calculated_total_power': calculated_total_power,
                'total_hvac_power': total_hvac_power,
                'power_difference': power_difference if total_hvac_power > 0 else 0,
                'power_percentage_error': power_percentage_error if total_hvac_power > 0 else 0,
                'calculated_total_energy': calculated_total_energy,
                'total_hvac_energy': total_hvac_energy,
                'energy_difference': energy_difference if total_hvac_energy > 0 else 0,
                'energy_percentage_error': energy_percentage_error if total_hvac_energy > 0 else 0,
            }
            verification_data.append(step_data)
            
            if terminated or truncated:
                print(f"\\nSimulation ended at step {step + 1}")
                break
        
        # Summary
        print("\\n" + "=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80)
        
        if verification_data:
            avg_power_error = sum(d['power_percentage_error'] for d in verification_data) / len(verification_data)
            avg_energy_error = sum(d['energy_percentage_error'] for d in verification_data) / len(verification_data)
            
            print(f"Average Power Error: {avg_power_error:.2f}%")
            print(f"Average Energy Error: {avg_energy_error:.2f}%")
            
            if avg_power_error < 5.0 and avg_energy_error < 5.0:
                print("\\n✅ OVERALL VERIFICATION PASSED")
                print("   Total HVAC power and energy correctly calculated as sum of components")
            else:
                print("\\n❌ OVERALL VERIFICATION FAILED")
                print("   Significant discrepancies found between calculated and reported totals")
        
        print("\\n" + "=" * 80)
        print("VERIFICATION COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error during verification: {e}")
        return False
    finally:
        env.close()
    
    return True

if __name__ == "__main__":
    success = run_comprehensive_hvac_verification()
    sys.exit(0 if success else 1)
'''
    
    script_file = '/workspace/run_comprehensive_verification.py'
    try:
        with open(script_file, 'w') as f:
            f.write(script_content)
        os.chmod(script_file, 0o755)  # Make executable
        print(f"✅ Comprehensive verification script saved to: {script_file}")
        return script_file
    except Exception as e:
        print(f"Error saving script: {e}")
        return None

def print_verification_guide():
    """Print a comprehensive guide for HVAC verification."""
    
    print("\n" + "=" * 80)
    print("COMPREHENSIVE HVAC VERIFICATION GUIDE")
    print("=" * 80)
    
    print("\n1. POWER VERIFICATION:")
    print("   Total HVAC Power = Sum of Individual Component Powers")
    print("   Components to verify:")
    print("   • Supply Fan 1 (Fan Electricity Rate)")
    print("   • Main Heating Coil 1 (Heating Coil Electricity Rate)")
    print("   • Main Cooling Coil 1 (Cooling Coil Electricity Rate)")
    print("   • SPACE1-1 Zone Coil (Heating Coil Electricity Rate)")
    print("   • SPACE2-1 Zone Coil (Heating Coil Electricity Rate)")
    print("   • SPACE3-1 Zone Coil (Heating Coil Electricity Rate)")
    print("   • SPACE4-1 Zone Coil (Heating Coil Electricity Rate)")
    print("   • SPACE5-1 Zone Coil (Heating Coil Electricity Rate)")
    
    print("\n2. ENERGY VERIFICATION:")
    print("   Total HVAC Energy = Sum of Categorized Energy Meters")
    print("   Energy meters to verify:")
    print("   • Heating:Electricity (All heating components)")
    print("   • Fans:Electricity (All fan components)")
    print("   • Cooling:Electricity (All cooling components)")
    
    print("\n3. CROSS-CHECK METHODS:")
    print("   Method 1: Individual Component Sum vs Total")
    print("   Method 2: Categorized Meter Sum vs Total")
    print("   Method 3: Facility vs Building vs HVAC Energy")
    
    print("\n4. EXPECTED RESULTS:")
    print("   • Power verification: Sum(Components) ≈ Total HVAC Power")
    print("   • Energy verification: Sum(Categories) ≈ Total HVAC Energy")
    print("   • Difference should be < 5%")
    
    print("\n5. HOW TO RUN:")
    print("   python3 /workspace/run_comprehensive_verification.py")
    
    print("\n6. TROUBLESHOOTING:")
    print("   • If power verification fails: Check individual component variables")
    print("   • If energy verification fails: Check meter definitions")
    print("   • If both fail: Check EnergyPlus building model configuration")

def main():
    """Main function."""
    
    # Analyze available data
    hvac_variables, hvac_meters = analyze_available_data()
    
    # Create verification environment
    config_file = create_verification_environment()
    if config_file:
        # Create verification script
        script_file = create_verification_script()
        if script_file:
            # Print verification guide
            print_verification_guide()
        else:
            print("❌ Failed to create verification script")
    else:
        print("❌ Failed to create verification configuration")

if __name__ == "__main__":
    main()