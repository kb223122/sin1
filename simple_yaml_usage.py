#!/usr/bin/env python3
"""
Simple script showing how to use your YAML configuration properly.

This addresses the permission denied error and shows the correct way to run verification.
"""

import sys
import os

def show_correct_usage():
    """Show the correct way to use your YAML configuration."""
    
    print("=" * 80)
    print("CORRECT USAGE OF YOUR YAML CONFIGURATION")
    print("=" * 80)
    
    print("\n❌ **WHAT YOU TRIED (WRONG):**")
    print("   '/Users/z5543337/sinergym/venv/lib/python3.12/site-packages/sinergym/data/default_configuration/5ZoneAutoDXVAV_zonewise.yaml'")
    print("   This tries to execute a YAML file as a script, which won't work.")
    
    print("\n✅ **WHAT YOU SHOULD DO (CORRECT):**")
    print("   1. Create a Python script that uses your YAML configuration")
    print("   2. Use gym.make() to create the environment")
    print("   3. Run the Python script, not the YAML file")
    
    print("\n🔧 **STEP-BY-STEP SOLUTION:**")
    print("   1. Copy your YAML configuration to your working directory")
    print("   2. Create a Python script that references your YAML")
    print("   3. Run the Python script with: python script_name.py")
    
    print("\n📁 **FILES YOU NEED:**")
    print("   1. Your YAML configuration file (e.g., '5ZoneAutoDXVAV_zonewise.yaml')")
    print("   2. A Python script that uses the YAML (e.g., 'run_hvac_verification_with_yaml.py')")
    
    print("\n🚀 **QUICK START:**")
    print("   1. Copy your YAML file to your working directory")
    print("   2. Run: python run_hvac_verification_with_yaml.py")
    print("   3. The script will use your YAML configuration automatically")
    
    print("\n🔍 **YOUR YAML CONFIGURATION ISSUES:**")
    print("   1. ✅ YAML structure looks good")
    print("   2. ❌ Missing reward function configuration")
    print("   3. ❌ Some variable names might need adjustment")
    
    print("\n🛠️  **FIXES NEEDED:**")
    print("   1. Add reward function configuration to your YAML")
    print("   2. Ensure all variable names match EnergyPlus outputs")
    print("   3. Use the Python script instead of running YAML directly")
    
    print("\n📋 **REWARD FUNCTION CONFIGURATION TO ADD:**")
    print("   Add this to your YAML file:")
    print("   ```yaml")
    print("   reward: sinergym.utils.rewards:LinearReward")
    print("   reward_kwargs:")
    print("     temperature_variables:")
    print("       - air_temperature_space1")
    print("       - air_temperature_space2")
    print("       - air_temperature_space3")
    print("       - air_temperature_space4")
    print("       - air_temperature_space5")
    print("     energy_variables:")
    print("       - HVAC_electricity_demand_rate")
    print("     range_comfort_winter:")
    print("       - 20.0")
    print("       - 23.5")
    print("     range_comfort_summer:")
    print("       - 23.0")
    print("       - 26.0")
    print("     summer_start:")
    print("       - 6")
    print("       - 1")
    print("     summer_final:")
    print("       - 9")
    print("       - 30")
    print("     energy_weight: 0.5")
    print("     lambda_energy: 1.0e-4")
    print("     lambda_temperature: 1.0")
    print("   ```")
    
    print("\n" + "=" * 80)
    print("✅ **SOLUTION COMPLETE**")
    print("=" * 80)
    
    print("\n📝 **NEXT STEPS:**")
    print("   1. Copy your YAML file to your working directory")
    print("   2. Add the reward function configuration above")
    print("   3. Run: python run_hvac_verification_with_yaml.py")
    print("   4. Check the verification results")

def main():
    """Main function."""
    show_correct_usage()

if __name__ == "__main__":
    main()