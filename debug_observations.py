#!/usr/bin/env python3
"""
Debug script to check what observation variables are actually generated
"""

import gymnasium as gym
import sinergym
from sinergym import register_envs_from_yaml

def debug_observations():
    """Debug the observation variables"""
    try:
        # Register the environment
        print("🔧 Registering environment...")
        register_envs_from_yaml('/workspace/5zone_individual_final.yaml')
        
        # Create environment
        print("🏗️ Creating environment...")
        env = gym.make('Eplus-5zone_individual-hot-continuous-v1')
        
        # Reset and get observations
        print("🔄 Getting observations...")
        obs, info = env.reset()
        
        print(f"📊 Observation type: {type(obs)}")
        print(f"📊 Observation shape: {obs.shape if hasattr(obs, 'shape') else 'N/A'}")
        
        if hasattr(obs, 'keys'):
            obs_keys = list(obs.keys())
            print(f"📋 Total observation keys: {len(obs_keys)}")
            print("📋 Observation keys:")
            for i, key in enumerate(obs_keys):
                print(f"  {i+1:2d}. {key}")
            
            # Check for zone temperature variables
            zone_temp_keys = [key for key in obs_keys if 'air_temperature' in key]
            print(f"\n🌡️ Zone temperature variables found: {len(zone_temp_keys)}")
            for key in zone_temp_keys:
                print(f"  - {key}")
            
            # Check for any zone-related variables
            zone_keys = [key for key in obs_keys if 'zone' in key.lower()]
            print(f"\n🏠 Zone-related variables found: {len(zone_keys)}")
            for key in zone_keys:
                print(f"  - {key}")
                
        else:
            print("❌ Observations don't have keys - this might be a numpy array")
            print(f"   First few values: {obs[:10] if len(obs) > 10 else obs}")
        
        env.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_observations()