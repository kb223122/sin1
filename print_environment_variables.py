#!/usr/bin/env python3
"""
Script to print all observation and action variables with their indices for any Sinergym environment.

Usage:
    python3 print_environment_variables.py
    python3 print_environment_variables.py Eplus-5zone-hot-continuous-v1
"""

import sys
import numpy as np

def print_environment_info(env_id):
    """Print detailed information about an environment's variables."""
    import gymnasium as gym
    import sinergym
    
    print("\n" + "="*80)
    print(f"SINERGYM ENVIRONMENT VARIABLES")
    print("="*80)
    print(f"Environment ID: {env_id}")
    print("="*80)
    
    try:
        # Create environment
        env = gym.make(env_id)
        
        # Get observation and action information
        obs_space = env.observation_space
        action_space = env.action_space
        obs_vars = env.observation_variables
        action_vars = env.action_variables
        
        # Print observation space info
        print(f"\n📥 OBSERVATION SPACE")
        print("-" * 80)
        print(f"Shape: {obs_space.shape}")
        print(f"Total Variables: {len(obs_vars)}")
        print(f"Data Type: {obs_space.dtype}")
        
        # Print observation variables with indices
        print(f"\n📊 OBSERVATION VARIABLES ({len(obs_vars)} total)")
        print("-" * 80)
        print(f"{'Index':<8} {'Variable Name':<40} {'Type/Category'}")
        print("-" * 80)
        
        for i, var_name in enumerate(obs_vars):
            # Categorize variable
            if i == 0:
                category = "Time"
            elif i == 1:
                category = "Time"
            elif i == 2:
                category = "Time"
            elif 'outdoor' in var_name or 'wind' in var_name or 'solar' in var_name:
                category = "Outdoor"
            elif 'temperature' in var_name or 'humidity' in var_name:
                category = "Indoor/Zone"
            elif 'setpoint' in var_name:
                category = "Setpoint"
            elif 'electricity' in var_name or 'power' in var_name or 'rate' in var_name:
                category = "Energy"
            elif 'occupant' in var_name:
                category = "Occupancy"
            else:
                category = "Other"
            
            print(f"[{i:2d}]     {var_name:<40} {category}")
        
        # Print action space info
        print(f"\n📤 ACTION SPACE")
        print("-" * 80)
        print(f"Shape: {action_space.shape}")
        print(f"Total Variables: {len(action_vars)}")
        print(f"Data Type: {action_space.dtype}")
        
        if hasattr(action_space, 'low') and hasattr(action_space, 'high'):
            print(f"Low Bounds: {action_space.low}")
            print(f"High Bounds: {action_space.high}")
        
        # Print action variables with indices
        print(f"\n🎮 ACTION VARIABLES ({len(action_vars)} total)")
        print("-" * 80)
        print(f"{'Index':<8} {'Variable Name':<40} {'Range'}")
        print("-" * 80)
        
        for i, var_name in enumerate(action_vars):
            if hasattr(action_space, 'low') and hasattr(action_space, 'high'):
                low = action_space.low[i]
                high = action_space.high[i]
                range_str = f"[{low:.2f}, {high:.2f}]"
            else:
                range_str = "N/A"
            print(f"[{i:2d}]     {var_name:<40} {range_str}")
        
        # Print example usage
        print("\n" + "="*80)
        print("💡 EXAMPLE USAGE")
        print("="*80)
        
        print("\n# Create environment and get observation")
        print(f"env = gym.make('{env_id}')")
        print("obs, info = env.reset()")
        print(f"print('Observation shape:', obs.shape)  # {obs_space.shape}")
        
        print("\n# Access specific observations by index")
        if len(obs_vars) > 0:
            print(f"month = obs[0]          # {obs_vars[0]}")
        if len(obs_vars) > 2:
            print(f"hour = obs[2]           # {obs_vars[2]}")
        if len(obs_vars) > 3:
            print(f"outdoor_temp = obs[3]   # {obs_vars[3]}")
        if len(obs_vars) > 9:
            print(f"zone_temp = obs[9]      # {obs_vars[9]}")
        
        print("\n# Create and apply action")
        if len(action_vars) == 1:
            low = action_space.low[0]
            high = action_space.high[0]
            mid = (low + high) / 2
            print(f"action = np.array([{mid:.1f}])  # {action_vars[0]}")
        elif len(action_vars) == 2:
            low1, low2 = action_space.low
            high1, high2 = action_space.high
            mid1 = (low1 + high1) / 2
            mid2 = (low2 + high2) / 2
            print(f"action = np.array([{mid1:.1f}, {mid2:.1f}])  # {action_vars}")
        
        print("obs, reward, terminated, truncated, info = env.step(action)")
        
        print("\n" + "="*80)
        print("✅ Done! Use these indices in your code.")
        print("="*80 + "\n")
        
        env.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\nMake sure '{env_id}' is a valid Sinergym environment ID.")
        print("\nAvailable environments:")
        try:
            import sinergym
            envs = sinergym.ids()
            for env in envs[:10]:  # Show first 10
                print(f"  - {env}")
            if len(envs) > 10:
                print(f"  ... and {len(envs) - 10} more")
        except:
            pass
        print()
        return False
    
    return True


def main():
    """Main function."""
    
    # Default environment or from command line
    if len(sys.argv) > 1:
        env_id = sys.argv[1]
    else:
        # Default to 5zone environment
        env_id = 'Eplus-5zone-hot-continuous-v1'
        print("\n💡 No environment specified, using default: " + env_id)
        print("   Usage: python3 print_environment_variables.py <env_id>\n")
    
    # Print environment info
    success = print_environment_info(env_id)
    
    if success and len(sys.argv) == 1:
        # If using default, show other examples
        print("\n" + "="*80)
        print("🔍 TRY OTHER ENVIRONMENTS")
        print("="*80)
        print("\nExamples:")
        print("  python3 print_environment_variables.py Eplus-5zone-hot-continuous-v1")
        print("  python3 print_environment_variables.py Eplus-datacenter_cw-hot-continuous-v1")
        print("  python3 print_environment_variables.py Eplus-smalldatacenter-hot-continuous-v1")
        print("  python3 print_environment_variables.py Eplus-office-hot-continuous-v1")
        print("  python3 print_environment_variables.py Eplus-warehouse-hot-continuous-v1")
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
