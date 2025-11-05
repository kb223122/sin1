# 🎯 How to Know Which YAML Configuration File is Being Used

## ⚡ Quick Answer

Your code now has **3 ways** to determine which YAML configuration file is being used:

### 1️⃣ **Automatic Logging (Easiest)**

Just import sinergym and watch the console:

```python
import sinergym
```

**You'll see:**
```
[SINERGYM] Loading YAML configuration from: /workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
[SINERGYM]   -> Registered environment: Eplus-5zone-hot-continuous-v1
[SINERGYM]   -> Registered environment: Eplus-5zone-mixed-continuous-v1
...
```

### 2️⃣ **Check Specific Environment**

```python
import sinergym

# Replace with your environment ID
env_id = 'Eplus-5zone-hot-continuous-v1'
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"Environment '{env_id}' uses: {yaml_file}")
```

### 3️⃣ **See All Mappings**

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
  Eplus-datacenter-hot-continuous-v1                 -> 2ZoneDataCenterHVAC_wEconomizer_CW.yaml
  ...
====================================================================================================
```

---

## 📚 Documentation

| File | What's Inside |
|------|--------------|
| **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** | 📖 Complete solution with detailed examples |
| **[YAML_CONFIG_QUICK_REFERENCE.md](YAML_CONFIG_QUICK_REFERENCE.md)** | ⚡ Quick reference guide |
| **[HOW_TO_CHECK_YAML_CONFIG.md](HOW_TO_CHECK_YAML_CONFIG.md)** | 🔧 Detailed guide with troubleshooting |
| **[YAML_CONFIG_TRACKER_README.md](YAML_CONFIG_TRACKER_README.md)** | 📋 Feature overview and API reference |

---

## 🚀 Try It Now

Run this simple example:

```bash
python3 example_check_yaml.py
```

Or use this in your code:

```python
import sinergym
import gymnasium as gym

# Check all mappings
sinergym.print_env_yaml_mapping()

# Check your specific environment
env_id = 'YOUR-ENV-ID'  # Replace with your environment
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"\n✅ Environment '{env_id}' uses: {yaml_file}")

# Create environment
env = gym.make(env_id)
env.close()
```

---

## 🔍 Solving Your Problem

**You said:** "I kept both modified and default YAML file at the same place... but I am still getting the error"

**Here's how to debug:**

### Step 1: Check file location
Your YAML files MUST be in:
```
/workspace/sinergym/data/default_configuration/
```

### Step 2: Import sinergym and watch output
```python
import sinergym
# Look at console output - it shows which YAML files are loaded
```

### Step 3: Check which environment you're using
```python
env_id = 'YOUR-ENVIRONMENT-ID'  # What did you pass to gym.make()?
yaml_file = sinergym.get_yaml_config_file(env_id)
print(f"This environment uses: {yaml_file}")
```

### Step 4: Verify it's the right file
```bash
ls -la /workspace/sinergym/data/default_configuration/
```

### Step 5: Check for duplicates
```bash
find /workspace -name "*.yaml" -type f | grep -i "your_filename"
```

### Step 6: Restart Python
After modifying a YAML file, you MUST restart your Python session:
- Close your Python script/notebook
- Restart it
- Import sinergym again

---

## ✨ What Changed?

### Modified File: `sinergym/__init__.py`

**Added:**
1. ✅ Console logging when YAML files are loaded
2. ✅ Internal dictionary tracking environment-to-YAML mappings  
3. ✅ `get_yaml_config_file(env_id)` function
4. ✅ `print_env_yaml_mapping()` function

**No breaking changes** - all existing code still works!

---

## 💡 Key Concepts

### Environment ID → YAML File

When you do this:
```python
env = gym.make('Eplus-5zone-hot-continuous-v1')
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                       Environment ID
```

That environment ID determines which YAML file is used:
```
'Eplus-5zone-hot-continuous-v1' → 5ZoneAutoDXVAV.yaml
```

### Where are YAML files?

Default location:
```
/workspace/sinergym/data/default_configuration/
    ├── 5ZoneAutoDXVAV.yaml
    ├── 2ZoneDataCenterHVAC_wEconomizer_CW.yaml
    ├── ASHRAE901_OfficeMedium_STD2019_Denver.yaml
    └── ... (other YAML files)
```

---

## 🎉 Summary

**Problem:** No way to know which YAML file is being used

**Solution:** Added automatic logging and utility functions

**Result:** You can now always know which YAML configuration file your code is using!

### The 3 Methods:

| Method | When to Use |
|--------|------------|
| **Console Output** | When you import sinergym |
| **`get_yaml_config_file(env_id)`** | To check a specific environment |
| **`print_env_yaml_mapping()`** | To see all environment-to-YAML mappings |

---

## 📞 Next Steps

1. ✅ **Import sinergym** and watch the console output
2. ✅ **Use `sinergym.print_env_yaml_mapping()`** to see all mappings
3. ✅ **Use `sinergym.get_yaml_config_file('your-env-id')`** to check your specific environment
4. ✅ **Verify your YAML file location** is correct
5. ✅ **Restart Python** after modifying any YAML files

---

## 🆘 Still Having Issues?

1. Read **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** for detailed explanation
2. Read **[HOW_TO_CHECK_YAML_CONFIG.md](HOW_TO_CHECK_YAML_CONFIG.md)** for troubleshooting
3. Run `python3 example_check_yaml.py` to see it in action

---

**No more guessing which YAML file is being used! 🎯**
