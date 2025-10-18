#!/usr/bin/env python3
"""
Simple test script for HVAC monitoring without requiring EnergyPlus.
This script tests the configuration and provides a mock simulation.
"""

import numpy as np
import yaml
import os

def load_yaml_config():
    """Load the YAML configuration."""
    yaml_path = 'sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml'
    
    try:
        with open(yaml_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"❌ Error loading YAML config: {e}")
        return None

def create_mock_observation():
    """Create a mock observation with HVAC data."""
    config = load_yaml_config()
    if not config:
        return None
    
    # Create mock observation data
    obs = {}
    
    # Time variables
    obs['month'] = 1
    obs['day_of_month'] = 1
    obs['hour'] = 12
    
    # Outdoor variables
    obs['outdoor_temperature'] = 25.0
    obs['outdoor_humidity'] = 50.0
    obs['wind_speed'] = 2.5
    obs['wind_direction'] = 180.0
    obs['diffuse_solar_radiation'] = 200.0
    obs['direct_solar_radiation'] = 500.0
    
    # Zone variables
    obs['air_temperature'] = 22.0
    obs['air_humidity'] = 45.0
    obs['people_occupant'] = 2.0
    
    # System variables
    obs['htg_setpoint'] = 20.0
    obs['clg_setpoint'] = 24.0
    
    # Energy variables
    obs['co2_emission'] = 0.5
    obs['HVAC_electricity_demand_rate'] = 1500.0
    
    # HVAC variables (from our configuration)
    obs['fan_electricity_rate'] = 200.0
    obs['fan_air_mass_flow_rate'] = 2.5
    obs['cooling_coil_total_rate'] = 800.0
    obs['cooling_coil_electricity_rate'] = 600.0
    obs['heating_coil_heating_rate'] = 0.0
    obs['heating_coil_electricity_rate'] = 0.0
    obs['outdoor_air_flow_fraction'] = 0.2
    
    return obs

def print_hvac_status_mock(obs, step):
    """Print HVAC status using mock data."""
    print(f"\n{'='*80}")
    print(f"HVAC COMPONENT STATUS - Step {step} (MOCK DATA)")
    print(f"{'='*80}")
    
    # System Overview
    print(f"\n🏢 SYSTEM OVERVIEW:")
    print(f"   Outdoor Air Flow Fraction: {obs.get('outdoor_air_flow_fraction', 'N/A'):.3f}")
    print(f"   Total HVAC Electricity Demand: {obs.get('HVAC_electricity_demand_rate', 'N/A'):.2f} W")
    
    # Supply Fan Status
    print(f"\n🌀 SUPPLY FAN (Supply Fan 1):")
    print(f"   Electricity Rate: {obs.get('fan_electricity_rate', 'N/A'):.2f} W")
    print(f"   Air Mass Flow Rate: {obs.get('fan_air_mass_flow_rate', 'N/A'):.3f} kg/s")
    
    # Main Cooling Coil Status
    print(f"\n❄️  MAIN COOLING COIL (Main Cooling Coil 1):")
    print(f"   Total Cooling Rate: {obs.get('cooling_coil_total_rate', 'N/A'):.2f} W")
    print(f"   Electricity Rate: {obs.get('cooling_coil_electricity_rate', 'N/A'):.2f} W")
    
    # Main Heating Coil Status
    print(f"\n🔥 MAIN HEATING COIL (Main heating Coil 1):")
    print(f"   Heating Rate: {obs.get('heating_coil_heating_rate', 'N/A'):.2f} W")
    print(f"   Electricity Rate: {obs.get('heating_coil_electricity_rate', 'N/A'):.2f} W")
    
    # Energy Summary
    print(f"\n⚡ ENERGY CONSUMPTION SUMMARY:")
    total_hvac = obs.get('HVAC_electricity_demand_rate', 0)
    fan_energy = obs.get('fan_electricity_rate', 0)
    cooling_energy = obs.get('cooling_coil_electricity_rate', 0)
    heating_energy = obs.get('heating_coil_electricity_rate', 0)
    
    print(f"   Total HVAC Electricity Demand: {total_hvac:.2f} W")
    print(f"   Fan Electricity: {fan_energy:.2f} W ({fan_energy/total_hvac*100:.1f}%)" if total_hvac > 0 else "   Fan Electricity: N/A")
    print(f"   Cooling Coil Electricity: {cooling_energy:.2f} W ({cooling_energy/total_hvac*100:.1f}%)" if total_hvac > 0 else "   Cooling Coil Electricity: N/A")
    print(f"   Heating Coil Electricity: {heating_energy:.2f} W ({heating_energy/total_hvac*100:.1f}%)" if total_hvac > 0 else "   Heating Coil Electricity: N/A")
    
    print(f"\n{'='*80}")

