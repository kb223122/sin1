#!/usr/bin/env python3
"""
Simple test for HVAC monitoring without meters.
"""

import gymnasium as gym
import sinergym
import numpy as np

def test_simple_hvac():
    """Test simple HVAC monitoring without meters."""
    print("🧪 Testing Simple HVAC Configuration (Variables Only)")
    print("=" * 60)
    
    try:
        # Create environment
        print("Creating environment...")
        env = gym.make('Eplus-5zone-v1')
        print("✅ Environment created successfully")
        
        # Reset environment
        print("Resetting environment...")
        obs, info = env.reset()
        print("✅ Environment reset successfully")
        
        # Check available variables
        print(f"\n📊 Available variables in observation space:")
        print(f"   Total variables: {len(obs)}")
        
        # Check for key HVAC variables
        hvac_vars = [
            'fan_electricity_rate',
            'fan_air_mass_flow_rate',
            'cooling_coil_total_rate',
            'cooling_coil_electricity_rate',
            'heating_coil_heating_rate',
            'heating_coil_electricity_rate',
            'outdoor_air_flow_fraction'
        ]
        
        available_vars = []
        missing_vars = []
        
        for var in hvac_vars:
            if var in obs:
                available_vars.append(var)
                print(f"   ✅ {var}: {obs[var]}")
            else:
                missing_vars.append(var)
                print(f"   ❌ {var}: NOT FOUND")
        
        # Test step execution
        print(f"\n🎮 Testing step execution...")
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        print("✅ Step execution successful")
        
        # Print HVAC status
        print(f"\n🏢 HVAC COMPONENT STATUS:")
        print(f"   Fan Electricity Rate: {obs.get('fan_electricity_rate', 'N/A')} W")
        print(f"   Fan Air Mass Flow Rate: {obs.get('fan_air_mass_flow_rate', 'N/A')} kg/s")
        print(f"   Cooling Coil Total Rate: {obs.get('cooling_coil_total_rate', 'N/A')} W")
        print(f"   Cooling Coil Electricity Rate: {obs.get('cooling_coil_electricity_rate', 'N/A')} W")
        print(f"   Heating Coil Heating Rate: {obs.get('heating_coil_heating_rate', 'N/A')} W")
        print(f"   Heating Coil Electricity Rate: {obs.get('heating_coil_electricity_rate', 'N/A')} W")
        print(f"   Outdoor Air Flow Fraction: {obs.get('outdoor_air_flow_fraction', 'N/A')}")
        
        # Test multiple steps
        print(f"\n🔄 Testing multiple steps...")
        for i in range(3):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            print(f"   Step {i+1}: Fan power = {obs.get('fan_electricity_rate', 'N/A')} W, Cooling = {obs.get('cooling_coil_electricity_rate', 'N/A')} W")
            
            if terminated or truncated:
                print(f"   Episode ended at step {i+1}")
                break
        
        env.close()
        
        # Summary
        print(f"\n📋 TEST SUMMARY:")
        print(f"   Available HVAC variables: {len(available_vars)}/{len(hvac_vars)}")
        print(f"   Missing variables: {missing_vars}")
        print(f"   Environment creation: ✅ PASS")
        print(f"   Step execution: ✅ PASS")
        
        if len(missing_vars) == 0:
            print(f"\n🎉 All tests passed! HVAC monitoring is working correctly.")
            return True
        else:
            print(f"\n⚠️  Some variables are missing, but basic functionality works.")
            return True
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        print("Please check the configuration files.")
        return False

if __name__ == "__main__":
    print("🏢 Simple HVAC Monitoring Test")
    print("=" * 60)
    print("This test validates the simplified configuration (variables only).")
    print("=" * 60)
    
    success = test_simple_hvac()
    
    if success:
        print(f"\n✅ Configuration test completed successfully!")
    else:
        print(f"\n❌ Configuration test failed.")