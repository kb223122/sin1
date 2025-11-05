# Solution: How to Know Which YAML Configuration File is Being Used

## Problem Statement
You need to determine which YAML configuration file your Sinergym code is using during execution, especially when you have both modified and default YAML files.

## Solution Implemented

I've enhanced the Sinergym library with logging and utility functions to make it easy to track which YAML configuration file is being used.

---

## Changes Made

### 1. Modified File: `sinergym/__init__.py`

**Added Features:**

#### a) **Console Logging During Import**
- When you import sinergym, it now prints which YAML files are being loaded
- Shows which environments are registered from each YAML file

#### b) **Environment-to-YAML Mapping Dictionary**
- Internal dictionary `_env_yaml_mapping` tracks which YAML file each environment came from

#### c) **New Function: `get_yaml_config_file(env_id)`**
```python
def get_yaml_config_file(env_id: str) -> Optional[str]:
    """
    Get the YAML configuration file path used to register a specific environment.
    
    Args:
        env_id: The environment ID (e.g., 'Eplus-5zone-hot-continuous-v1')
    
    Returns:
        Path to the YAML configuration file, or None if not found
    """
```

#### d) **New Function: `print_env_yaml_mapping()`**
```python
def print_env_yaml_mapping():
    """
    Print a table showing which YAML file was used to register each environment.
    """
```

---

## How to Use

### **Method 1: Watch Console Output During Import**

Simply import sinergym and observe the console messages:

```python
import sinergym
```

**Output:**
```
[SINERGYM] Loading YAML configuration from: /workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
[SINERGYM]   -> Registered environment: Eplus-5zone-hot-continuous-v1
[SINERGYM]   -> Registered environment: Eplus-5zone-mixed-continuous-v1
[SINERGYM]   -> Registered environment: Eplus-5zone-cool-continuous-v1
[SINERGYM] Loading YAML configuration from: /workspace/sinergym/data/default_configuration/2ZoneDataCenterHVAC_wEconomizer_CW.yaml
[SINERGYM]   -> Registered environment: Eplus-datacenter-hot-continuous-v1
... (and so on)
```

### **Method 2: Check a Specific Environment**

```python
import sinergym

# Check which YAML file is used for your environment
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"Environment '{env_id}' uses YAML file: {yaml_file}")
```

**Output:**
```
Environment 'Eplus-5zone-hot-continuous-v1' uses YAML file: /workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
```

### **Method 3: Print All Mappings**

```python
import sinergym

# Show all environment-to-YAML mappings
sinergym.print_env_yaml_mapping()
```

**Output:**
```
====================================================================================================
[SINERGYM] Environment to YAML Configuration Mapping
====================================================================================================
  Eplus-5zone-hot-continuous-v1                      -> 5ZoneAutoDXVAV.yaml
  Eplus-5zone-mixed-continuous-v1                    -> 5ZoneAutoDXVAV.yaml
  Eplus-datacenter-hot-continuous-v1                 -> 2ZoneDataCenterHVAC_wEconomizer_CW.yaml
  ... (all environments)
====================================================================================================
```

### **Method 4: Verify Before Creating Environment**

```python
import sinergym
import gymnasium as gym

# Check configuration before creating the environment
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_config = sinergym.get_yaml_config_file(env_id)
print(f"About to create environment using: {yaml_config}")

# Create the environment
env = gym.make(env_id)

# Your code here...
env.reset()
# ...

env.close()
```

---

## Complete Working Example

```python
import sinergym
import gymnasium as gym

# Step 1: Import shows all YAML files being loaded (see console output)

# Step 2: Print all environment-to-YAML mappings
print("\n=== All Environment-to-YAML Mappings ===")
sinergym.print_env_yaml_mapping()

# Step 3: Check specific environment
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"\n=== Checking Specific Environment ===")
print(f"Environment: {env_id}")
print(f"YAML file: {yaml_file}")

# Step 4: Create and use environment
print(f"\n=== Creating Environment ===")
print(f"Creating environment: {env_id}")
print(f"Using YAML config: {yaml_file}")

env = gym.make(env_id)
obs, info = env.reset()
print(f"Environment created successfully!")
print(f"Observation space: {env.observation_space}")
print(f"Action space: {env.action_space}")

env.close()
```

