#!/usr/bin/env python3
"""
Script to check which YAML configuration file is being used for Sinergym environments.

This script demonstrates how to:
1. See which YAML file each environment was registered from
2. Check the YAML file for a specific environment
3. Print all environment-to-YAML mappings
"""

import sinergym
import gymnasium as gym

def main():
    print("\n" + "="*100)
    print("SINERGYM YAML CONFIGURATION CHECKER")
    print("="*100)
    
    # Method 1: Print all environment-to-YAML mappings
    print("\n[Method 1] All Environment to YAML Configuration Mappings:")
    sinergym.print_env_yaml_mapping()
    
    # Method 2: Check YAML file for a specific environment
    print("\n[Method 2] Check specific environment:")
    
    # List all available environments
    available_envs = sinergym.ids()
    print(f"\nTotal Sinergym environments available: {len(available_envs)}")
    
    if available_envs:
        # Check a few example environments
        example_env_id = available_envs[0]
        yaml_file = sinergym.get_yaml_config_file(example_env_id)
        print(f"\nExample: Environment '{example_env_id}'")
        print(f"  -> Uses YAML file: {yaml_file}")
        
        # Method 3: When creating an environment, you can check its config
        print("\n[Method 3] Creating an environment and checking its configuration:")
        print(f"\nCreating environment: {example_env_id}")
        env = gym.make(example_env_id)
        yaml_config = sinergym.get_yaml_config_file(example_env_id)
        print(f"This environment is configured by: {yaml_config}")
        env.close()
    
    # Method 4: Check if you're using a custom environment ID
    print("\n[Method 4] How to check your specific environment:")
    print("  Use: sinergym.get_yaml_config_file('YOUR_ENV_ID')")
    print("  Example:")
    print("    import sinergym")
    print("    yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')")
    print("    print(f'YAML config: {yaml_file}')")
    
    print("\n" + "="*100)
    print("TIPS:")
    print("="*100)
    print("1. When you import sinergym, you'll see '[SINERGYM] Loading YAML configuration from: ...' messages")
    print("2. Each environment is registered with messages like '[SINERGYM]   -> Registered environment: ...'")
    print("3. Use sinergym.print_env_yaml_mapping() anytime to see all mappings")
    print("4. Use sinergym.get_yaml_config_file('env_id') to check a specific environment")
    print("="*100 + "\n")

if __name__ == "__main__":
    main()
