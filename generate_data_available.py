#!/usr/bin/env python3
"""
Script to generate data_available.txt file to see what variables are actually available.
"""

import gymnasium as gym
import sinergym
import os
import shutil

def generate_data_available():
    """Run a quick simulation to generate data_available.txt"""
    print("🔍 Generating data_available.txt file...")
    
    # Create environment
    env = gym.make('Eplus-5zone-v1')
    
    # Run one step to generate the data_available.txt file
    obs, info = env.reset()
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Find the data_available.txt file
    episode_dir = info.get('episode_path', '')
    if episode_dir:
        data_available_path = os.path.join(episode_dir, 'output', 'data_available.txt')
        if os.path.exists(data_available_path):
            # Copy to current directory for easy access
            shutil.copy2(data_available_path, 'data_available.txt')
            print(f"✅ data_available.txt generated and copied to current directory")
            return True
        else:
            print(f"❌ data_available.txt not found at {data_available_path}")
    else:
        print("❌ Episode path not found in info")
    
    env.close()
    return False

if __name__ == "__main__":
    generate_data_available()