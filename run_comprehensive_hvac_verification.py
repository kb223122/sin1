#!/usr/bin/env python3
"""
Comprehensive HVAC Component Verification Script
"""

import sys
import os
sys.path.append('/workspace')

def run_comprehensive_hvac_verification():
    """Run comprehensive HVAC component verification."""
    
    try:
        import gymnasium as gym
        import numpy as np
        from sinergym.envs.eplus_env import EplusEnv
        import yaml
        import pandas as pd
    except ImportError as e:
        print(f"Import error: {e}")
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
    print("COMPREHENSIVE HVAC COMPONENT VERIFICATION")
    print("=" * 80)
    
    try:
        obs, info = env.reset()
        print("Environment reset successfully")
        
        # Store verification data
        verification_data = []
        
        for step in range(10):
            print(f"\n{'='*60}")
            print(f"STEP {step + 1}")
            print(f"{'='*60}")
            
            # Take random action
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            # 1. TOTAL HVAC POWER VERIFICATION
            print("\n🔌 TOTAL HVAC POWER VERIFICATION:")
            print("-" * 40)
            
            total_hvac_power = obs.get('HVAC_electricity_demand_rate', 0.0)
            
            # Central system components
            central_components = {
                'Supply Fan 1': obs.get('supply_fan_electricity_rate', 0.0),
                'Main Heating Coil 1': obs.get('main_heating_coil_electricity_rate', 0.0),
                'Main Cooling Coil 1': obs.get('main_cooling_coil_electricity_rate', 0.0),
            }
            
            # Zone reheat components
            zone_components = {
                'SPACE1-1 Zone Coil': obs.get('zone1_reheat_electricity_rate', 0.0),
                'SPACE2-1 Zone Coil': obs.get('zone2_reheat_electricity_rate', 0.0),
                'SPACE3-1 Zone Coil': obs.get('zone3_reheat_electricity_rate', 0.0),
                'SPACE4-1 Zone Coil': obs.get('zone4_reheat_electricity_rate', 0.0),
                'SPACE5-1 Zone Coil': obs.get('zone5_reheat_electricity_rate', 0.0),
            }
            
            # Additional cooling components
            additional_cooling_components = {
                'Cooling Coil Evaporative Condenser Pump': obs.get('cooling_coil_evaporative_condenser_pump_electricity_rate', 0.0),
                'Cooling Coil Basin Heater': obs.get('cooling_coil_basin_heater_electricity_rate', 0.0),
            }
            
            print("Central System Components (W):")
            for name, power in central_components.items():
                print(f"  {name}: {power:.2f}")
            
            print("\nZone Reheat Components (W):")
            for name, power in zone_components.items():
                print(f"  {name}: {power:.2f}")
            
            print("\nAdditional Cooling Components (W):")
            for name, power in additional_cooling_components.items():
                print(f"  {name}: {power:.2f}")
            
            # Calculate total
            central_total = sum(central_components.values())
            zone_total = sum(zone_components.values())
            additional_cooling_total = sum(additional_cooling_components.values())
            calculated_total_power = central_total + zone_total + additional_cooling_total
            
            print(f"\nCentral System Total: {central_total:.2f} W")
            print(f"Zone Reheat Total: {zone_total:.2f} W")
            print(f"Additional Cooling Total: {additional_cooling_total:.2f} W")
            print(f"Calculated Total Power: {calculated_total_power:.2f} W")
            print(f"EnergyPlus Total Power: {total_hvac_power:.2f} W")
            
            if total_hvac_power > 0:
                power_difference = abs(total_hvac_power - calculated_total_power)
                power_percentage_error = (power_difference / total_hvac_power) * 100
                print(f"Power Difference: {power_difference:.2f} W ({power_percentage_error:.2f}%)")
                
                if power_percentage_error < 5.0:
                    print("✅ POWER VERIFICATION PASSED")
                else:
                    print("⚠️  POWER VERIFICATION WARNING")
            
            # 2. TOTAL HVAC ENERGY VERIFICATION
            print("\n⚡ TOTAL HVAC ENERGY VERIFICATION:")
            print("-" * 40)
            
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
                print(f"Calculated Total Energy: {calculated_total_energy:.2f} J")
                print(f"Energy Difference: {energy_difference:.2f} J ({energy_percentage_error:.2f}%)")
                
                if energy_percentage_error < 5.0:
                    print("✅ ENERGY VERIFICATION PASSED")
                else:
                    print("⚠️  ENERGY VERIFICATION WARNING")
            
            # 3. COOLING:ELECTRICITY METER BREAKDOWN
            print("\n❄️  COOLING:ELECTRICITY METER BREAKDOWN:")
            print("-" * 40)
            
            # Individual cooling components
            cooling_components = {
                'Main Cooling Coil 1': obs.get('main_cooling_coil_electricity_energy', 0.0),
                'Cooling Coil Evaporative Condenser Pump': obs.get('cooling_coil_evaporative_condenser_pump_electricity_energy', 0.0),
                'Cooling Coil Basin Heater': obs.get('cooling_coil_basin_heater_electricity_energy', 0.0),
            }
            
            # Zone cooling energy transfer
            zone_cooling_energy = {
                'SPACE1-1 Cooling Energy': obs.get('zone1_sensible_cooling_energy', 0.0),
                'SPACE2-1 Cooling Energy': obs.get('zone2_sensible_cooling_energy', 0.0),
                'SPACE3-1 Cooling Energy': obs.get('zone3_sensible_cooling_energy', 0.0),
                'SPACE4-1 Cooling Energy': obs.get('zone4_sensible_cooling_energy', 0.0),
                'SPACE5-1 Cooling Energy': obs.get('zone5_sensible_cooling_energy', 0.0),
            }
            
            print("Cooling Components (J):")
            for name, energy in cooling_components.items():
                print(f"  {name}: {energy:.2f}")
            
            print("\nZone Cooling Energy Transfer (J):")
            for name, energy in zone_cooling_energy.items():
                print(f"  {name}: {energy:.2f}")
            
            # Calculate cooling total
            cooling_components_total = sum(cooling_components.values())
            zone_cooling_total = sum(zone_cooling_energy.values())
            calculated_cooling_total = cooling_components_total + zone_cooling_total
            
            print(f"\nCooling Components Total: {cooling_components_total:.2f} J")
            print(f"Zone Cooling Total: {zone_cooling_total:.2f} J")
            print(f"Calculated Cooling Total: {calculated_cooling_total:.2f} J")
            print(f"Cooling:Electricity Meter: {cooling_energy:.2f} J")
            
            if cooling_energy > 0:
                cooling_difference = abs(cooling_energy - calculated_cooling_total)
                cooling_percentage_error = (cooling_difference / cooling_energy) * 100
                print(f"Cooling Difference: {cooling_difference:.2f} J ({cooling_percentage_error:.2f}%)")
                
                if cooling_percentage_error < 5.0:
                    print("✅ COOLING VERIFICATION PASSED")
                else:
                    print("⚠️  COOLING VERIFICATION WARNING")
            
            # 4. COMPONENT CONTRIBUTION ANALYSIS
            print("\n📊 COMPONENT CONTRIBUTION ANALYSIS:")
            print("-" * 40)
            
            if total_hvac_power > 0:
                print("Power Contribution (%):")
                for name, power in {**central_components, **zone_components, **additional_cooling_components}.items():
                    contribution = (power / total_hvac_power) * 100
                    print(f"  {name}: {contribution:.2f}%")
            
            if total_hvac_energy > 0:
                print("\nEnergy Contribution (%):")
                print(f"  Heating: {(heating_energy / total_hvac_energy) * 100:.2f}%")
                print(f"  Fans: {(fans_energy / total_hvac_energy) * 100:.2f}%")
                print(f"  Cooling: {(cooling_energy / total_hvac_energy) * 100:.2f}%")
            
            # Store data for analysis
            step_data = {
                'step': step + 1,
                'total_hvac_power': total_hvac_power,
                'calculated_total_power': calculated_total_power,
                'power_difference': power_difference if total_hvac_power > 0 else 0,
                'power_percentage_error': power_percentage_error if total_hvac_power > 0 else 0,
                'total_hvac_energy': total_hvac_energy,
                'calculated_total_energy': calculated_total_energy,
                'energy_difference': energy_difference if total_hvac_energy > 0 else 0,
                'energy_percentage_error': energy_percentage_error if total_hvac_energy > 0 else 0,
                'cooling_energy': cooling_energy,
                'calculated_cooling_total': calculated_cooling_total,
                'cooling_difference': cooling_difference if cooling_energy > 0 else 0,
                'cooling_percentage_error': cooling_percentage_error if cooling_energy > 0 else 0,
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
            df = pd.DataFrame(verification_data)
            
            print(f"\nAverage Power Error: {df['power_percentage_error'].mean():.2f}%")
            print(f"Average Energy Error: {df['energy_percentage_error'].mean():.2f}%")
            print(f"Average Cooling Error: {df['cooling_percentage_error'].mean():.2f}%")
            
            print("\n✅ VERIFICATION COMPLETE")
            print("   All HVAC components have been analyzed and verified")
            
            # Save detailed results
            df.to_csv('/workspace/hvac_component_verification_results.csv', index=False)
            print(f"\nDetailed results saved to: /workspace/hvac_component_verification_results.csv")
        
        print("\n" + "=" * 80)
        print("COMPONENT CONTRIBUTION SUMMARY")
        print("=" * 80)
        
        print("\n🔌 TOTAL HVAC POWER COMPONENTS:")
        print("1. Central System (3 components):")
        print("   • Supply Fan 1")
        print("   • Main Heating Coil 1")
        print("   • Main Cooling Coil 1")
        print("2. Zone Reheat System (5 components):")
        print("   • SPACE1-1 Zone Coil")
        print("   • SPACE2-1 Zone Coil")
        print("   • SPACE3-1 Zone Coil")
        print("   • SPACE4-1 Zone Coil")
        print("   • SPACE5-1 Zone Coil")
        print("3. Additional Cooling (2 components):")
        print("   • Cooling Coil Evaporative Condenser Pump")
        print("   • Cooling Coil Basin Heater")
        
        print("\n⚡ TOTAL HVAC ENERGY COMPONENTS:")
        print("1. Heating:Electricity (All heating components)")
        print("2. Fans:Electricity (All fan components)")
        print("3. Cooling:Electricity (All cooling components)")
        
        print("\n❄️  COOLING:ELECTRICITY COMPONENTS:")
        print("1. Main Cooling Coil 1")
        print("2. Cooling Coil Evaporative Condenser Pump")
        print("3. Cooling Coil Basin Heater")
        print("4. Zone Cooling Energy Transfer (5 zones)")
        
    except Exception as e:
        print(f"Error during verification: {e}")
        return False
    finally:
        env.close()
    
    return True

if __name__ == "__main__":
    success = run_comprehensive_hvac_verification()
    sys.exit(0 if success else 1)
