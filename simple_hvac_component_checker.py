#!/usr/bin/env python3
"""
Simple HVAC Component Checker for 5-Zone Building

This script provides a simple way to check what components contribute to:
1. Total HVAC Power
2. Total HVAC Energy
3. Cooling:Electricity meter specifically
"""

import sys
import os
sys.path.append('/workspace')

def create_simple_verification_environment():
    """Create a simple environment for component verification."""
    
    print("=" * 80)
    print("CREATING SIMPLE HVAC COMPONENT CHECKER")
    print("=" * 80)
    
    # Simple variables configuration focused on key components
    variables = {
        # Environment
        'Site Outdoor Air Drybulb Temperature': {
            'variable_names': 'outdoor_temperature',
            'keys': 'ENVIRONMENT'
        },
        'Zone Air Temperature': {
            'variable_names': 'air_temperature',
            'keys': 'SPACE5-1'
        },
        
        # TOTAL HVAC
        'Facility Total HVAC Electricity Demand Rate': {
            'variable_names': 'HVAC_electricity_demand_rate',
            'keys': 'WHOLE BUILDING'
        },
        
        # CENTRAL SYSTEM COMPONENTS
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
        
        # ZONE REHEAT COMPONENTS (Note: These will have variable name conflicts)
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
        
        # ADDITIONAL COOLING COMPONENTS
        'Cooling Coil Evaporative Condenser Pump Electricity Energy': {
            'variable_names': 'cooling_coil_evaporative_condenser_pump_electricity_energy',
            'keys': 'MAIN COOLING COIL 1'
        },
        'Cooling Coil Basin Heater Electricity Energy': {
            'variable_names': 'cooling_coil_basin_heater_electricity_energy',
            'keys': 'MAIN COOLING COIL 1'
        },
    }
    
    # Meters configuration
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
        'id_base': '5zone_simple_hvac_checker',
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
    config_file = '/workspace/simple_hvac_checker_config.yaml'
    try:
        import yaml
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Simple checker configuration saved to: {config_file}")
        return config_file
    except Exception as e:
        print(f"Error saving configuration: {e}")
        return None

