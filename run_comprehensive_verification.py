#!/usr/bin/env python3
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
    print("\n" + "=" * 80)
    print("RUNNING COMPREHENSIVE HVAC POWER AND ENERGY VERIFICATION")
    print("=" * 80)
    
    try:
        obs, info = env.reset()
        print("Environment reset successfully")
        print(f"Available observation variables: {list(obs.keys())}")
        
        # Store verification data
        verification_data = []
        
        for step in range(10):  # Run 10 steps
            print(f"\n--- Step {step + 1} ---")
            
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
            print("\nPOWER VERIFICATION:")
            print("Individual Component Powers (W):")
            for name, power in components_power.items():
                print(f"  {name}: {power:.2f}")
            
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
            
            # Energy verification using meters
            print("\nENERGY VERIFICATION:")
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
                print(f"\nSimulation ended at step {step + 1}")
                break
        
        # Summary
        print("\n" + "=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80)
        
        if verification_data:
            avg_power_error = sum(d['power_percentage_error'] for d in verification_data) / len(verification_data)
            avg_energy_error = sum(d['energy_percentage_error'] for d in verification_data) / len(verification_data)
            
            print(f"Average Power Error: {avg_power_error:.2f}%")
            print(f"Average Energy Error: {avg_energy_error:.2f}%")
            
            if avg_power_error < 5.0 and avg_energy_error < 5.0:
                print("\n✅ OVERALL VERIFICATION PASSED")
                print("   Total HVAC power and energy correctly calculated as sum of components")
            else:
                print("\n❌ OVERALL VERIFICATION FAILED")
                print("   Significant discrepancies found between calculated and reported totals")
        
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
    success = run_comprehensive_hvac_verification()
    sys.exit(0 if success else 1)
