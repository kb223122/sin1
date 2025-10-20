#!/usr/bin/env python3
"""
Test script for 5-zone individual control environment
"""

import gymnasium as gym
import sinergym
from sinergym import register_envs_from_yaml

# Register the custom environment from YAML
register_envs_from_yaml('/workspace/5zone_individual_corrected.yaml')

# Now you can use the environment
env = gym.make('Eplus-5zone_individual-hot-continuous-v1')

print("Environment created successfully!")
print(f"Environment ID: {env.spec.id}")
print(f"Observation space: {env.observation_space}")
print(f"Action space: {env.action_space}")

# Test basic functionality
obs, info = env.reset()
print(f"Initial observation shape: {obs.shape}")
print(f"Observation keys: {list(obs.keys()) if hasattr(obs, 'keys') else 'N/A'}")

# Test a simple action
action = env.action_space.sample()
print(f"Sample action: {action}")

obs, reward, terminated, truncated, info = env.step(action)
print(f"Step successful! Reward: {reward}")

env.close()
print("Environment closed successfully!")