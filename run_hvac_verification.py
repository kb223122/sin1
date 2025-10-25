#!/usr/bin/env python3
"""
Complete HVAC Power Verification Script for 5-Zone Building

This script provides multiple ways to verify that total HVAC power equals
the sum of individual components in the 5-zone building.
"""

import sys
import os
import json
import yaml

def print_hvac_components_summary():
    """Print a summary of HVAC components in the 5-zone building."""
    
    print("=" * 80)
    print("5-ZONE BUILDING HVAC COMPONENTS SUMMARY")
    print("=" * 80)
    
    print("\nHVAC SYSTEM ARCHITECTURE:")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│                    CENTRAL HVAC SYSTEM                     │")
    print("├─────────────────────────────────────────────────────────────┤")
    print("│ 1. Supply Fan 1 (Variable Volume)                         │")
    print("│ 2. Main Cooling Coil 1 (Two-Speed DX)                     │")
    print("│ 3. Main Heating Coil 1 (Electric)                         │")
    print("└─────────────────────────────────────────────────────────────┘")
    print("                              │")
    print("                              ▼")
    print("┌─────────────────────────────────────────────────────────────┐")
    print("│                    ZONE HVAC SYSTEMS                       │")
    print("├─────────────────────────────────────────────────────────────┤")
    print("│ Zone 1: VAV Reheat + SPACE1-1 Zone Coil (Electric)        │")
    print("│ Zone 2: VAV Reheat + SPACE2-1 Zone Coil (Electric)        │")
    print("│ Zone 3: VAV Reheat + SPACE3-1 Zone Coil (Electric)        │")
    print("│ Zone 4: VAV Reheat + SPACE4-1 Zone Coil (Electric)        │")
    print("│ Zone 5: VAV Reheat + SPACE5-1 Zone Coil (Electric)        │")
    print("└─────────────────────────────────────────────────────────────┘")
    
    print("\nTOTAL HVAC POWER CALCULATION:")
    print("Total HVAC Power = Supply Fan Power + Main Cooling Coil Power + Main Heating Coil Power +")
    print("                   Zone1 Reheat Power + Zone2 Reheat Power + Zone3 Reheat Power +")
    print("                   Zone4 Reheat Power + Zone5 Reheat Power")
    
    print("\nCOMPONENTS BREAKDOWN:")
    print("• Central System: 3 components (Fan + Cooling + Heating)")
    print("• Zone Systems: 5 components (one reheat coil per zone)")
    print("• Total Components: 8 electrical components")

def create_verification_environment():
    """Create a Sinergym environment configuration for verification."""
    
    print("\n" + "=" * 80)
    print("CREATING VERIFICATION ENVIRONMENT CONFIGURATION")
    print("=" * 80)
    
    # Enhanced configuration with all HVAC components
    config = {
        "id_base": "5zone_hvac_verification",
        "building_file": "5ZoneAutoDXVAV.epJSON",
        "weather_specification": {
            "weather_files": ["USA_AZ_Davis-Monthan.AFB.722745_TMY3.epw"],
            "keys": ["hot"]
        },
        "time_variables": ["month", "day_of_month", "hour"],
        "variables": {
            # Environment variables
            "Site Outdoor Air DryBulb Temperature": {
                "variable_names": "outdoor_temperature",
                "keys": "Environment"
            },
            "Zone Air Temperature": {
                "variable_names": "air_temperature",
                "keys": "SPACE5-1"
            },
            
            # Individual HVAC component electricity rates
            "Fan Electricity Rate": {
                "variable_names": "supply_fan_electricity_rate",
                "keys": "Supply Fan 1"
            },
            "Cooling Coil Electricity Rate": {
                "variable_names": "main_cooling_coil_electricity_rate",
                "keys": "Main Cooling Coil 1"
            },
            "Heating Coil Electricity Rate": {
                "variable_names": "main_heating_coil_electricity_rate",
                "keys": "Main heating Coil 1"
            },
            "Heating Coil Electricity Rate": {
                "variable_names": "zone1_reheat_electricity_rate",
                "keys": "SPACE1-1 Zone Coil"
            },
            "Heating Coil Electricity Rate": {
                "variable_names": "zone2_reheat_electricity_rate",
                "keys": "SPACE2-1 Zone Coil"
            },
            "Heating Coil Electricity Rate": {
                "variable_names": "zone3_reheat_electricity_rate",
                "keys": "SPACE3-1 Zone Coil"
            },
            "Heating Coil Electricity Rate": {
                "variable_names": "zone4_reheat_electricity_rate",
                "keys": "SPACE4-1 Zone Coil"
            },
            "Heating Coil Electricity Rate": {
                "variable_names": "zone5_reheat_electricity_rate",
                "keys": "SPACE5-1 Zone Coil"
            },
            
            # Total HVAC power
            "Facility Total HVAC Electricity Demand Rate": {
                "variable_names": "HVAC_electricity_demand_rate",
                "keys": "Whole Building"
            }
        },
        "meters": {
            "Electricity:HVAC": "total_electricity_HVAC",
            "Electricity:Fans": "supply_fan_electricity",
            "Electricity:Cooling": "cooling_coil_electricity",
            "Electricity:Heating": "heating_coil_electricity"
        },
        "actuators": {
            "HTG-SETP-SCH": {
                "variable_name": "Heating_Setpoint_RL",
                "element_type": "Schedule:Compact",
                "value_type": "Schedule Value"
            },
            "CLG-SETP-SCH": {
                "variable_name": "Cooling_Setpoint_RL",
                "element_type": "Schedule:Compact",
                "value_type": "Schedule Value"
            }
        },
        "action_space": "gym.spaces.Box(low=np.array([12.0, 23.25], dtype=np.float32), high=np.array([23.25, 30.0], dtype=np.float32), shape=(2,), dtype=np.float32)"
    }
    
    # Save configuration
    config_file = "/workspace/5zone_hvac_verification_config.yaml"
    try:
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Verification configuration saved to: {config_file}")
        return config_file
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return None

