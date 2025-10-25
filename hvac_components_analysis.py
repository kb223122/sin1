#!/usr/bin/env python3
"""
HVAC Components Analysis for 5-Zone Building

This script analyzes the HVAC components in the 5-zone building and shows
how they should sum up to the total HVAC power.
"""

import json
import os

def analyze_5zone_hvac_components():
    """
    Analyze the HVAC components in the 5-zone building epJSON file.
    """
    
    print("=" * 80)
    print("5-ZONE BUILDING HVAC COMPONENTS ANALYSIS")
    print("=" * 80)
    
    # Path to the building file
    building_file = "/workspace/sinergym/data/buildings/5ZoneAutoDXVAV.epJSON"
    
    if not os.path.exists(building_file):
        print(f"Building file not found: {building_file}")
        return
    
    # Load the building file
    try:
        with open(building_file, 'r') as f:
            building_data = json.load(f)
        print("✅ Building file loaded successfully")
    except Exception as e:
        print(f"Error loading building file: {e}")
        return
    
    # Analyze HVAC components
    print("\n" + "=" * 60)
    print("HVAC COMPONENTS FOUND IN 5-ZONE BUILDING")
    print("=" * 60)
    
    # 1. Fans
    print("\n1. FANS:")
    if "Fan:VariableVolume" in building_data:
        for fan_name, fan_data in building_data["Fan:VariableVolume"].items():
            print(f"   - {fan_name}")
            print(f"     Type: Variable Volume Fan")
            print(f"     Power Coefficients: {fan_data.get('fan_power_coefficient_1', 'N/A')}")
            print(f"     Min Flow Fraction: {fan_data.get('fan_power_minimum_flow_fraction', 'N/A')}")
    
    # 2. Cooling Coils
    print("\n2. COOLING COILS:")
    if "Coil:Cooling:DX:TwoSpeed" in building_data:
        for coil_name, coil_data in building_data["Coil:Cooling:DX:TwoSpeed"].items():
            print(f"   - {coil_name}")
            print(f"     Type: Two-Speed DX Cooling Coil")
            print(f"     High Speed COP: {coil_data.get('high_speed_gross_rated_cooling_cop', 'N/A')}")
            print(f"     Condenser Type: {coil_data.get('condenser_type', 'N/A')}")
    
    # 3. Heating Coils
    print("\n3. HEATING COILS:")
    if "Coil:Heating:Electric" in building_data:
        for coil_name, coil_data in building_data["Coil:Heating:Electric"].items():
            print(f"   - {coil_name}")
            print(f"     Type: Electric Heating Coil")
            print(f"     Efficiency: {coil_data.get('efficiency', 'N/A')}")
            print(f"     Nominal Capacity: {coil_data.get('nominal_capacity', 'N/A')}")
    
    # 4. VAV Reheat Units
    print("\n4. VAV REHEAT UNITS:")
    if "AirTerminal:SingleDuct:VAV:Reheat" in building_data:
        for vav_name, vav_data in building_data["AirTerminal:SingleDuct:VAV:Reheat"].items():
            print(f"   - {vav_name}")
            print(f"     Type: VAV Reheat Terminal")
            print(f"     Reheat Coil: {vav_data.get('reheat_coil_name', 'N/A')}")
            print(f"     Reheat Coil Type: {vav_data.get('reheat_coil_object_type', 'N/A')}")
    
    # 5. Air Distribution Units
    print("\n5. AIR DISTRIBUTION UNITS:")
    if "ZoneHVAC:AirDistributionUnit" in building_data:
        for adu_name, adu_data in building_data["ZoneHVAC:AirDistributionUnit"].items():
            print(f"   - {adu_name}")
            print(f"     Air Terminal: {adu_data.get('air_terminal_name', 'N/A')}")
    
    print("\n" + "=" * 60)
    print("POWER CALCULATION BREAKDOWN")
    print("=" * 60)
    
    print("\nThe total HVAC power should be the sum of:")
    print("1. Supply Fan Power (Supply Fan 1)")
    print("2. Main Cooling Coil Power (Main Cooling Coil 1)")
    print("3. Main Heating Coil Power (Main heating Coil 1)")
    print("4. Zone 1 Reheat Coil Power (SPACE1-1 Zone Coil)")
    print("5. Zone 2 Reheat Coil Power (SPACE2-1 Zone Coil)")
    print("6. Zone 3 Reheat Coil Power (SPACE3-1 Zone Coil)")
    print("7. Zone 4 Reheat Coil Power (SPACE4-1 Zone Coil)")
    print("8. Zone 5 Reheat Coil Power (SPACE5-1 Zone Coil)")
    
    print("\n" + "=" * 60)
    print("VERIFICATION VARIABLES NEEDED")
    print("=" * 60)
    
    print("\nTo verify the power summation, you need these variables:")
    print("Variables:")
    print("  - Fan Electricity Rate: Supply Fan 1")
    print("  - Cooling Coil Electricity Rate: Main Cooling Coil 1")
    print("  - Heating Coil Electricity Rate: Main heating Coil 1")
    print("  - Heating Coil Electricity Rate: SPACE1-1 Zone Coil")
    print("  - Heating Coil Electricity Rate: SPACE2-1 Zone Coil")
    print("  - Heating Coil Electricity Rate: SPACE3-1 Zone Coil")
    print("  - Heating Coil Electricity Rate: SPACE4-1 Zone Coil")
    print("  - Heating Coil Electricity Rate: SPACE5-1 Zone Coil")
    print("  - Facility Total HVAC Electricity Demand Rate: Whole Building")
    
    print("\nMeters:")
    print("  - Electricity:HVAC (for total energy)")
    print("  - Electricity:Fans (for fan energy)")
    print("  - Electricity:Cooling (for cooling energy)")
    print("  - Electricity:Heating (for heating energy)")