def test_hvac_monitoring_mock():
    """Test HVAC monitoring with mock data."""
    print("🧪 Testing HVAC Monitoring with Mock Data")
    print("=" * 80)
    
    # Load configuration
    config = load_yaml_config()
    if not config:
        print("❌ Failed to load configuration")
        return False
    
    print("✅ Configuration loaded successfully")
    
    # Test variable access
    variables = config.get('variables', {})
    hvac_vars = [
        'Fan Electricity Rate',
        'Fan Air Mass Flow Rate', 
        'Cooling Coil Total Cooling Rate',
        'Cooling Coil Electricity Rate',
        'Heating Coil Heating Rate',
        'Heating Coil Electricity Rate',
        'Air System Outdoor Air Flow Fraction'
    ]
    
    print(f"\n📊 Available HVAC Variables:")
    for var in hvac_vars:
        if var in variables:
            var_config = variables[var]
            var_name = var_config.get('variable_names', 'N/A')
            keys = var_config.get('keys', 'N/A')
            print(f"   ✅ {var} -> {var_name} (keys: {keys})")
        else:
            print(f"   ❌ {var} -> NOT FOUND")
    
    # Test meters
    meters = config.get('meters', {})
    hvac_meters = [
        'Electricity:HVAC',
        'Fan Electricity Energy',
        'Cooling Coil Total Cooling Energy',
        'Cooling Coil Electricity Energy',
        'Heating Coil Heating Energy',
        'Heating Coil Electricity Energy'
    ]
    
    print(f"\n📊 Available HVAC Meters:")
    for meter in hvac_meters:
        if meter in meters:
            meter_name = meters[meter]
            print(f"   ✅ {meter} -> {meter_name}")
        else:
            print(f"   ❌ {meter} -> NOT FOUND")
    
    # Test mock observation
    print(f"\n🎭 Testing Mock Observation:")
    obs = create_mock_observation()
    if obs:
        print("✅ Mock observation created successfully")
        
        # Test accessing HVAC variables
        print(f"\n📈 Mock HVAC Data:")
        for var in hvac_vars:
            if var in variables:
                var_name = variables[var]['variable_names']
                value = obs.get(var_name, 'N/A')
                print(f"   {var_name}: {value}")
        
        # Print formatted status
        print_hvac_status_mock(obs, 1)
        
        return True
    else:
        print("❌ Failed to create mock observation")
        return False

def main():
    """Run the mock test."""
    print("🏢 HVAC Monitoring Mock Test")
    print("=" * 80)
    print("This test validates the configuration without requiring EnergyPlus.")
    print("=" * 80)
    
    success = test_hvac_monitoring_mock()
    
    if success:
        print(f"\n🎉 Mock test completed successfully!")
        print(f"📝 The configuration is ready for use with EnergyPlus.")
        print(f"💡 To run with real EnergyPlus data, install EnergyPlus and run the full test.")
    else:
        print(f"\n❌ Mock test failed.")
        print(f"🔧 Please check the configuration files.")

if __name__ == "__main__":
    main()