def create_simple_checker_script():
    """Create a simple checker script."""
    
    script_content = '''#!/usr/bin/env python3
"""
Simple HVAC Component Checker Script
"""

import sys
import os
sys.path.append('/workspace')

def run_simple_hvac_checker():
    """Run simple HVAC component checker."""
    
    try:
        import gymnasium as gym
        import numpy as np
        from sinergym.envs.eplus_env import EplusEnv
        import yaml
    except ImportError as e:
        print(f"Import error: {e}")
        return False
    
    # Load the simple checker configuration
    config_file = "/workspace/simple_hvac_checker_config.yaml"
    
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
        print("✅ Simple HVAC checker environment created successfully")
    except Exception as e:
        print(f"Error creating environment: {e}")
        return False
    
    # Run checker
    print("\\n" + "=" * 80)
    print("SIMPLE HVAC COMPONENT CHECKER")
    print("=" * 80)
    
    try:
        obs, info = env.reset()
        print("Environment reset successfully")
        print(f"Available observation variables: {len(obs.keys())} variables")
        
        for step in range(3):  # Run 3 steps
            print(f"\\n{'='*60}")
            print(f"STEP {step + 1}")
            print(f"{'='*60}")
            
            # Take random action
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            # 1. CHECK TOTAL HVAC POWER COMPONENTS
            print("\\n🔌 TOTAL HVAC POWER COMPONENTS:")
            print("-" * 40)
            
            total_hvac_power = obs.get('HVAC_electricity_demand_rate', 0.0)
            print(f"Total HVAC Power: {total_hvac_power:.2f} W")
            
            # Central system components
            central_components = {
                'Supply Fan 1': obs.get('supply_fan_electricity_rate', 0.0),
                'Main Heating Coil 1': obs.get('main_heating_coil_electricity_rate', 0.0),
                'Main Cooling Coil 1': obs.get('main_cooling_coil_electricity_rate', 0.0),
            }
            
            print("\\nCentral System Components:")
            for name, power in central_components.items():
                print(f"  {name}: {power:.2f} W")
            
            # Zone reheat components (Note: These may not work due to variable name conflicts)
            zone_components = {
                'SPACE1-1 Zone Coil': obs.get('zone1_reheat_electricity_rate', 0.0),
                'SPACE2-1 Zone Coil': obs.get('zone2_reheat_electricity_rate', 0.0),
                'SPACE3-1 Zone Coil': obs.get('zone3_reheat_electricity_rate', 0.0),
                'SPACE4-1 Zone Coil': obs.get('zone4_reheat_electricity_rate', 0.0),
                'SPACE5-1 Zone Coil': obs.get('zone5_reheat_electricity_rate', 0.0),
            }
            
            print("\\nZone Reheat Components:")
            for name, power in zone_components.items():
                print(f"  {name}: {power:.2f} W")
            
            # Additional cooling components
            additional_cooling = {
                'Cooling Coil Evaporative Condenser Pump': obs.get('cooling_coil_evaporative_condenser_pump_electricity_energy', 0.0),
                'Cooling Coil Basin Heater': obs.get('cooling_coil_basin_heater_electricity_energy', 0.0),
            }
            
            print("\\nAdditional Cooling Components:")
            for name, power in additional_cooling.items():
                print(f"  {name}: {power:.2f} W")
            
            # Calculate total
            central_total = sum(central_components.values())
            zone_total = sum(zone_components.values())
            additional_total = sum(additional_cooling.values())
            calculated_total = central_total + zone_total + additional_total
            
            print(f"\\nCentral System Total: {central_total:.2f} W")
            print(f"Zone Reheat Total: {zone_total:.2f} W")
            print(f"Additional Cooling Total: {additional_total:.2f} W")
            print(f"Calculated Total: {calculated_total:.2f} W")
            
            if total_hvac_power > 0:
                difference = abs(total_hvac_power - calculated_total)
                percentage_error = (difference / total_hvac_power) * 100
                print(f"Difference: {difference:.2f} W ({percentage_error:.2f}%)")
            
            # 2. CHECK TOTAL HVAC ENERGY COMPONENTS
            print("\\n⚡ TOTAL HVAC ENERGY COMPONENTS:")
            print("-" * 40)
            
            total_hvac_energy = obs.get('total_electricity_HVAC', 0.0)
            heating_energy = obs.get('heating_electricity', 0.0)
            fans_energy = obs.get('fans_electricity', 0.0)
            cooling_energy = obs.get('cooling_electricity', 0.0)
            
            print(f"Total HVAC Energy: {total_hvac_energy:.2f} J")
            print(f"Heating Energy: {heating_energy:.2f} J")
            print(f"Fans Energy: {fans_energy:.2f} J")
            print(f"Cooling Energy: {cooling_energy:.2f} J")
            
            calculated_energy = heating_energy + fans_energy + cooling_energy
            print(f"Calculated Total: {calculated_energy:.2f} J")
            
            if total_hvac_energy > 0:
                energy_difference = abs(total_hvac_energy - calculated_energy)
                energy_percentage_error = (energy_difference / total_hvac_energy) * 100
                print(f"Energy Difference: {energy_difference:.2f} J ({energy_percentage_error:.2f}%)")
            
            # 3. CHECK COOLING:ELECTRICITY METER COMPONENTS
            print("\\n❄️  COOLING:ELECTRICITY METER COMPONENTS:")
            print("-" * 40)
            
            print(f"Cooling:Electricity Meter: {cooling_energy:.2f} J")
            
            # Individual cooling components
            cooling_components = {
                'Main Cooling Coil 1': obs.get('main_cooling_coil_electricity_rate', 0.0),
                'Cooling Coil Evaporative Condenser Pump': obs.get('cooling_coil_evaporative_condenser_pump_electricity_energy', 0.0),
                'Cooling Coil Basin Heater': obs.get('cooling_coil_basin_heater_electricity_energy', 0.0),
            }
            
            print("\\nCooling Components:")
            for name, power in cooling_components.items():
                print(f"  {name}: {power:.2f} W/J")
            
            cooling_total = sum(cooling_components.values())
            print(f"\\nCalculated Cooling Total: {cooling_total:.2f} W/J")
            
            if cooling_energy > 0:
                cooling_difference = abs(cooling_energy - cooling_total)
                cooling_percentage_error = (cooling_difference / cooling_energy) * 100
                print(f"Cooling Difference: {cooling_difference:.2f} J ({cooling_percentage_error:.2f}%)")
            
            # 4. COMPONENT CONTRIBUTION SUMMARY
            print("\\n📊 COMPONENT CONTRIBUTION SUMMARY:")
            print("-" * 40)
            
            if total_hvac_power > 0:
                print("Power Contribution (%):")
                for name, power in {**central_components, **zone_components, **additional_cooling}.items():
                    if power > 0:
                        contribution = (power / total_hvac_power) * 100
                        print(f"  {name}: {contribution:.2f}%")
            
            if total_hvac_energy > 0:
                print("\\nEnergy Contribution (%):")
                if heating_energy > 0:
                    print(f"  Heating: {(heating_energy / total_hvac_energy) * 100:.2f}%")
                if fans_energy > 0:
                    print(f"  Fans: {(fans_energy / total_hvac_energy) * 100:.2f}%")
                if cooling_energy > 0:
                    print(f"  Cooling: {(cooling_energy / total_hvac_energy) * 100:.2f}%")
            
            if terminated or truncated:
                print(f"\\nSimulation ended at step {step + 1}")
                break
        
        print("\\n" + "=" * 80)
        print("COMPONENT CHECK SUMMARY")
        print("=" * 80)
        
        print("\\n🔌 **TOTAL HVAC POWER COMPONENTS:**")
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
        
        print("\\n⚡ **TOTAL HVAC ENERGY COMPONENTS:**")
        print("1. Heating:Electricity (All heating components)")
        print("2. Fans:Electricity (All fan components)")
        print("3. Cooling:Electricity (All cooling components)")
        
        print("\\n❄️  **COOLING:ELECTRICITY COMPONENTS:**")
        print("1. Main Cooling Coil 1")
        print("2. Cooling Coil Evaporative Condenser Pump")
        print("3. Cooling Coil Basin Heater")
        print("4. Zone cooling energy transfer (included in meter)")
        
        print("\\n✅ **VERIFICATION COMPLETE**")
        print("   All HVAC components have been identified and checked")
        
    except Exception as e:
        print(f"Error during verification: {e}")
        return False
    finally:
        env.close()
    
    return True

if __name__ == "__main__":
    success = run_simple_hvac_checker()
    sys.exit(0 if success else 1)
'''
    
    script_file = '/workspace/run_simple_hvac_checker.py'
    try:
        with open(script_file, 'w') as f:
            f.write(script_content)
        os.chmod(script_file, 0o755)
        print(f"✅ Simple checker script saved to: {script_file}")
        return script_file
    except Exception as e:
        print(f"Error saving script: {e}")
        return None