def create_verification_config():
    """
    Create a configuration file for HVAC power verification.
    """
    
    config = {
        "id_base": "5zone_verification",
        "building_file": "5ZoneAutoDXVAV.epJSON",
        "weather_specification": {
            "weather_files": ["USA_AZ_Davis-Monthan.AFB.722745_TMY3.epw"],
            "keys": ["hot"]
        },
        "time_variables": ["month", "day_of_month", "hour"],
        "variables": {
            # Environment variables
            "outdoor_temperature": {
                "variable_names": "outdoor_temperature",
                "keys": "Environment"
            },
            "air_temperature": {
                "variable_names": "air_temperature",
                "keys": "SPACE5-1"
            },
            
            # Individual HVAC component electricity rates
            "supply_fan_electricity_rate": {
                "variable_names": "supply_fan_electricity_rate",
                "keys": "Supply Fan 1"
            },
            "main_cooling_coil_electricity_rate": {
                "variable_names": "main_cooling_coil_electricity_rate",
                "keys": "Main Cooling Coil 1"
            },
            "main_heating_coil_electricity_rate": {
                "variable_names": "main_heating_coil_electricity_rate",
                "keys": "Main heating Coil 1"
            },
            "zone1_reheat_electricity_rate": {
                "variable_names": "zone1_reheat_electricity_rate",
                "keys": "SPACE1-1 Zone Coil"
            },
            "zone2_reheat_electricity_rate": {
                "variable_names": "zone2_reheat_electricity_rate",
                "keys": "SPACE2-1 Zone Coil"
            },
            "zone3_reheat_electricity_rate": {
                "variable_names": "zone3_reheat_electricity_rate",
                "keys": "SPACE3-1 Zone Coil"
            },
            "zone4_reheat_electricity_rate": {
                "variable_names": "zone4_reheat_electricity_rate",
                "keys": "SPACE4-1 Zone Coil"
            },
            "zone5_reheat_electricity_rate": {
                "variable_names": "zone5_reheat_electricity_rate",
                "keys": "SPACE5-1 Zone Coil"
            },
            
            # Total HVAC power
            "HVAC_electricity_demand_rate": {
                "variable_names": "HVAC_electricity_demand_rate",
                "keys": "Whole Building"
            }
        },
        "meters": {
            "total_electricity_HVAC": "Electricity:HVAC",
            "supply_fan_electricity": "Electricity:Fans",
            "cooling_coil_electricity": "Electricity:Cooling",
            "heating_coil_electricity": "Electricity:Heating"
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
        import yaml
        with open(config_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"\n✅ Verification configuration saved to: {config_file}")
    except ImportError:
        print("\n⚠️  YAML not available, saving as JSON instead")
        with open(config_file.replace('.yaml', '.json'), 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Verification configuration saved to: {config_file.replace('.yaml', '.json')}")

def main():
    """Main function."""
    
    analyze_5zone_hvac_components()
    create_verification_config()
    
    print("\n" + "=" * 80)
    print("NEXT STEPS FOR VERIFICATION")
    print("=" * 80)
    print("1. Use the generated configuration file to create a Sinergym environment")
    print("2. Run the environment and collect power data for each component")
    print("3. Sum the individual component powers and compare with total HVAC power")
    print("4. Verify that: Sum(Components) ≈ Total HVAC Power")
    print("\nThe verification should show that the total HVAC power is the sum of:")
    print("- 1 Supply Fan")
    print("- 1 Main Cooling Coil")
    print("- 1 Main Heating Coil")
    print("- 5 Zone Reheat Coils")

if __name__ == "__main__":
    main()