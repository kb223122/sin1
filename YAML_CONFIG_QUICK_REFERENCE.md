# YAML Configuration Quick Reference

## Problem
You need to know which YAML configuration file your Sinergym code is using during execution.

## Solution Summary

I've added 3 new features to help you track YAML configuration files:

### 1. **Automatic Console Logging**
When you import sinergym, you'll see which YAML files are loaded:

```python
import sinergym
```

Output:
```
[SINERGYM] Loading YAML configuration from: /path/to/5ZoneAutoDXVAV.yaml
[SINERGYM]   -> Registered environment: Eplus-5zone-hot-continuous-v1
[SINERGYM]   -> Registered environment: Eplus-5zone-mixed-continuous-v1
...
```

### 2. **Function: `get_yaml_config_file(env_id)`**
Get the YAML file for a specific environment:

```python
yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')
print(f"YAML config: {yaml_file}")
```

### 3. **Function: `print_env_yaml_mapping()`**
Print all environment-to-YAML mappings:

```python
sinergym.print_env_yaml_mapping()
```

Output:
```
====================================================================================================
[SINERGYM] Environment to YAML Configuration Mapping
====================================================================================================
  Eplus-5zone-hot-continuous-v1                      -> 5ZoneAutoDXVAV.yaml
  Eplus-datacenter-hot-continuous-v1                 -> 2ZoneDataCenterHVAC_wEconomizer_CW.yaml
  ...
====================================================================================================
```

## Complete Example

```python
import sinergym
import gymnasium as gym

# Method 1: See console output when importing
# (Already done above)

# Method 2: Print all mappings
sinergym.print_env_yaml_mapping()

# Method 3: Check specific environment
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_config = sinergym.get_yaml_config_file(env_id)
print(f"Environment '{env_id}' uses: {yaml_config}")

# Method 4: Verify before creating environment
env = gym.make(env_id)
print(f"Active environment uses: {sinergym.get_yaml_config_file(env.spec.id)}")
env.close()
```

## Files Modified

1. `/workspace/sinergym/__init__.py` - Added logging and utility functions

## Files Created

1. `/workspace/check_yaml_config.py` - Demonstration script
2. `/workspace/HOW_TO_CHECK_YAML_CONFIG.md` - Detailed documentation
3. `/workspace/YAML_CONFIG_QUICK_REFERENCE.md` - This quick reference

## Key Points

✅ **YAML files are loaded from**: `sinergym/data/default_configuration/`  
✅ **Environment ID determines which YAML is used**  
✅ **You can now see which YAML file is loaded in real-time**  
✅ **Three methods to check: console output, `get_yaml_config_file()`, and `print_env_yaml_mapping()`**  

## Troubleshooting

If changes to your YAML file aren't reflected:

1. Verify file location: `sinergym/data/default_configuration/<filename>.yaml`
2. Check you're using the right environment ID: `sinergym.get_yaml_config_file('your-env-id')`
3. Restart Python session after modifying YAML files
4. Check for duplicate YAML files: `find /workspace -name "*.yaml" -type f`

## Next Steps

1. Import sinergym and observe the console output
2. Use `sinergym.print_env_yaml_mapping()` to see all mappings
3. Use `sinergym.get_yaml_config_file('your-env-id')` to check your specific environment
