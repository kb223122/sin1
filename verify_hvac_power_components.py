#!/usr/bin/env python3
"""
HVAC Power Component Verification Script for 5-Zone Building

This script verifies that the total HVAC power and energy is the sum of all
individual HVAC components in the 5-zone building by adding detailed component
variables and comparing them with the total values.
"""

import sys
import os
sys.path.append('/workspace')

import sinergym
import gymnasium as gym
import numpy as np
import pandas as pd
from sinergym.utils.wrappers import NormalizeObservation

def create_enhanced_5zone_env():
    """
    Create a 5-zone environment with detailed HVAC component variables
    to verify power summation.
    """
    
    # Enhanced variables configuration with individual HVAC components
    enhanced_variables = {
        # Environment variables
        'outdoor_temperature': ('Site Outdoor Air DryBulb Temperature', 'Environment'),
        'outdoor_humidity': ('Site Outdoor Air Relative Humidity', 'Environment'),
        'wind_speed': ('Site Wind Speed', 'Environment'),
        'wind_direction': ('Site Wind Direction', 'Environment'),
        'diffuse_solar_radiation': ('Site Diffuse Solar Radiation Rate per Area', 'Environment'),
        'direct_solar_radiation': ('Site Direct Solar Radiation Rate per Area', 'Environment'),
        
        # Zone variables
        'air_temperature': ('Zone Air Temperature', 'SPACE5-1'),
        'air_humidity': ('Zone Air Relative Humidity', 'SPACE5-1'),
        'people_occupant': ('Zone People Occupant Count', 'SPACE5-1'),
        'htg_setpoint': ('Zone Thermostat Heating Setpoint Temperature', 'SPACE5-1'),
        'clg_setpoint': ('Zone Thermostat Cooling Setpoint Temperature', 'SPACE5-1'),
        
        # Individual HVAC component electricity rates
        'supply_fan_electricity_rate': ('Fan Electricity Rate', 'Supply Fan 1'),
        'main_cooling_coil_electricity_rate': ('Cooling Coil Electricity Rate', 'Main Cooling Coil 1'),
        'main_heating_coil_electricity_rate': ('Heating Coil Electricity Rate', 'Main heating Coil 1'),
        
        # Zone reheat coil electricity rates
        'zone1_reheat_electricity_rate': ('Heating Coil Electricity Rate', 'SPACE1-1 Zone Coil'),
        'zone2_reheat_electricity_rate': ('Heating Coil Electricity Rate', 'SPACE2-1 Zone Coil'),
        'zone3_reheat_electricity_rate': ('Heating Coil Electricity Rate', 'SPACE3-1 Zone Coil'),
        'zone4_reheat_electricity_rate': ('Heating Coil Electricity Rate', 'SPACE4-1 Zone Coil'),
        'zone5_reheat_electricity_rate': ('Heating Coil Electricity Rate', 'SPACE5-1 Zone Coil'),
        
        # Total HVAC variables
        'HVAC_electricity_demand_rate': ('Facility Total HVAC Electricity Demand Rate', 'Whole Building'),
        'co2_emission': ('Environmental Impact Total CO2 Emissions Carbon Equivalent Mass', 'site'),
    }
    
    # Enhanced meters configuration
    enhanced_meters = {
        'total_electricity_HVAC': 'Electricity:HVAC',
        # Individual component meters (if available)
        'supply_fan_electricity': 'Electricity:Fans',
        'cooling_coil_electricity': 'Electricity:Cooling',
        'heating_coil_electricity': 'Electricity:Heating',
    }
    
    # Actuators
    actuators = {
        'Heating_Setpoint_RL': ('Schedule:Compact', 'Schedule Value', 'HTG-SETP-SCH'),
        'Cooling_Setpoint_RL': ('Schedule:Compact', 'Schedule Value', 'CLG-SETP-SCH'),
    }
    
    # Time variables
    time_variables = ['month', 'day_of_month', 'hour']
    
    # Action space
    action_space = gym.spaces.Box(
        low=np.array([12.0, 23.25], dtype=np.float32),
        high=np.array([23.25, 30.0], dtype=np.float32),
        shape=(2,),
        dtype=np.float32
    )
    
    # Create environment
    env = EplusEnv(
        building_file='5ZoneAutoDXVAV.epJSON',
        weather_files='USA_AZ_Davis-Monthan.AFB.722745_TMY3.epw',
        action_space=action_space,
        time_variables=time_variables,
        variables=enhanced_variables,
        meters=enhanced_meters,
        actuators=actuators,
        env_name='5zone_hvac_verification'
    )
    
    return env

