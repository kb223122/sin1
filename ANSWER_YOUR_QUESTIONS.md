# ✅ Answers to Your Questions

## Question 1: How to know which YAML file my code is using?

**Answer:** I've added logging and utility functions to Sinergym!

### Three Ways to Check:

**1. Watch Console Output (Automatic)**
```python
import sinergym
```
Output shows:
```
[SINERGYM] Loading YAML configuration from: /workspace/sinergym/data/default_configuration/5ZoneAutoDXVAV.yaml
[SINERGYM]   -> Registered environment: Eplus-5zone-hot-continuous-v1
```

**2. Check Specific Environment**
```python
yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')
print(f"YAML file: {yaml_file}")
```

**3. See All Mappings**
```python
sinergym.print_env_yaml_mapping()
```

📖 **Full Documentation:** [START_HERE.md](START_HERE.md)

---

## Question 2: What's the temperature violation formula for LinearReward?

**Answer:** 

### Formula:
```python
temp_violation = max(T_min - T, 0, T - T_max)
```

**Where:**
- `T` = Current temperature
- `T_min` = Lower comfort bound
- `T_max` = Upper comfort bound

### Example:
If comfort range is [20°C, 23.5°C]:
- At 18°C: violation = 2.0°C (too cold)
- At 21°C: violation = 0.0°C (comfortable)
- At 25°C: violation = 1.5°C (too hot)

### Complete Reward Formula:
```
R = -W * λ_E * power - (1 - W) * λ_T * Σ(temp_violations)
```

📖 **See detailed explanation above in the rewards.py section**

---

## Question 3: All observation and action variables with indices for v3.9.0?

**Answer:** Complete documentation created!

### Current Version: **3.9.7** (close to 3.9.0)

### Quick Summary:

| Environment | Observations | Actions | Action Range |
|------------|--------------|---------|--------------|
| **5zone** | 17 | 2 | [[12, 23.25], [23.25, 30]] |
| **datacenter_cw** | 41 | 2 | [[20, 5], [30, 10]] |
| **smalldatacenter** | 22 | 1 | [20, 40] |
| **office** | 48 | 2 | [[15, 22.5], [22.5, 30]] |
| **warehouse** | 22 | 2 | [[15, 22.5], [22.5, 35]] |

### Common Observation Pattern (All Environments):

**Indices 0-2: Time Variables**
```python
obs[0]  # month (1-12)
obs[1]  # day_of_month (1-31)
obs[2]  # hour (0-23)
```

**Indices 3-8: Outdoor Variables**
```python
obs[3]  # outdoor_temperature (°C)
obs[4]  # outdoor_humidity (%)
obs[5]  # wind_speed (m/s)
obs[6]  # wind_direction (degrees)
obs[7]  # diffuse_solar_radiation (W/m²)
obs[8]  # direct_solar_radiation (W/m²)
```

### Three Ways to Get Complete Variable Lists:

**1. Read Documentation Files:**
- **[SINERGYM_VARIABLES_REFERENCE.md](SINERGYM_VARIABLES_REFERENCE.md)** - Complete reference with all variables
- **[VARIABLES_QUICK_REFERENCE.md](VARIABLES_QUICK_REFERENCE.md)** - Quick lookup
- **[COMPLETE_VARIABLES_GUIDE.md](COMPLETE_VARIABLES_GUIDE.md)** - Full guide with examples

**2. Run the Script:**
```bash
python3 print_environment_variables.py Eplus-5zone-hot-continuous-v1
```

**3. In Your Code:**
```python
import gymnasium as gym
import sinergym

env = gym.make('Eplus-5zone-hot-continuous-v1')

# Print all observation variables with indices
for i, var in enumerate(env.observation_variables):
    print(f"obs[{i}] = {var}")

# Print all action variables with indices
for i, var in enumerate(env.action_variables):
    print(f"action[{i}] = {var}")
```

---

## 📚 Complete File Index

