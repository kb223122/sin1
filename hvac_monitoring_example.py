#!/usr/bin/env python3
"""
HVAC Component Monitoring Example for Sinergym 5Zone Environment

This script demonstrates how to monitor and print HVAC component status
and power consumption at each simulation step using the modified 5Zone
environment configuration.

The script shows how to:
1. Access real-time HVAC component data
2. Print component status and power consumption
3. Monitor system performance metrics
4. Track energy consumption patterns
"""

import gymnasium as gym
import numpy as np
import sinergym
from sinergym.utils.rewards import LinearReward
import time
import pandas as pd
from datetime import datetime

def print_hvac_status(obs, step, timestamp=None):
    """
    Print comprehensive HVAC component status and power consumption.
    
    Args:
        obs (dict): Observation dictionary from environment
        step (int): Current simulation step
        timestamp (str): Optional timestamp string
    """
    print(f"\n{'='*80}")
    print(f"HVAC COMPONENT STATUS - Step {step}")
    if timestamp:
        print(f"Timestamp: {timestamp}")
    print(f"{'='*80}")
    
    # System Overview
    print(f"\n🏢 SYSTEM OVERVIEW:")
    print(f"   Outdoor Air Economizer Status: {obs.get('outdoor_air_economizer_status', 'N/A')}")
    print(f"   Outdoor Air Flow Fraction: {obs.get('outdoor_air_flow_fraction', 'N/A'):.3f}")
    print(f"   Mixed Air Mass Flow Rate: {obs.get('mixed_air_mass_flow_rate', 'N/A'):.3f} kg/s")
    print(f"   Mixed Air Temperature: {obs.get('mixed_air_temp', 'N/A'):.2f}°C")
    
    # Supply Fan Status
    print(f"\n🌀 SUPPLY FAN (Supply Fan 1):")
    print(f"   Electricity Rate: {obs.get('fan_electricity_rate', 'N/A'):.2f} W")
    print(f"   Air Mass Flow Rate: {obs.get('fan_air_mass_flow_rate', 'N/A'):.3f} kg/s")
    print(f"   Rise in Air Temperature: {obs.get('fan_rise_air_temp', 'N/A'):.2f}°C")
    print(f"   Heat Gain to Air: {obs.get('fan_heat_gain', 'N/A'):.2f} W")
    
    # Main Cooling Coil Status
    print(f"\n❄️  MAIN COOLING COIL (Main Cooling Coil 1):")
    print(f"   Total Cooling Rate: {obs.get('cooling_coil_total_rate', 'N/A'):.2f} W")
    print(f"   Sensible Cooling Rate: {obs.get('cooling_coil_sensible_rate', 'N/A'):.2f} W")
    print(f"   Latent Cooling Rate: {obs.get('cooling_coil_latent_rate', 'N/A'):.2f} W")
    print(f"   Electricity Rate: {obs.get('cooling_coil_electricity_rate', 'N/A'):.2f} W")
    print(f"   Runtime Fraction: {obs.get('cooling_coil_runtime_fraction', 'N/A'):.3f}")
    print(f"   Basin Heater Rate: {obs.get('cooling_coil_basin_heater_rate', 'N/A'):.2f} W")
    print(f"   Outlet Temperature: {obs.get('cooling_coil_outlet_temp', 'N/A'):.2f}°C")
    
    # Main Heating Coil Status
    print(f"\n🔥 MAIN HEATING COIL (Main heating Coil 1):")
    print(f"   Heating Rate: {obs.get('heating_coil_heating_rate', 'N/A'):.2f} W")
    print(f"   Electricity Rate: {obs.get('heating_coil_electricity_rate', 'N/A'):.2f} W")
    print(f"   Outlet Temperature: {obs.get('heating_coil_outlet_temp', 'N/A'):.2f}°C")
    
    # Supply Air Status
    print(f"\n💨 SUPPLY AIR SYSTEM:")
    print(f"   Supply Air Temperature: {obs.get('supply_air_temp', 'N/A'):.2f}°C")
    print(f"   Supply Air Mass Flow Rate: {obs.get('supply_air_mass_flow_rate', 'N/A'):.3f} kg/s")
    
    # VAV Terminal Status for each zone
    zones = ['1', '2', '3', '4', '5']
    for zone in zones:
        print(f"\n🏠 ZONE {zone} VAV TERMINAL:")
        damper_pos = obs.get(f'vav_damper_position_{zone}', 'N/A')
        heating_rate = obs.get(f'vav_heating_rate_{zone}', 'N/A')
        cooling_rate = obs.get(f'vav_cooling_rate_{zone}', 'N/A')
        
        print(f"   Damper Position: {damper_pos:.3f}" if isinstance(damper_pos, (int, float)) else f"   Damper Position: {damper_pos}")
        print(f"   Sensible Heating Rate: {heating_rate:.2f} W" if isinstance(heating_rate, (int, float)) else f"   Sensible Heating Rate: {heating_rate}")
        print(f"   Sensible Cooling Rate: {cooling_rate:.2f} W" if isinstance(cooling_rate, (int, float)) else f"   Sensible Cooling Rate: {cooling_rate}")
    
    # Energy Summary
    print(f"\n⚡ ENERGY CONSUMPTION SUMMARY:")
    total_hvac = obs.get('HVAC_electricity_demand_rate', 0)
    fan_energy = obs.get('fan_electricity_rate', 0)
    cooling_energy = obs.get('cooling_coil_electricity_rate', 0)
    heating_energy = obs.get('heating_coil_electricity_rate', 0)
    basin_heater_energy = obs.get('cooling_coil_basin_heater_rate', 0)
    
    print(f"   Total HVAC Electricity Demand: {total_hvac:.2f} W")
    print(f"   Fan Electricity: {fan_energy:.2f} W ({fan_energy/total_hvac*100:.1f}%)" if total_hvac > 0 else "   Fan Electricity: N/A")
    print(f"   Cooling Coil Electricity: {cooling_energy:.2f} W ({cooling_energy/total_hvac*100:.1f}%)" if total_hvac > 0 else "   Cooling Coil Electricity: N/A")
    print(f"   Heating Coil Electricity: {heating_energy:.2f} W ({heating_energy/total_hvac*100:.1f}%)" if total_hvac > 0 else "   Heating Coil Electricity: N/A")
    print(f"   Basin Heater Electricity: {basin_heater_energy:.2f} W ({basin_heater_energy/total_hvac*100:.1f}%)" if total_hvac > 0 else "   Basin Heater Electricity: N/A")
    
    print(f"\n{'='*80}")

