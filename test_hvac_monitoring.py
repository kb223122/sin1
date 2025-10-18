#!/usr/bin/env python3
"""
Test script for HVAC monitoring implementation.
This script verifies that the modified configuration files work correctly.
"""

import gymnasium as gym
import sinergym
import sys
import os

def test_environment_creation():
    """Test if the environment can be created with the new configuration."""
    try:
        print("🧪 Testing environment creation...")
        env = gym.make('Eplus-5zone-v1')
        print("✅ Environment created successfully!")
        return env
    except Exception as e:
        print(f"❌ Failed to create environment: {e}")
        return None

def test_observation_space(env):
    """Test if the observation space includes the new HVAC variables."""
    if env is None:
        return False
    
    try:
        print("\n🧪 Testing observation space...")
        obs, info = env.reset()
        
        # Check for key HVAC variables
        hvac_variables = [
            'fan_electricity_rate',
            'cooling_coil_electricity_rate', 
            'heating_coil_electricity_rate',
            'cooling_coil_runtime_fraction',
            'outdoor_air_flow_fraction',
            'supply_air_temp',
            'mixed_air_temp'
        ]
        
        missing_vars = []
        for var in hvac_variables:
            if var not in obs:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing variables: {missing_vars}")
        else:
            print("✅ All key HVAC variables found in observation space!")
        
        # Print sample values
        print("\n📊 Sample HVAC values:")
        for var in hvac_variables:
            if var in obs:
                print(f"   {var}: {obs[var]}")
        
        return len(missing_vars) == 0
        
    except Exception as e:
        print(f"❌ Error testing observation space: {e}")
        return False

def test_step_execution(env):
    """Test if the environment can execute steps with HVAC monitoring."""
    if env is None:
        return False
    
    try:
        print("\n🧪 Testing step execution...")
        obs, info = env.reset()
        
        # Take a few steps
        for i in range(3):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            print(f"   Step {i+1}: HVAC demand = {obs.get('HVAC_electricity_demand_rate', 'N/A')} W")
            
            if terminated or truncated:
                break
        
        print("✅ Step execution successful!")
        return True
        
    except Exception as e:
        print(f"❌ Error during step execution: {e}")
        return False

def main():
    """Run all tests."""
    print("🏢 HVAC Monitoring Implementation Test")
    print("=" * 50)
    
    # Test 1: Environment creation
    env = test_environment_creation()
    
    # Test 2: Observation space
    obs_test_passed = test_observation_space(env)
    
    # Test 3: Step execution
    step_test_passed = test_step_execution(env)
    
    # Clean up
    if env:
        env.close()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY:")
    print(f"   Environment Creation: {'✅ PASS' if env else '❌ FAIL'}")
    print(f"   Observation Space: {'✅ PASS' if obs_test_passed else '❌ FAIL'}")
    print(f"   Step Execution: {'✅ PASS' if step_test_passed else '❌ FAIL'}")
    
    if env and obs_test_passed and step_test_passed:
        print("\n🎉 All tests passed! HVAC monitoring is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)