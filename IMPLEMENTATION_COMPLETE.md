# ✅ Implementation Complete: YAML Configuration Tracker

## 🎯 Problem Solved

**Your Question:** "How to know which YAML file my code is using during execution?"

**Answer:** I've added logging and utility functions to Sinergym that make it easy to track which YAML configuration file is being used.

---

## 🚀 What You Can Do Now

### Option 1: See Console Output (Automatic)

```python
import sinergym
```

Output shows:
```
[SINERGYM] Loading YAML configuration from: /workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
[SINERGYM]   -> Registered environment: Eplus-5zone-hot-continuous-v1
```

### Option 2: Check Specific Environment

```python
import sinergym

yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')
print(f"YAML file: {yaml_file}")
```

### Option 3: See All Mappings

```python
import sinergym

sinergym.print_env_yaml_mapping()
```

---

## 📝 Changes Made

### Modified: `sinergym/__init__.py`

1. ✅ Added `_env_yaml_mapping` dictionary to track mappings
2. ✅ Added console logging: `[SINERGYM] Loading YAML configuration from: ...`
3. ✅ Added function: `get_yaml_config_file(env_id)`
4. ✅ Added function: `print_env_yaml_mapping()`
5. ✅ Added `Optional` import for type hints

**No breaking changes!** All existing code continues to work.

---

## 📚 Documentation Created

| File | Purpose |
|------|---------|
| **[START_HERE.md](START_HERE.md)** | 🎯 Quick start guide - **READ THIS FIRST** |
| **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** | 📖 Complete solution documentation |
| **[YAML_CONFIG_QUICK_REFERENCE.md](YAML_CONFIG_QUICK_REFERENCE.md)** | ⚡ Quick reference |
| **[HOW_TO_CHECK_YAML_CONFIG.md](HOW_TO_CHECK_YAML_CONFIG.md)** | 🔧 Detailed guide with troubleshooting |
| **[YAML_CONFIG_TRACKER_README.md](YAML_CONFIG_TRACKER_README.md)** | 📋 Feature overview |
| **[example_check_yaml.py](example_check_yaml.py)** | 🚀 Runnable example |
| **[check_yaml_config.py](check_yaml_config.py)** | 📊 Comprehensive demo |

---

## 🎬 Try It Now

### Quick Test

```python
import sinergym

# See all environment-to-YAML mappings
sinergym.print_env_yaml_mapping()

# Check your specific environment
yaml_file = sinergym.get_yaml_config_file('YOUR-ENV-ID')
print(f"Using YAML: {yaml_file}")
```

### Run Example Script

```bash
python3 example_check_yaml.py
```

---

## 🔍 How It Works

```
1. Import sinergym
        ↓
2. System loads YAML files from sinergym/data/default_configuration/
        ↓
3. Console shows which files are loaded [NEW!]
        ↓
4. Each environment is registered
        ↓
5. System tracks which YAML file each environment came from [NEW!]
        ↓
6. You can query this information anytime [NEW!]
```

---

## 🛠️ API Reference

### `sinergym.get_yaml_config_file(env_id: str) -> Optional[str]`

Returns the YAML configuration file path for a given environment ID.

**Example:**
```python
yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')
# Returns: /workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
```

### `sinergym.print_env_yaml_mapping() -> None`

Prints a formatted table of all environment-to-YAML mappings.

**Example:**
```python
sinergym.print_env_yaml_mapping()
# Prints table showing all environments and their YAML files
```

---

## 🐛 Debugging Your Issue

You mentioned getting an error with both modified and default YAML files. Here's how to debug:

### Step 1: Check Console Output
```python
import sinergym
# Watch for [SINERGYM] messages showing which files are loaded
```

### Step 2: Verify Environment ID
```python
# What environment ID are you using?
env_id = 'YOUR-ENV-ID'  # Replace with your actual ID
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"Environment '{env_id}' uses: {yaml_file}")
```

### Step 3: Check File Location
YAML files MUST be in:
```
/workspace/sinergym/data/default_configuration/
```

### Step 4: List YAML Files
```bash
ls -la /workspace/sinergym/data/default_configuration/*.yaml
```

### Step 5: Check for Duplicates
```bash
find /workspace -name "*.yaml" -type f | grep -i "your_filename"
```

### Step 6: Restart Python
After modifying any YAML file, restart your Python session!

---

## 📊 Example Output

### When Importing Sinergym:
```
[SINERGYM] Loading YAML configuration from: /workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
[SINERGYM]   -> Registered environment: Eplus-5zone-hot-continuous-v1
[SINERGYM]   -> Registered environment: Eplus-5zone-mixed-continuous-v1
[SINERGYM]   -> Registered environment: Eplus-5zone-cool-continuous-v1
[SINERGYM] Loading YAML configuration from: /workspace/sinergym/data/default_configuration/2ZoneDataCenterHVAC_wEconomizer_CW.yaml
[SINERGYM]   -> Registered environment: Eplus-datacenter-hot-continuous-v1
...
```

### Using `print_env_yaml_mapping()`:
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

### Using `get_yaml_config_file()`:
```python
>>> yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')
>>> print(yaml_file)
/workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
```

---

## ✨ Benefits

✅ **No more confusion** about which YAML file is being used  
✅ **Easy debugging** of configuration issues  
✅ **Real-time feedback** when importing sinergym  
✅ **Programmatic access** to configuration mappings  
✅ **No breaking changes** to existing code  

---

## 📖 Read Next

1. **[START_HERE.md](START_HERE.md)** - Quick start guide
2. **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** - Complete documentation
3. Run `python3 example_check_yaml.py` - See it in action

---

## 🎉 Summary

**Before:** No way to know which YAML file was being used  
**After:** Three easy methods to check YAML configuration files  

### The Solution:
1. 🖥️ **Console logging** - See YAML files as they load
2. 🔍 **`get_yaml_config_file(env_id)`** - Check specific environment
3. 📋 **`print_env_yaml_mapping()`** - See all mappings

**Implementation complete!** ✅

No more guessing which YAML configuration file your code is using! 🎯
