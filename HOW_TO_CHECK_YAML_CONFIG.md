# How to Know Which YAML Configuration File is Being Used

This guide explains how to determine which YAML configuration file your Sinergym code is using during execution.

## Overview

Sinergym automatically loads YAML configuration files from `sinergym/data/default_configuration/` when you import the library. Each YAML file registers one or more environments. The specific YAML file used depends on the **environment ID** you specify when creating an environment.

## New Features Added

I've added the following features to help you track YAML configuration files:

### 1. **Automatic Logging on Import**

When you import sinergym, you'll now see console messages showing:
- Which YAML files are being loaded
- Which environments are registered from each file

```python
import sinergym

# Output will show:
# [SINERGYM] Loading YAML configuration from: /path/to/5ZoneAutoDXVAV.yaml
# [SINERGYM]   -> Registered environment: Eplus-5zone-hot-continuous-v1
# [SINERGYM]   -> Registered environment: Eplus-5zone-mixed-continuous-v1
# ... (and so on for each YAML file)
```

### 2. **Check Specific Environment's YAML File**

Use the `get_yaml_config_file()` function to check which YAML file was used to register a specific environment:

```python
import sinergym

# Check which YAML file is used for a specific environment
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"Environment '{env_id}' uses YAML file: {yaml_file}")
```

### 3. **Print All Environment-to-YAML Mappings**

Use the `print_env_yaml_mapping()` function to see a complete table of all environments and their corresponding YAML files:

```python
import sinergym

# Print a complete mapping of environments to YAML files
sinergym.print_env_yaml_mapping()

# Output will show:
# ====================================================================================================
# [SINERGYM] Environment to YAML Configuration Mapping
# ====================================================================================================
#   Eplus-5zone-hot-continuous-v1                      -> 5ZoneAutoDXVAV.yaml
#   Eplus-5zone-mixed-continuous-v1                    -> 5ZoneAutoDXVAV.yaml
#   Eplus-datacenter-hot-continuous-v1                 -> 2ZoneDataCenterHVAC_wEconomizer.yaml
#   ... (all environments listed)
# ====================================================================================================
```

## Complete Example Usage

Here's a complete example showing how to verify which YAML file your code is using:

```python
import sinergym
import gymnasium as gym

# Step 1: See all environments and their YAML files
print("All environment-to-YAML mappings:")
sinergym.print_env_yaml_mapping()

# Step 2: Check a specific environment before creating it
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_config = sinergym.get_yaml_config_file(env_id)
print(f"\nEnvironment '{env_id}' will use YAML config: {yaml_config}")

# Step 3: Create the environment
env = gym.make(env_id)

# Step 4: Verify again after creation (optional)
yaml_config = sinergym.get_yaml_config_file(env.spec.id)
print(f"Active environment is using: {yaml_config}")

# Use the environment...
env.reset()
# ... your code here ...

env.close()
```

## Understanding the Environment ID to YAML Mapping

The relationship between environment IDs and YAML files follows this pattern:

1. **Each YAML file** in `sinergym/data/default_configuration/` contains configuration for one or more environments
2. **The environment ID** determines which YAML file is used
3. **The YAML file name** typically corresponds to the building model (e.g., `5ZoneAutoDXVAV.yaml` configures the 5-zone building)

### Example Mappings:

| Environment ID | YAML Configuration File |
|----------------|------------------------|
| `Eplus-5zone-hot-continuous-v1` | `5ZoneAutoDXVAV.yaml` |
| `Eplus-5zone-mixed-continuous-v1` | `5ZoneAutoDXVAV.yaml` |
| `Eplus-datacenter-hot-continuous-v1` | `2ZoneDataCenterHVAC_wEconomizer_CW.yaml` |
| `Eplus-office-hot-continuous-v1` | `ASHRAE901_OfficeMedium_STD2019_Denver.yaml` |
| `Eplus-warehouse-hot-continuous-v1` | `ASHRAE901_Warehouse_STD2019_Denver.yaml` |

## Troubleshooting

### If you modified a YAML file but changes aren't reflected:

1. **Check the file location**: Make sure you modified the YAML file in the correct location:
   ```
   /workspace/sinergym/data/default_configuration/<your_file>.yaml
   ```

2. **Verify the environment ID**: Make sure you're creating the correct environment:
   ```python
   yaml_file = sinergym.get_yaml_config_file('your-env-id')
   print(f"Expected YAML: {yaml_file}")
   ```

3. **Reload the module**: If you modified a YAML file, you need to restart your Python session or reload the module:
   ```python
   import importlib
   importlib.reload(sinergym)
   ```

4. **Check for multiple copies**: Search for duplicate YAML files:
   ```bash
   find /workspace -name "*.yaml" -type f | grep -i "your_filename"
   ```

### If you get an error:

1. **Check the import messages**: Look at the console output when you `import sinergym` - it shows all YAML files being loaded
2. **Verify the YAML file exists**: 
   ```bash
   ls -la /workspace/sinergym/data/default_configuration/
   ```
3. **Check YAML syntax**: Make sure your YAML file is valid:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('your_file.yaml'))"
   ```

## Using Custom YAML Files

If you want to use a custom YAML configuration file that's NOT in the default directory:

```python
import sinergym

# Register environments from your custom YAML file
custom_yaml_path = '/path/to/your/custom_config.yaml'
sinergym.register_envs_from_yaml(custom_yaml_path)

# Check what was registered
sinergym.print_env_yaml_mapping()

# Now you can use the environments defined in your custom YAML
import gymnasium as gym
env = gym.make('your-custom-env-id')
```

## Quick Reference Commands

```python
# Print all environment-to-YAML mappings
sinergym.print_env_yaml_mapping()

# Get YAML file for specific environment
yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')

# List all available Sinergym environments
all_envs = sinergym.ids()

# Register custom YAML file
sinergym.register_envs_from_yaml('/path/to/custom.yaml')
```

## Summary

With these new features, you can always know which YAML configuration file your code is using by:

1. **Watching the console output** when you import sinergym
2. **Using `sinergym.get_yaml_config_file(env_id)`** to check a specific environment
3. **Using `sinergym.print_env_yaml_mapping()`** to see all mappings at once

This makes debugging configuration issues much easier!
