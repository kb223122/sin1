#!/usr/bin/env python3
"""
Simple HVAC Power Verification Script for 5-Zone Building

This script creates a minimal environment to verify that total HVAC power
equals the sum of individual HVAC components.
"""

import sys
import os
sys.path.append('/workspace')

def create_verification_env():
    """
    Create a 5-zone environment with individual HVAC component variables.
    """
    
    # Import required modules
    try:
        import gymnasium as gym
        import numpy as np
        from sinergym.envs.eplus_env import EplusEnv
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please ensure Sinergym and required packages are installed.")
        return None
    
    # Define variables to capture individual HVAC components
    variables = {
        # Environment variables
        'outdoor_temperature': ('Site Outdoor Air DryBulb Temperature', 'Environment'),
        'air_temperature': ('Zone Air Temperature', 'SPACE5-1'),
        
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
        
        # Total HVAC power
        'HVAC_electricity_demand_rate': ('Facility Total HVAC Electricity Demand Rate', 'Whole Building'),
    }
    
    # Meters for energy verification
    meters = {
        'total_electricity_HVAC': 'Electricity:HVAC',
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
    
    try:
        # Create environment
        env = EplusEnv(
            building_file='5ZoneAutoDXVAV.epJSON',
            weather_files='USA_AZ_Davis-Monthan.AFB.722745_TMY3.epw',
            action_space=action_space,
            time_variables=time_variables,
            variables=variables,
            meters=meters,
            actuators=actuators,
            env_name='5zone_hvac_verification'
        )
        return env
    except Exception as e:
        print(f"Error creating environment: {e}")
        return None

def verify_power_components(env, num_steps=5):
    """
    Verify that total HVAC power equals sum of individual components.
    """
    
    print("=" * 60)
    print("HVAC POWER COMPONENT VERIFICATION")
    print("=" * 60)
    
    # Reset environment
    try:
        obs, info = env.reset()
        print("Environment reset successfully")
    except Exception as e:
        print(f"Error resetting environment: {e}")
        return
    
    print(f"Available observation variables: {list(obs.keys())}")
    
    for step in range(num_steps):
        print(f"\n--- Step {step + 1} ---")
        
        try:
            # Take a random action
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            # Extract individual component powers
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
            
            # Calculate sum of components
            calculated_total = sum(components.values())
            
            # Get total from EnergyPlus
            total_hvac_power = obs.get('HVAC_electricity_demand_rate', 0.0)
            
            # Print results
            print("Individual Component Powers:")
            for name, power in components.items():
                print(f"  {name}: {power:.2f} W")
            
            print(f"\nCalculated Total: {calculated_total:.2f} W")
            print(f"EnergyPlus Total: {total_hvac_power:.2f} W")
            
            # Calculate difference
            difference = abs(total_hvac_power - calculated_total)
            if total_hvac_power > 0:
                percentage_error = (difference / total_hvac_power) * 100
                print(f"Difference: {difference:.2f} W ({percentage_error:.2f}%)")
                
                if percentage_error < 1.0:
                    print("✅ VERIFICATION PASSED")
                else:
                    print("⚠️  VERIFICATION WARNING - Check component definitions")
            else:
                print("ℹ️  No HVAC power consumption at this timestep")
            
            # Check for termination
            if terminated or truncated:
                print(f"\nSimulation ended at step {step + 1}")
                break
                
        except Exception as e:
            print(f"Error in step {step + 1}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("VERIFICATION COMPLETE")
    print("=" * 60)

def main():
    """Main function."""
    
    print("Creating 5-zone environment for HVAC verification...")
    env = create_verification_env()
    
    if env is None:
        print("Failed to create environment. Please check your Sinergym installation.")
        return False
    
    try:
        verify_power_components(env, num_steps=10)
    except Exception as e:
        print(f"Error during verification: {e}")
        return False
    finally:
        env.close()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)