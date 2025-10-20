#!/usr/bin/env python3
"""
Test script for corrected 5-zone individual control environment
"""

import gymnasium as gym
import sinergym
from sinergym import register_envs_from_yaml

def test_environment():
    """Test the corrected 5-zone environment"""
    try:
        # Register the custom environment from YAML
        print("🔧 Registering environment...")
        register_envs_from_yaml('/workspace/5zone_individual_corrected_final.yaml')
        print("✅ Environment registered successfully!")

        # Create the environment
        print("🏗️ Creating environment...")
        env = gym.make('Eplus-5zone_individual-hot-continuous-v1')
        print("✅ Environment created successfully!")

        # Print environment details
        print(f"📊 Environment ID: {env.spec.id}")
        print(f"📊 Observation space: {env.observation_space}")
        print(f"📊 Action space: {env.action_space}")

        # Test basic functionality
        print("🔄 Testing environment...")
        obs, info = env.reset()
        print(f"✅ Reset successful! Observation shape: {obs.shape}")
        
        # Check if observation contains expected keys
        if hasattr(obs, 'keys'):
            obs_keys = list(obs.keys())
            print(f"📋 Observation keys: {obs_keys[:10]}...")  # Show first 10 keys
            
            # Check for zone temperature variables
            zone_temp_keys = [key for key in obs_keys if 'air_temperature_zone' in key]
            print(f"🌡️ Zone temperature variables: {zone_temp_keys}")
            
            if len(zone_temp_keys) == 5:
                print("✅ All 5 zone temperature variables found!")
            else:
                print(f"❌ Expected 5 zone temperature variables, found {len(zone_temp_keys)}")

        # Test a simple action
        print("🎯 Testing action...")
        action = env.action_space.sample()
        print(f"📤 Sample action: {action}")
        
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"✅ Step successful! Reward: {reward:.4f}")
        
        # Test a few more steps
        print("🔄 Testing multiple steps...")
        for i in range(3):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            print(f"  Step {i+1}: Reward = {reward:.4f}, Terminated = {terminated}, Truncated = {truncated}")
            
            if terminated or truncated:
                print("  Episode ended, resetting...")
                obs, info = env.reset()
                break

        env.close()
        print("✅ Environment closed successfully!")
        print("🎉 All tests passed! The environment is working correctly.")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_environment()
    if success:
        print("\n🚀 Ready to use! You can now run your multiaction.py script.")
    else:
        print("\n❌ There are still issues to resolve.")