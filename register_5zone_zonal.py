#!/usr/bin/env python3
"""
Register the custom 5-zone zonal environment with Sinergym
"""

import sinergym
import gymnasium as gym

# Register the custom 5-zone zonal environment
# This assumes you have placed your YAML config file in the correct location
# You may need to adjust the path based on where you put your config file

# Method 1: Direct registration (if config is in default location)
try:
    # Try to register from the default configuration directory
    sinergym.utils.common.register_envs_from_yaml(
        config_path="sinergym/data/default_configuration/5ZoneAutoDXVAV000.yaml"
    )
    print("Successfully registered environment from default config directory")
except Exception as e:
    print(f"Could not register from default directory: {e}")

# Method 2: Manual registration (if config is elsewhere)
try:
    # You can also manually register by specifying the full path
    # Replace with the actual path to your YAML file
    config_path = "/workspace/5ZoneAutoDXVAV000.yaml"  # Adjust this path
    
    # Load and register the environment
    import yaml
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    # Register the environment
    gym.register(
        id=f"Eplus-{config['id_base']}-hot-continuous-v1",
        entry_point="sinergym.envs:EplusEnv",
        kwargs={
            "idf_file": config["building_file"],
            "weather_file": config["weather_specification"]["weather_files"][0],  # Use first weather file
            "observation_space": config.get("observation_space"),
            "action_space": config.get("action_space"),
            "time_variables": config.get("time_variables", []),
            "variables": config.get("variables", {}),
            "meters": config.get("meters", {}),
            "actuators": config.get("actuators", {}),
            "reward": config.get("reward"),
            "reward_kwargs": config.get("reward_kwargs", {}),
            "weather_variability": config.get("weather_variability"),
            "max_ep_store": config.get("max_ep_store", 10),
            "action_definition": config.get("action_definition"),
            "env_name": config["id_base"]
        }
    )
    print("Successfully registered environment manually")
    
except Exception as e:
    print(f"Could not register manually: {e}")

# Method 3: List available environments
print("\nAvailable Sinergym environments:")
try:
    # List all registered environments
    env_list = [env_id for env_id in gym.envs.registry.keys() if 'Eplus' in env_id]
    for env_id in sorted(env_list):
        print(f"  - {env_id}")
except Exception as e:
    print(f"Could not list environments: {e}")

print("\nTo use your custom environment, make sure to:")
print("1. Place your YAML config file in the correct location")
print("2. Update the config_path variable above")
print("3. Run this script before using the environment")
print("4. Use the environment ID: 'Eplus-5zone-zonal-hot-continuous-v1'")