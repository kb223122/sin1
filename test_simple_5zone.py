#!/usr/bin/env python3
"""
Test script for simplified 5-zone individual control environment
"""

import gymnasium as gym
import sinergym
from sinergym import register_envs_from_yaml

def test_simple_environment():
    """Test the simplified 5-zone environment"""
    try:
        # Register the environment
        print("🔧 Registering environment...")
        register_envs_from_yaml('/workspace/5zone_individual_working.yaml')
        
        # Create environment
        print("🏗️ Creating environment...")
        env = gym.make('Eplus-5zone_individual-hot-continuous-v1')
        
        print(f"📊 Environment ID: {env.spec.id}")
        print(f"📊 Observation space: {env.observation_space}")
        print(f"📊 Action space: {env.action_space}")
        
        # Reset and get observations
        print("🔄 Testing environment...")
        obs, info = env.reset()
        print(f"✅ Reset successful! Observation type: {type(obs)}")
        
        if hasattr(obs, 'keys'):
            obs_keys = list(obs.keys())
            print(f"📋 Observation keys: {obs_keys}")
            
            # Check for expected keys
            expected_keys = ['air_temperature', 'air_humidity', 'people_occupant', 
                           'htg_setpoint', 'clg_setpoint', 'outdoor_temperature']
            missing_keys = [key for key in expected_keys if key not in obs_keys]
            if missing_keys:
                print(f"⚠️  Missing expected keys: {missing_keys}")
            else:
                print("✅ All expected observation keys present")
        else:
            print(f"📊 Observation values: {obs[:10] if len(obs) > 10 else obs}")
        
        # Test action
        print("🎯 Testing action...")
        action = env.action_space.sample()
        print(f"📤 Sample action: {action}")
        
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"✅ Step successful! Reward: {reward:.4f}")
        
        # Test a few more steps
        print("🔄 Testing multiple steps...")
        for i in range(2):
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            print(f"  Step {i+1}: Reward = {reward:.4f}")
            
            if terminated or truncated:
                print("  Episode ended, resetting...")
                obs, info = env.reset()
                break

        env.close()
        print("✅ Environment closed successfully!")
        print("🎉 Basic test passed! The environment is working.")
        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_environment()
    if success:
        print("\n🚀 The simplified environment works! You can now use this configuration.")
        print("📝 Note: This version controls all 5 zones but only monitors zone 1.")
        print("   For full individual zone monitoring, we'll need to extend this further.")
    else:
        print("\n❌ There are still issues to resolve.")