def create_verification_script():
    """Create a Python script to run the verification."""
    
    script_content = '''#!/usr/bin/env python3
"""
HVAC Power Verification Script - Generated
"""

import sys
import os
sys.path.append('/workspace')

def run_hvac_verification():
    """Run the HVAC power verification."""
    
    try:
        import gymnasium as gym
        import numpy as np
        from sinergym.envs.eplus_env import EplusEnv
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure Sinergym and required packages are installed.")
        return False
    
    # Load the verification configuration
    config_file = "/workspace/5zone_hvac_verification_config.yaml"
    
    try:
        import yaml
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
        print("✅ Environment created successfully")
    except Exception as e:
        print(f"Error creating environment: {e}")
        return False
    
    # Run verification
    print("\\n" + "=" * 60)
    print("RUNNING HVAC POWER VERIFICATION")
    print("=" * 60)
    
    try:
        obs, info = env.reset()
        print("Environment reset successfully")
        
        for step in range(5):  # Run 5 steps
            print(f"\\n--- Step {step + 1} ---")
            
            # Take random action
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            # Extract component powers
            components = {
                'Supply Fan': obs.get('supply_fan_electricity_rate', 0.0),
                'Main Cooling Coil': obs.get('main_cooling_coil_electricity_rate', 0.0),
                'Main Heating Coil': obs.get('main_heating_coil_electricity_rate', 0.0),
                'Zone 1 Reheat': obs.get('zone1_reheat_electricity_rate', 0.0),
                'Zone 2 Reheat': obs.get('zone2_reheat_electricity_rate', 0.0),
                'Zone 3 Reheat': obs.get('zone3_reheat_electricity_rate', 0.0),
                'Zone 4 Reheat': obs.get('zone4_reheat_electricity_rate', 0.0),
                'Zone 5 Reheat': obs.get('zone5_reheat_electricity_rate', 0.0),
            }
            
            # Calculate sum
            calculated_total = sum(components.values())
            total_hvac_power = obs.get('HVAC_electricity_demand_rate', 0.0)
            
            # Print results
            print("Component Powers (W):")
            for name, power in components.items():
                print(f"  {name}: {power:.2f}")
            
            print(f"\\nCalculated Total: {calculated_total:.2f} W")
            print(f"EnergyPlus Total: {total_hvac_power:.2f} W")
            
            if total_hvac_power > 0:
                difference = abs(total_hvac_power - calculated_total)
                percentage_error = (difference / total_hvac_power) * 100
                print(f"Difference: {difference:.2f} W ({percentage_error:.2f}%)")
                
                if percentage_error < 5.0:
                    print("✅ VERIFICATION PASSED")
                else:
                    print("⚠️  VERIFICATION WARNING")
            
            if terminated or truncated:
                break
        
        print("\\n" + "=" * 60)
        print("VERIFICATION COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error during verification: {e}")
        return False
    finally:
        env.close()
    
    return True

if __name__ == "__main__":
    success = run_hvac_verification()
    sys.exit(0 if success else 1)
'''
    
    script_file = "/workspace/run_verification.py"
    try:
        with open(script_file, 'w') as f:
            f.write(script_content)
        os.chmod(script_file, 0o755)  # Make executable
        print(f"✅ Verification script saved to: {script_file}")
        return script_file
    except Exception as e:
        print(f"Error saving script: {e}")
        return None

def print_verification_instructions():
    """Print instructions for running the verification."""
    
    print("\n" + "=" * 80)
    print("HOW TO RUN HVAC POWER VERIFICATION")
    print("=" * 80)
    
    print("\nMETHOD 1: Run the generated script")
    print("  python3 /workspace/run_verification.py")
    
    print("\nMETHOD 2: Use the configuration in your own code")
    print("  from sinergym.envs.eplus_env import EplusEnv")
    print("  import yaml")
    print("  # Load config and create environment")
    
    print("\nMETHOD 3: Manual verification")
    print("  1. Create environment with individual component variables")
    print("  2. Run simulation and collect power data")
    print("  3. Sum individual components and compare with total")
    
    print("\nEXPECTED RESULT:")
    print("  Sum(Individual Components) ≈ Total HVAC Power")
    print("  Difference should be < 5%")
    
    print("\nCOMPONENTS TO VERIFY:")
    print("  • Supply Fan 1")
    print("  • Main Cooling Coil 1")
    print("  • Main Heating Coil 1")
    print("  • SPACE1-1 Zone Coil")
    print("  • SPACE2-1 Zone Coil")
    print("  • SPACE3-1 Zone Coil")
    print("  • SPACE4-1 Zone Coil")
    print("  • SPACE5-1 Zone Coil")

def main():
    """Main function."""
    
    print_hvac_components_summary()
    
    config_file = create_verification_environment()
    if config_file:
        script_file = create_verification_script()
        if script_file:
            print_verification_instructions()
        else:
            print("❌ Failed to create verification script")
    else:
        print("❌ Failed to create verification configuration")

if __name__ == "__main__":
    main()