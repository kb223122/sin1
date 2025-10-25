#!/usr/bin/env python3
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
    print("\n" + "=" * 60)
    print("RUNNING HVAC POWER VERIFICATION")
    print("=" * 60)
    
    try:
        obs, info = env.reset()
        print("Environment reset successfully")
        
        for step in range(5):  # Run 5 steps
            print(f"\n--- Step {step + 1} ---")
            
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
            
            print(f"\nCalculated Total: {calculated_total:.2f} W")
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
        
        print("\n" + "=" * 60)
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
