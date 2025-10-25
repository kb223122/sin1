#!/usr/bin/env python3
"""
HVAC Verification Script for Fixed 5-Zone Configuration
"""

import sys
import os
sys.path.append('/workspace')

def run_hvac_verification():
    """Run HVAC verification with the fixed configuration."""
    
    try:
        import gymnasium as gym
        import numpy as np
        from sinergym.envs.eplus_env import EplusEnv
        import yaml
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    
    # Load the fixed configuration
    config_file = "/workspace/fixed_5zone_config.yaml"
    
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
        print("✅ Environment created successfully")
    except Exception as e:
        print(f"Error creating environment: {e}")
        return False
    
    # Run verification
    print("\n" + "=" * 80)
    print("RUNNING HVAC VERIFICATION WITH FIXED CONFIGURATION")
    print("=" * 80)
    
    try:
        obs, info = env.reset()
        print("Environment reset successfully")
        
        for step in range(5):
            print(f"\n--- Step {step + 1} ---")
            
            # Take random action
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            # METER-BASED ENERGY VERIFICATION
            print("\nMETER-BASED ENERGY VERIFICATION:")
            total_hvac_energy = obs.get('total_electricity_HVAC', 0.0)
            heating_energy = obs.get('heating_electricity', 0.0)
            fans_energy = obs.get('fans_electricity', 0.0)
            cooling_energy = obs.get('cooling_electricity', 0.0)
            
            print(f"Total HVAC Energy: {total_hvac_energy:.2f} J")
            print(f"Heating Energy: {heating_energy:.2f} J")
            print(f"Fans Energy: {fans_energy:.2f} J")
            print(f"Cooling Energy: {cooling_energy:.2f} J")
            
            calculated_total_energy = heating_energy + fans_energy + cooling_energy
            if total_hvac_energy > 0:
                energy_difference = abs(total_hvac_energy - calculated_total_energy)
                energy_percentage_error = (energy_difference / total_hvac_energy) * 100
                print(f"Calculated Total: {calculated_total_energy:.2f} J")
                print(f"Energy Difference: {energy_difference:.2f} J ({energy_percentage_error:.2f}%)")
                
                if energy_percentage_error < 5.0:
                    print("✅ ENERGY VERIFICATION PASSED")
                else:
                    print("⚠️  ENERGY VERIFICATION WARNING")
            
            # COMPONENT-BASED POWER VERIFICATION
            print("\nCOMPONENT-BASED POWER VERIFICATION:")
            total_hvac_power = obs.get('HVAC_electricity_demand_rate', 0.0)
            
            # Central system components
            central_components = {
                'Supply Fan': obs.get('fan_electricity_rate', 0.0),
                'Main Heating Coil': obs.get('heating_coil_electricity_rate', 0.0),
                'Main Cooling Coil': obs.get('cooling_coil_electricity_rate', 0.0),
            }
            
            # Zone reheat components
            zone_components = {
                'Zone 1 Reheat': obs.get('reheat_power_space1', 0.0),
                'Zone 2 Reheat': obs.get('reheat_power_space2', 0.0),
                'Zone 3 Reheat': obs.get('reheat_power_space3', 0.0),
                'Zone 4 Reheat': obs.get('reheat_power_space4', 0.0),
                'Zone 5 Reheat': obs.get('reheat_power_space5', 0.0),
            }
            
            print("Central System Components:")
            for name, power in central_components.items():
                print(f"  {name}: {power:.2f} W")
            
            print("\nZone Reheat Components:")
            for name, power in zone_components.items():
                print(f"  {name}: {power:.2f} W")
            
            calculated_total_power = sum(central_components.values()) + sum(zone_components.values())
            print(f"\nCalculated Total Power: {calculated_total_power:.2f} W")
            print(f"EnergyPlus Total Power: {total_hvac_power:.2f} W")
            
            if total_hvac_power > 0:
                power_difference = abs(total_hvac_power - calculated_total_power)
                power_percentage_error = (power_difference / total_hvac_power) * 100
                print(f"Power Difference: {power_difference:.2f} W ({power_percentage_error:.2f}%)")
                
                if power_percentage_error < 5.0:
                    print("✅ POWER VERIFICATION PASSED")
                else:
                    print("⚠️  POWER VERIFICATION WARNING")
            
            if terminated or truncated:
                break
        
        print("\n" + "=" * 80)
        print("VERIFICATION COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error during verification: {e}")
        return False
    finally:
        env.close()
    
    return True

if __name__ == "__main__":
    success = run_hvac_verification()
    sys.exit(0 if success else 1)
