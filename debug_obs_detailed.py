#!/usr/bin/env python3
"""
Deep analysis of observation variables to understand the naming issue
"""

import gymnasium as gym
import sinergym
from sinergym import register_envs_from_yaml

def debug_observations_detailed():
    """Deep debug of observation variables"""
    try:
        # Register the environment
        print("🔧 Registering environment...")
        register_envs_from_yaml('/workspace/5zone_individual_final_working.yaml')
        
        # Create environment
        print("🏗️ Creating environment...")
        env = gym.make('Eplus-5zone_individual-hot-continuous-v1')
        
        # Get observation variables before reset
        print("📋 Getting observation variables...")
        obs_vars = env.get_wrapper_attr("observation_variables")
        print(f"📊 Total observation variables: {len(obs_vars)}")
        print("📋 All observation variables:")
        for i, var in enumerate(obs_vars):
            print(f"  {i+1:3d}. {var}")
        
        # Reset and get observations
        print("\n🔄 Getting observations...")
        obs, info = env.reset()
        print(f"📊 Observation type: {type(obs)}")
        print(f"📊 Observation shape: {obs.shape if hasattr(obs, 'shape') else 'N/A'}")
        
        # Create observation dictionary
        obs_dict = dict(zip(obs_vars, obs))
        print(f"📊 Observation dict keys: {len(obs_dict)}")
        
        # Check for zone temperature variables
        zone_temp_keys = [key for key in obs_dict.keys() if 'air_temperature' in key]
        print(f"\n🌡️ Zone temperature variables found: {len(zone_temp_keys)}")
        for key in zone_temp_keys:
            print(f"  - {key}: {obs_dict[key]}")
        
        # Check for any zone-related variables
        zone_keys = [key for key in obs_dict.keys() if 'space' in key.lower()]
        print(f"\n🏠 Zone-related variables found: {len(zone_keys)}")
        for key in zone_keys:
            print(f"  - {key}: {obs_dict[key]}")
        
        # Check what the reward function expects
        print(f"\n🎯 Reward function temperature variables:")
        try:
            reward_fn = env.get_wrapper_attr("reward_fn")
            if hasattr(reward_fn, 'temp_names'):
                print(f"  Expected: {reward_fn.temp_names}")
                missing = [name for name in reward_fn.temp_names if name not in obs_dict]
                if missing:
                    print(f"  ❌ Missing: {missing}")
                else:
                    print(f"  ✅ All present!")
        except Exception as e:
            print(f"  Could not get reward function details: {e}")
        
        # Check if we can find the variables with different naming
        print(f"\n🔍 Searching for temperature variables with different patterns:")
        patterns = ['air_temperature', 'temperature', 'zone', 'space']
        for pattern in patterns:
            matches = [key for key in obs_dict.keys() if pattern in key.lower()]
            if matches:
                print(f"  Pattern '{pattern}': {matches}")
        
        env.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_observations_detailed()