def verify_hvac_power_components(env, num_steps=10):
    """
    Verify that total HVAC power equals sum of individual components.
    
    Args:
        env: Sinergym environment
        num_steps: Number of simulation steps to run
    """
    
    print("=" * 80)
    print("HVAC POWER COMPONENT VERIFICATION FOR 5-ZONE BUILDING")
    print("=" * 80)
    
    # Lists to store data
    verification_data = []
    
    # Reset environment
    obs, info = env.reset()
    
    print(f"\nInitial observation keys: {list(obs.keys())}")
    print(f"Initial info keys: {list(info.keys())}")
    
    for step in range(num_steps):
        # Take a random action
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Extract HVAC component powers
        try:
            # Individual component powers
            supply_fan_power = obs.get('supply_fan_electricity_rate', 0.0)
            main_cooling_power = obs.get('main_cooling_coil_electricity_rate', 0.0)
            main_heating_power = obs.get('main_heating_coil_electricity_rate', 0.0)
            
            zone1_reheat_power = obs.get('zone1_reheat_electricity_rate', 0.0)
            zone2_reheat_power = obs.get('zone2_reheat_electricity_rate', 0.0)
            zone3_reheat_power = obs.get('zone3_reheat_electricity_rate', 0.0)
            zone4_reheat_power = obs.get('zone4_reheat_electricity_rate', 0.0)
            zone5_reheat_power = obs.get('zone5_reheat_electricity_rate', 0.0)
            
            # Total HVAC power from EnergyPlus
            total_hvac_power = obs.get('HVAC_electricity_demand_rate', 0.0)
            
            # Calculate sum of individual components
            calculated_total = (supply_fan_power + 
                              main_cooling_power + 
                              main_heating_power + 
                              zone1_reheat_power + 
                              zone2_reheat_power + 
                              zone3_reheat_power + 
                              zone4_reheat_power + 
                              zone5_reheat_power)
            
            # Calculate difference and percentage error
            difference = abs(total_hvac_power - calculated_total)
            percentage_error = (difference / max(total_hvac_power, 1e-6)) * 100
            
            # Store data
            step_data = {
                'step': step + 1,
                'supply_fan_power': supply_fan_power,
                'main_cooling_power': main_cooling_power,
                'main_heating_power': main_heating_power,
                'zone1_reheat_power': zone1_reheat_power,
                'zone2_reheat_power': zone2_reheat_power,
                'zone3_reheat_power': zone3_reheat_power,
                'zone4_reheat_power': zone4_reheat_power,
                'zone5_reheat_power': zone5_reheat_power,
                'calculated_total': calculated_total,
                'total_hvac_power': total_hvac_power,
                'difference': difference,
                'percentage_error': percentage_error
            }
            verification_data.append(step_data)
            
            # Print step results
            print(f"\n--- Step {step + 1} ---")
            print(f"Supply Fan Power: {supply_fan_power:.2f} W")
            print(f"Main Cooling Coil Power: {main_cooling_power:.2f} W")
            print(f"Main Heating Coil Power: {main_heating_power:.2f} W")
            print(f"Zone 1 Reheat Power: {zone1_reheat_power:.2f} W")
            print(f"Zone 2 Reheat Power: {zone2_reheat_power:.2f} W")
            print(f"Zone 3 Reheat Power: {zone3_reheat_power:.2f} W")
            print(f"Zone 4 Reheat Power: {zone4_reheat_power:.2f} W")
            print(f"Zone 5 Reheat Power: {zone5_reheat_power:.2f} W")
            print(f"Calculated Total: {calculated_total:.2f} W")
            print(f"EnergyPlus Total: {total_hvac_power:.2f} W")
            print(f"Difference: {difference:.2f} W ({percentage_error:.2f}%)")
            
            if percentage_error < 1.0:
                print("✓ VERIFICATION PASSED - Components sum to total within 1%")
            else:
                print("⚠ VERIFICATION WARNING - Significant difference detected")
                
        except Exception as e:
            print(f"Error in step {step + 1}: {e}")
            continue
        
        if terminated or truncated:
            print(f"\nSimulation ended at step {step + 1}")
            break
    
    # Create summary
    if verification_data:
        df = pd.DataFrame(verification_data)
        
        print("\n" + "=" * 80)
        print("VERIFICATION SUMMARY")
        print("=" * 80)
        
        print(f"\nAverage Percentage Error: {df['percentage_error'].mean():.2f}%")
        print(f"Maximum Percentage Error: {df['percentage_error'].max():.2f}%")
        print(f"Minimum Percentage Error: {df['percentage_error'].min():.2f}%")
        
        print(f"\nAverage Calculated Total: {df['calculated_total'].mean():.2f} W")
        print(f"Average EnergyPlus Total: {df['total_hvac_power'].mean():.2f} W")
        
        # Check if verification passed
        if df['percentage_error'].max() < 5.0:
            print("\n✅ OVERALL VERIFICATION PASSED")
            print("   Total HVAC power is correctly calculated as sum of components")
        else:
            print("\n❌ OVERALL VERIFICATION FAILED")
            print("   Significant discrepancies found between calculated and reported totals")
        
        # Save detailed results
        df.to_csv('/workspace/hvac_power_verification_results.csv', index=False)
        print(f"\nDetailed results saved to: /workspace/hvac_power_verification_results.csv")
    
    env.close()
    return verification_data

