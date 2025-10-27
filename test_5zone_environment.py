#!/usr/bin/env python3
"""
Test script to verify the 5-zone zonal environment works correctly
"""

import numpy as np
import gymnasium as gym
import sinergym

def test_environment():
    """Test the 5-zone zonal environment"""
    print("Testing 5-zone zonal environment...")
    
    try:
        # Try to create the environment
        env = gym.make('Eplus-5zone-zonal-hot-continuous-v1')
        print("✓ Environment created successfully")
        
        # Test basic properties
        print(f"✓ Observation space: {env.observation_space}")
        print(f"✓ Action space: {env.action_space}")
        print(f"✓ Action space shape: {env.action_space.shape}")
        print(f"✓ Action space low: {env.action_space.low}")
        print(f"✓ Action space high: {env.action_space.high}")
        
        # Test reset
        obs, info = env.reset()
        print(f"✓ Reset successful, observation shape: {obs.shape}")
        print(f"✓ Info keys: {list(info.keys())}")
        
        # Test step with random action
        action = env.action_space.sample()
        print(f"✓ Random action: {action}")
        
        next_obs, reward, terminated, truncated, info = env.step(action)
        print(f"✓ Step successful")
        print(f"  - Next observation shape: {next_obs.shape}")
        print(f"  - Reward: {reward}")
        print(f"  - Terminated: {terminated}")
        print(f"  - Truncated: {truncated}")
        
        # Test multiple steps
        print("\nTesting multiple steps...")
        for i in range(5):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            print(f"  Step {i+1}: Reward={reward:.4f}, Terminated={terminated}")
            
            if terminated or truncated:
                break
        
        env.close()
        print("✓ Environment closed successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing environment: {e}")
        return False

def test_observation_structure():
    """Test the observation structure and variable names"""
    print("\nTesting observation structure...")
    
    try:
        env = gym.make('Eplus-5zone-zonal-hot-continuous-v1')
        obs, info = env.reset()
        
        # Get observation variables
        obs_vars = env.get_wrapper_attr('observation_variables')
        print(f"✓ Number of observation variables: {len(obs_vars)}")
        
        # Check for zone-specific variables
        zone_vars = {}
        for zone in ['space1', 'space2', 'space3', 'space4', 'space5']:
            zone_vars[zone] = {
                'temp': f'air_temperature_{zone}',
                'humidity': f'air_humidity_{zone}',
                'occupancy': f'air_occ_{zone}',
                'heating_sp': f'htg_setpoint_{zone}',
                'cooling_sp': f'clg_setpoint_{zone}'
            }
        
        print("✓ Zone-specific variables found:")
        for zone, vars in zone_vars.items():
            print(f"  {zone.upper()}:")
            for var_type, var_name in vars.items():
                if var_name in obs_vars:
                    idx = obs_vars.index(var_name)
                    print(f"    {var_type}: {var_name} (index {idx}) = {obs[idx]:.2f}")
                else:
                    print(f"    {var_type}: {var_name} - NOT FOUND")
        
        # Check action variables
        action_vars = env.get_wrapper_attr('action_variables')
        print(f"\n✓ Number of action variables: {len(action_vars)}")
        print("✓ Action variables:")
        for i, var in enumerate(action_vars):
            print(f"  {i}: {var}")
        
        env.close()
        return True
        
    except Exception as e:
        print(f"✗ Error testing observation structure: {e}")
        return False

def test_zone_control():
    """Test zone-wise control logic"""
    print("\nTesting zone-wise control...")
    
    try:
        env = gym.make('Eplus-5zone-zonal-hot-continuous-v1')
        obs, info = env.reset()
        
        # Test different control strategies for each zone
        print("Testing different control strategies:")
        
        # Strategy 1: All zones same setpoints
        action1 = np.array([20.0, 25.0, 20.0, 25.0, 20.0, 25.0, 20.0, 25.0, 20.0, 25.0], dtype=np.float32)
        obs1, reward1, _, _, _ = env.step(action1)
        print(f"  Strategy 1 (uniform): Reward = {reward1:.4f}")
        
        # Strategy 2: Different setpoints per zone
        action2 = np.array([18.0, 22.0, 20.0, 24.0, 22.0, 26.0, 19.0, 23.0, 21.0, 25.0], dtype=np.float32)
        obs2, reward2, _, _, _ = env.step(action2)
        print(f"  Strategy 2 (varied): Reward = {reward2:.4f}")
        
        # Strategy 3: Extreme setpoints (should be clipped)
        action3 = np.array([5.0, 35.0, 5.0, 35.0, 5.0, 35.0, 5.0, 35.0, 5.0, 35.0], dtype=np.float32)
        action3_clipped = np.clip(action3, env.action_space.low, env.action_space.high)
        obs3, reward3, _, _, _ = env.step(action3_clipped)
        print(f"  Strategy 3 (extreme, clipped): Reward = {reward3:.4f}")
        print(f"    Original: {action3}")
        print(f"    Clipped:  {action3_clipped}")
        
        env.close()
        return True
        
    except Exception as e:
        print(f"✗ Error testing zone control: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("5-ZONE ZONAL ENVIRONMENT TEST SUITE")
    print("="*60)
    
    # Run tests
    test1 = test_environment()
    test2 = test_observation_structure()
    test3 = test_zone_control()
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"Environment creation: {'PASS' if test1 else 'FAIL'}")
    print(f"Observation structure: {'PASS' if test2 else 'FAIL'}")
    print(f"Zone control: {'PASS' if test3 else 'FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n✓ All tests passed! Environment is ready to use.")
    else:
        print("\n✗ Some tests failed. Check the error messages above.")
    
    print("="*60)