def run_hvac_monitoring_simulation(episodes=1, max_steps=100):
    """
    Run a simulation with comprehensive HVAC monitoring.
    
    Args:
        episodes (int): Number of episodes to run
        max_steps (int): Maximum steps per episode
    """
    print("🚀 Starting HVAC Component Monitoring Simulation")
    print("=" * 80)
    
    # Create environment with the modified configuration
    env = gym.make(
        'Eplus-5zone-v1',
        config_params={
            'building_file': '5ZoneAutoDXVAV.epJSON',
            'weather_files': ['USA_AZ_Davis-Monthan.AFB.722745_TMY3.epw'],
            'reward': LinearReward,
            'reward_kwargs': {
                'temperature_variables': ['air_temperature'],
                'energy_variables': ['HVAC_electricity_demand_rate'],
                'range_comfort_winter': [20.0, 23.5],
                'range_comfort_summer': [23.0, 26.0],
                'summer_start': [6, 1],
                'summer_final': [9, 30],
                'energy_weight': 0.5,
                'lambda_energy': 1.0e-4,
                'lambda_temperature': 1.0
            }
        }
    )
    
    # Data collection for analysis
    hvac_data = []
    
    for episode in range(episodes):
        print(f"\n🎬 Starting Episode {episode + 1}")
        obs, info = env.reset()
        
        # Print initial state
        print_hvac_status(obs, 0, f"Episode {episode + 1} - Initial State")
        
        for step in range(max_steps):
            # Take a random action (you can replace this with your control strategy)
            action = env.action_space.sample()
            
            # Step the environment
            obs, reward, terminated, truncated, info = env.step(action)
            
            # Create timestamp
            timestamp = f"Episode {episode + 1}, Step {step + 1}"
            
            # Print HVAC status every 10 steps or at the end
            if step % 10 == 0 or step == max_steps - 1 or terminated or truncated:
                print_hvac_status(obs, step + 1, timestamp)
            
            # Collect data for analysis
            hvac_data.append({
                'episode': episode + 1,
                'step': step + 1,
                'timestamp': timestamp,
                'fan_electricity_rate': obs.get('fan_electricity_rate', 0),
                'cooling_coil_electricity_rate': obs.get('cooling_coil_electricity_rate', 0),
                'heating_coil_electricity_rate': obs.get('heating_coil_electricity_rate', 0),
                'total_hvac_demand': obs.get('HVAC_electricity_demand_rate', 0),
                'cooling_coil_runtime_fraction': obs.get('cooling_coil_runtime_fraction', 0),
                'outdoor_air_flow_fraction': obs.get('outdoor_air_flow_fraction', 0),
                'supply_air_temp': obs.get('supply_air_temp', 0),
                'mixed_air_temp': obs.get('mixed_air_temp', 0),
                'reward': reward
            })
            
            if terminated or truncated:
                print(f"\n🏁 Episode {episode + 1} finished at step {step + 1}")
                break
        
        # Brief pause between episodes
        time.sleep(1)
    
    env.close()
    
    # Analyze collected data
    analyze_hvac_data(hvac_data)
    
    return hvac_data

