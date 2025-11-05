# YAML Configuration Tracker for Sinergym

## Quick Start

To find out which YAML configuration file your code is using:

```python
import sinergym

# Method 1: See which YAML files are loaded (automatic on import)
# Look for console messages: [SINERGYM] Loading YAML configuration from: ...

# Method 2: Check a specific environment
yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')
print(f"YAML file: {yaml_file}")

# Method 3: See all mappings
sinergym.print_env_yaml_mapping()
```

---

## What's New?

✨ **Three new ways to track YAML configuration files:**

1. **Automatic Console Logging**: See which YAML files are loaded when you import sinergym
2. **`get_yaml_config_file(env_id)`**: Function to check which YAML file a specific environment uses
3. **`print_env_yaml_mapping()`**: Function to print all environment-to-YAML mappings

---

## Documentation Files

| File | Description |
|------|-------------|
| **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** | 📖 Complete solution overview with examples |
| **[YAML_CONFIG_QUICK_REFERENCE.md](YAML_CONFIG_QUICK_REFERENCE.md)** | ⚡ Quick reference for common tasks |
| **[HOW_TO_CHECK_YAML_CONFIG.md](HOW_TO_CHECK_YAML_CONFIG.md)** | 🔧 Detailed guide with troubleshooting |
| **[example_check_yaml.py](example_check_yaml.py)** | 🚀 Simple runnable example |
| **[check_yaml_config.py](check_yaml_config.py)** | 📊 Comprehensive demonstration script |

---

## Quick Examples

### Example 1: Check which YAML file is used for your environment

```python
import sinergym

env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"Environment: {env_id}")
print(f"YAML file: {yaml_file}")
```

**Output:**
```
Environment: Eplus-5zone-hot-continuous-v1
YAML file: /workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
```

### Example 2: See all environment-to-YAML mappings

```python
import sinergym

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
  ...
====================================================================================================
```

### Example 3: Verify configuration before creating environment

```python
import sinergym
import gymnasium as gym

# Check before creating
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_config = sinergym.get_yaml_config_file(env_id)
print(f"Will use YAML: {yaml_config}")

# Create environment
env = gym.make(env_id)
env.close()
```

---

## Running the Examples

### Simple Example
```bash
python3 example_check_yaml.py
```

### Comprehensive Example
```bash
python3 check_yaml_config.py
```

---

## API Reference

### `sinergym.get_yaml_config_file(env_id: str) -> Optional[str]`

Get the YAML configuration file path for a specific environment.

**Parameters:**
- `env_id` (str): The environment ID (e.g., 'Eplus-5zone-hot-continuous-v1')

**Returns:**
- Path to the YAML configuration file, or None if not found

**Example:**
```python
yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')
```

---

### `sinergym.print_env_yaml_mapping()`

Print a formatted table showing all environment-to-YAML mappings.

**Parameters:** None

**Returns:** None (prints to console)

**Example:**
```python
sinergym.print_env_yaml_mapping()
```

---

## How It Works

```
1. You import sinergym
        ↓
2. System loads all YAML files from sinergym/data/default_configuration/
        ↓
3. Each YAML file registers one or more environments
        ↓
4. System tracks which YAML file each environment came from
        ↓
5. You can query this information using the new functions
```

---

## Troubleshooting

### Problem: Modified YAML file but changes aren't reflected

**Solutions:**
1. Verify file location: `sinergym/data/default_configuration/<filename>.yaml`
2. Check environment ID: `sinergym.get_yaml_config_file('your-env-id')`
3. Restart Python session after modifying YAML files
4. Check for duplicates: `find /workspace -name "*.yaml" -type f`

### Problem: Don't know which environment ID to use

**Solution:**
```python
import sinergym

# List all available environments
all_envs = sinergym.ids()
print(f"Available environments: {all_envs}")

# Show which YAML file each uses
sinergym.print_env_yaml_mapping()
```

### Problem: Getting an error when creating environment

**Solution:**
```python
import sinergym

# Check if environment exists
env_id = 'YOUR-ENV-ID'
yaml_file = sinergym.get_yaml_config_file(env_id)

if yaml_file:
    print(f"Environment '{env_id}' exists")
    print(f"Uses YAML: {yaml_file}")
else:
    print(f"Environment '{env_id}' not found")
    print("Available environments:")
    for env in sinergym.ids():
        print(f"  - {env}")
```

---

## Modified Files

### `sinergym/__init__.py`

**Changes:**
- Added `_env_yaml_mapping` dictionary to track environment-to-YAML mappings
- Added console logging when loading YAML files
- Added `get_yaml_config_file()` function
- Added `print_env_yaml_mapping()` function
- Added logging when registering environments

---

## Key Concepts

### Environment ID
The string you pass to `gym.make()`:
```python
env = gym.make('Eplus-5zone-hot-continuous-v1')
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                    Environment ID
```

### YAML Configuration File
The file that defines the environment settings. Located in:
```
sinergym/data/default_configuration/
    ├── 5ZoneAutoDXVAV.yaml
    ├── 2ZoneDataCenterHVAC_wEconomizer_CW.yaml
    ├── ASHRAE901_OfficeMedium_STD2019_Denver.yaml
    └── ... (more YAML files)
```

### Mapping
The relationship between an environment ID and its YAML file:
```
'Eplus-5zone-hot-continuous-v1' → '5ZoneAutoDXVAV.yaml'
```

---

## Summary

You can now easily determine which YAML configuration file is being used by:

1. ✅ Watching console output when importing sinergym
2. ✅ Using `sinergym.get_yaml_config_file(env_id)`
3. ✅ Using `sinergym.print_env_yaml_mapping()`

No more confusion about which configuration file is active! 🎉

---

## Additional Resources

- **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** - Full solution documentation
- **[YAML_CONFIG_QUICK_REFERENCE.md](YAML_CONFIG_QUICK_REFERENCE.md)** - Quick reference
- **[HOW_TO_CHECK_YAML_CONFIG.md](HOW_TO_CHECK_YAML_CONFIG.md)** - Detailed guide

---

## License

This enhancement follows the same license as the Sinergym project.

---

## Support

If you have questions or issues:
1. Check the documentation files above
2. Run `example_check_yaml.py` to see it in action
3. Use `sinergym.print_env_yaml_mapping()` to verify your configuration