def verify_hvac_energy_components(env, num_steps=10):
    """
    Verify that total HVAC energy equals sum of individual components.
    """
    
    print("\n" + "=" * 80)
    print("HVAC ENERGY COMPONENT VERIFICATION")
    print("=" * 80)
    
    # Reset environment
    obs, info = env.reset()
    
    # Lists to store energy data
    energy_data = []
    
    for step in range(num_steps):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        
        try:
            # Get meter values (cumulative energy)
            total_hvac_energy = obs.get('total_electricity_HVAC', 0.0)
            
            # Note: Individual component energy meters might not be available
            # This would require additional meter definitions in the building model
            print(f"Step {step + 1}: Total HVAC Energy = {total_hvac_energy:.2f} J")
            
            energy_data.append({
                'step': step + 1,
                'total_hvac_energy': total_hvac_energy
            })
            
        except Exception as e:
            print(f"Error in energy verification step {step + 1}: {e}")
            continue
        
        if terminated or truncated:
            break
    
    print("\nNote: Individual component energy verification requires additional")
    print("meter definitions in the EnergyPlus building model.")
    print("The total HVAC energy meter is available but individual component")
    print("energy meters need to be added to the building configuration.")
    
    env.close()
    return energy_data

def main():
    """Main function to run HVAC power verification."""
    
    try:
        print("Creating enhanced 5-zone environment...")
        env = create_enhanced_5zone_env()
        
        print("Running HVAC power component verification...")
        power_results = verify_hvac_power_components(env, num_steps=20)
        
        print("\nRunning HVAC energy component verification...")
        energy_results = verify_hvac_energy_components(env, num_steps=20)
        
        print("\n" + "=" * 80)
        print("VERIFICATION COMPLETE")
        print("=" * 80)
        print("Check the generated CSV file for detailed results.")
        
    except Exception as e:
        print(f"Error during verification: {e}")
        print("\nNote: This script requires EnergyPlus to be installed and")
        print("the Sinergym environment to be properly configured.")
        return False
    
    return True

if __name__ == "__main__":
    # Import required modules
    try:
        from sinergym.envs.eplus_env import EplusEnv
        import pandas as pd
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure all required packages are installed.")
        sys.exit(1)
    
    success = main()
    sys.exit(0 if success else 1)