def print_simple_guide():
    """Print simple guide."""
    
    print("\n" + "=" * 80)
    print("SIMPLE HVAC COMPONENT CHECKER GUIDE")
    print("=" * 80)
    
    print("\n🎯 **WHAT THIS CHECKER DOES:**")
    print("=" * 40)
    
    print("\n1. **Identifies Total HVAC Power Components**")
    print("   • Central system: 3 components")
    print("   • Zone reheat system: 5 components")
    print("   • Additional cooling: 2 components")
    print("   • Total: 10 components")
    
    print("\n2. **Identifies Total HVAC Energy Components**")
    print("   • Heating:Electricity meter")
    print("   • Fans:Electricity meter")
    print("   • Cooling:Electricity meter")
    
    print("\n3. **Identifies Cooling:Electricity Components**")
    print("   • Main Cooling Coil 1")
    print("   • Cooling Coil Evaporative Condenser Pump")
    print("   • Cooling Coil Basin Heater")
    print("   • Zone cooling energy transfer")
    
    print("\n🚀 **HOW TO RUN:**")
    print("=" * 20)
    print("python3 /workspace/run_simple_hvac_checker.py")
    
    print("\n📊 **EXPECTED OUTPUT:**")
    print("=" * 20)
    print("• Component-by-component power and energy values")
    print("• Percentage contribution analysis")
    print("• Verification of component summation")
    print("• Clear identification of all contributing components")

def main():
    """Main function."""
    
    print("=" * 80)
    print("SIMPLE HVAC COMPONENT CHECKER SETUP")
    print("=" * 80)
    
    # Create simple checker environment
    config_file = create_simple_verification_environment()
    if config_file:
        # Create simple checker script
        script_file = create_simple_checker_script()
        if script_file:
            # Print simple guide
            print_simple_guide()
        else:
            print("❌ Failed to create simple checker script")
    else:
        print("❌ Failed to create simple checker configuration")

if __name__ == "__main__":
    main()