---

## Files Created

1. **`/workspace/SOLUTION_SUMMARY.md`** (this file) - Complete solution summary
2. **`/workspace/YAML_CONFIG_QUICK_REFERENCE.md`** - Quick reference guide
3. **`/workspace/HOW_TO_CHECK_YAML_CONFIG.md`** - Detailed documentation with troubleshooting
4. **`/workspace/check_yaml_config.py`** - Comprehensive demonstration script
5. **`/workspace/example_check_yaml.py`** - Simple example script

---

## Understanding How It Works

### The Flow:

1. **YAML Location**: YAML files are stored in `sinergym/data/default_configuration/`
2. **Automatic Loading**: When you `import sinergym`, it automatically loads all YAML files from that directory
3. **Environment Registration**: Each YAML file registers one or more environments
4. **Mapping Stored**: The system now stores which YAML file was used for each environment ID
5. **Easy Access**: You can query this mapping anytime using the new functions

### Environment ID → YAML File Relationship:

The environment ID you use when calling `gym.make()` determines which YAML file is used:

```
gym.make('Eplus-5zone-hot-continuous-v1')
    ↓
Uses: 5ZoneAutoDXVAV.yaml
    ↓
Configuration for 5-zone building with hot climate
```

---

## Troubleshooting Your Issue

You mentioned you have both modified and default YAML files. Here's how to verify which one is being used:

### Step 1: Check YAML File Location
```bash
ls -la /workspace/sinergym/data/default_configuration/*.yaml
```

### Step 2: Import Sinergym and Watch Output
```python
import sinergym
# Look for the [SINERGYM] Loading YAML configuration from: messages
```

### Step 3: Verify Your Environment ID
```python
# Check what environment you're creating
env_id = 'YOUR-ENVIRONMENT-ID'  # Replace with your actual ID
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"Environment '{env_id}' uses: {yaml_file}")
```

### Step 4: Check for Duplicate Files
```bash
# Search for duplicate YAML files
find /workspace -name "*.yaml" -type f | grep -i "your_filename"
```

### Common Issues:

1. **Modified wrong file**: The YAML file must be in `sinergym/data/default_configuration/`
2. **Wrong environment ID**: Make sure you're using the correct environment ID that matches your YAML
3. **Need to reload**: After modifying a YAML file, restart your Python session
4. **Multiple copies**: Only the file in `sinergym/data/default_configuration/` is loaded

---

## Testing the Solution

Run the example script to see it in action:

```bash
cd /workspace
python3 example_check_yaml.py
```

Or use it in your own code:

```python
import sinergym

# This will immediately show which YAML files are loaded
sinergym.print_env_yaml_mapping()

# Check your specific environment
yaml_file = sinergym.get_yaml_config_file('YOUR-ENV-ID')
print(f"Using YAML: {yaml_file}")
```

---

## Key Takeaways

✅ **YAML files are automatically loaded** from `sinergym/data/default_configuration/`  
✅ **Environment ID determines which YAML is used**  
✅ **Three ways to check**: console output, `get_yaml_config_file()`, `print_env_yaml_mapping()`  
✅ **Logging happens automatically** when you import sinergym  
✅ **Works for both default and custom YAML files**  

---

## Next Steps

1. **Run the example**: Execute `python3 example_check_yaml.py`
2. **Check your environment**: Use `sinergym.get_yaml_config_file('your-env-id')`
3. **Verify the YAML file**: Make sure you're modifying the correct file
4. **Restart Python**: If you modified a YAML, restart your Python session

---

## Summary

The problem was that there was no easy way to know which YAML configuration file was being used. Now:

- **Automatic logging** shows which files are loaded when you import
- **`get_yaml_config_file(env_id)`** tells you which YAML file a specific environment uses
- **`print_env_yaml_mapping()`** shows all environment-to-YAML mappings
- **Clear console messages** make debugging configuration issues easy

No more guessing which YAML file is being used! 🎉