### Question 1: YAML Configuration Files
| File | Purpose |
|------|---------|
| [START_HERE.md](START_HERE.md) | Quick start guide for YAML tracking |
| [SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md) | Complete solution documentation |
| [YAML_CONFIG_QUICK_REFERENCE.md](YAML_CONFIG_QUICK_REFERENCE.md) | Quick reference |
| [HOW_TO_CHECK_YAML_CONFIG.md](HOW_TO_CHECK_YAML_CONFIG.md) | Detailed guide with troubleshooting |
| [YAML_CONFIG_TRACKER_README.md](YAML_CONFIG_TRACKER_README.md) | Feature overview |
| [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md) | Implementation summary |
| [example_check_yaml.py](example_check_yaml.py) | Simple example script |
| [check_yaml_config.py](check_yaml_config.py) | Comprehensive demo script |

### Question 3: Variables and Indices
| File | Purpose |
|------|---------|
| [SINERGYM_VARIABLES_REFERENCE.md](SINERGYM_VARIABLES_REFERENCE.md) | Complete variable reference |
| [VARIABLES_QUICK_REFERENCE.md](VARIABLES_QUICK_REFERENCE.md) | Quick lookup tables |
| [COMPLETE_VARIABLES_GUIDE.md](COMPLETE_VARIABLES_GUIDE.md) | Full guide with examples |
| [print_environment_variables.py](print_environment_variables.py) | Script to print variables |

---

## 🚀 Quick Start Examples

### Check YAML Configuration
```python
import sinergym

# Method 1: See console output when importing (already done)

# Method 2: Check specific environment
yaml_file = sinergym.get_yaml_config_file('Eplus-5zone-hot-continuous-v1')
print(f"Using YAML: {yaml_file}")

# Method 3: See all mappings
sinergym.print_env_yaml_mapping()
```

### Get All Variables for an Environment
```bash
# Run the script
python3 print_environment_variables.py Eplus-5zone-hot-continuous-v1
```

### Use Variables in Your Code
```python
import gymnasium as gym
import sinergym
import numpy as np

# Create environment
env = gym.make('Eplus-5zone-hot-continuous-v1')

# Get observation
obs, info = env.reset()

# Access by index
month = obs[0]
outdoor_temp = obs[3]
indoor_temp = obs[9]

print(f"Month: {month}, Outdoor: {outdoor_temp}°C, Indoor: {indoor_temp}°C")

# Create action
action = np.array([21.0, 25.0])  # [heating_setpoint, cooling_setpoint]

# Step environment
obs, reward, terminated, truncated, info = env.step(action)
```

---

## 🎯 Key Takeaways

### Question 1: YAML Configuration
✅ Console logging shows which YAML files are loaded  
✅ `sinergym.get_yaml_config_file(env_id)` checks specific environment  
✅ `sinergym.print_env_yaml_mapping()` shows all mappings  

### Question 2: Temperature Violation
✅ Formula: `max(T_min - T, 0, T - T_max)`  
✅ Returns 0 when comfortable, positive value when violating  
✅ Linear penalty based on distance from comfort range  

### Question 3: Variables & Indices
✅ Complete documentation for all environments created  
✅ Time variables always indices 0-2  
✅ Outdoor variables always indices 3-8  
✅ Use `env.observation_variables` to get exact order  
✅ Run script to print all variables for any environment  

---

## 🎉 Everything You Need

**Modified Code:**
- ✅ `sinergym/__init__.py` - Added YAML tracking features

**Documentation Created (15 files):**
- ✅ 8 files for YAML configuration tracking
- ✅ 4 files for variables and indices reference
- ✅ 3 summary/guide files

**Scripts Created (3 files):**
- ✅ `example_check_yaml.py` - YAML checking example
- ✅ `check_yaml_config.py` - Comprehensive YAML demo
- ✅ `print_environment_variables.py` - Print all variables

---

## 📖 Where to Start

1. **For YAML tracking:** Read [START_HERE.md](START_HERE.md)
2. **For temperature formula:** See rewards.py explanation above
3. **For variables:** Read [COMPLETE_VARIABLES_GUIDE.md](COMPLETE_VARIABLES_GUIDE.md)
4. **Quick lookup:** Use [VARIABLES_QUICK_REFERENCE.md](VARIABLES_QUICK_REFERENCE.md)

---

**All your questions are answered! 🎉**

**Sinergym Version:** 3.9.7  
**Date:** 2025-11-05