def analyze_hvac_data(data):
    """
    Analyze collected HVAC data and provide insights.
    
    Args:
        data (list): List of dictionaries containing HVAC data
    """
    if not data:
        print("No data to analyze.")
        return
    
    df = pd.DataFrame(data)
    
    print(f"\n📊 HVAC PERFORMANCE ANALYSIS")
    print("=" * 80)
    
    # Energy consumption analysis
    print(f"\n⚡ ENERGY CONSUMPTION STATISTICS:")
    print(f"   Average Fan Electricity Rate: {df['fan_electricity_rate'].mean():.2f} W")
    print(f"   Average Cooling Coil Electricity Rate: {df['cooling_coil_electricity_rate'].mean():.2f} W")
    print(f"   Average Heating Coil Electricity Rate: {df['heating_coil_electricity_rate'].mean():.2f} W")
    print(f"   Average Total HVAC Demand: {df['total_hvac_demand'].mean():.2f} W")
    
    # System performance analysis
    print(f"\n🌡️  SYSTEM PERFORMANCE:")
    print(f"   Average Supply Air Temperature: {df['supply_air_temp'].mean():.2f}°C")
    print(f"   Average Mixed Air Temperature: {df['mixed_air_temp'].mean():.2f}°C")
    print(f"   Average Cooling Coil Runtime Fraction: {df['cooling_coil_runtime_fraction'].mean():.3f}")
    print(f"   Average Outdoor Air Flow Fraction: {df['outdoor_air_flow_fraction'].mean():.3f}")
    
    # Energy efficiency analysis
    total_energy = df['total_hvac_demand'].sum()
    fan_energy = df['fan_electricity_rate'].sum()
    cooling_energy = df['cooling_coil_electricity_rate'].sum()
    heating_energy = df['heating_coil_electricity_rate'].sum()
    
    print(f"\n🔋 ENERGY DISTRIBUTION:")
    print(f"   Fan Energy Share: {fan_energy/total_energy*100:.1f}%" if total_energy > 0 else "   Fan Energy Share: N/A")
    print(f"   Cooling Energy Share: {cooling_energy/total_energy*100:.1f}%" if total_energy > 0 else "   Cooling Energy Share: N/A")
    print(f"   Heating Energy Share: {heating_energy/total_energy*100:.1f}%" if total_energy > 0 else "   Heating Energy Share: N/A")
    
    # Peak demand analysis
    print(f"\n📈 PEAK DEMAND ANALYSIS:")
    print(f"   Peak Total HVAC Demand: {df['total_hvac_demand'].max():.2f} W")
    print(f"   Peak Fan Electricity Rate: {df['fan_electricity_rate'].max():.2f} W")
    print(f"   Peak Cooling Coil Electricity Rate: {df['cooling_coil_electricity_rate'].max():.2f} W")
    print(f"   Peak Heating Coil Electricity Rate: {df['heating_coil_electricity_rate'].max():.2f} W")

def create_hvac_report(data, filename="hvac_monitoring_report.csv"):
    """
    Create a CSV report of HVAC monitoring data.
    
    Args:
        data (list): List of dictionaries containing HVAC data
        filename (str): Output filename for the report
    """
    if not data:
        print("No data to export.")
        return
    
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"\n📄 HVAC monitoring report saved to: {filename}")

if __name__ == "__main__":
    print("🏢 Sinergym HVAC Component Monitoring System")
    print("=" * 80)
    print("This script demonstrates comprehensive HVAC component monitoring")
    print("including status, power consumption, and performance metrics.")
    print("=" * 80)
    
    # Run the monitoring simulation
    try:
        hvac_data = run_hvac_monitoring_simulation(episodes=1, max_steps=50)
        
        # Create a detailed report
        create_hvac_report(hvac_data, "hvac_detailed_report.csv")
        
        print(f"\n✅ HVAC monitoring simulation completed successfully!")
        print(f"📊 Data collected for {len(hvac_data)} simulation steps")
        
    except Exception as e:
        print(f"\n❌ Error during simulation: {str(e)}")
        print("Please ensure that:")
        print("1. Sinergym is properly installed")
        print("2. The modified epJSON and YAML files are in the correct locations")
        print("3. EnergyPlus is properly configured")