#!/usr/bin/env python3
"""
Simple example showing how to check which YAML configuration file is being used.

This is a minimal example you can run to verify which YAML file your environment uses.
"""

import sys

def main():
    print("="*80)
    print("YAML Configuration Checker - Simple Example")
    print("="*80)
    print()
    
    # Step 1: Import sinergym (this will show YAML loading messages)
    print("Step 1: Importing sinergym...")
    print("(Watch for '[SINERGYM] Loading YAML configuration from:' messages)")
    print("-"*80)
    import sinergym
    print()
    
    # Step 2: Show all environment-to-YAML mappings
    print("Step 2: Showing all environment-to-YAML mappings...")
    print("-"*80)
    sinergym.print_env_yaml_mapping()
    
    # Step 3: Check a specific environment
    print("Step 3: Checking specific environment...")
    print("-"*80)
    
    # Get all available environments
    all_envs = sinergym.ids()
    print(f"Total environments available: {len(all_envs)}")
    
    if all_envs:
        # Pick the first one as an example
        example_env = all_envs[0]
        yaml_file = sinergym.get_yaml_config_file(example_env)
        print(f"\nExample environment: {example_env}")
        print(f"Uses YAML file: {yaml_file}")
        
        # Show a few more examples
        print("\nMore examples:")
        for env_id in all_envs[:5]:  # Show first 5
            yaml_file = sinergym.get_yaml_config_file(env_id)
            yaml_name = yaml_file.split('/')[-1] if yaml_file else 'Unknown'
            print(f"  - {env_id}: {yaml_name}")
    
    print()
    print("="*80)
    print("HOW TO USE IN YOUR CODE:")
    print("="*80)
    print("""
# Method 1: Watch console output when importing
import sinergym  # Look for [SINERGYM] messages

# Method 2: Print all mappings
sinergym.print_env_yaml_mapping()

# Method 3: Check specific environment
yaml_file = sinergym.get_yaml_config_file('YOUR-ENV-ID')
print(f"YAML config: {yaml_file}")

# Method 4: Before creating environment
import gymnasium as gym
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_config = sinergym.get_yaml_config_file(env_id)
print(f"Will use YAML: {yaml_config}")
env = gym.make(env_id)
    """)
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(f"Error: {e}")
        print("\nMake sure sinergym and its dependencies are installed:")
        print("  pip install -e .")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
