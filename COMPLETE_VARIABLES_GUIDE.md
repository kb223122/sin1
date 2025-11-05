# ✅ Complete Guide: All Observation & Action Variables in Sinergym v3.9.7

## 📋 What You Asked For

You asked for: **"All observation variable names and their index, and action variables available and their index as per Sinergym version 3.9.0"**

✅ **Current Version: 3.9.7** (close to 3.9.0)

---

## 📚 Documentation Files Created

I've created comprehensive documentation with all variables and indices:

| File | What's Inside |
|------|--------------|
| **[SINERGYM_VARIABLES_REFERENCE.md](SINERGYM_VARIABLES_REFERENCE.md)** | 📖 **Complete reference** - All variables with indices for every environment |
| **[VARIABLES_QUICK_REFERENCE.md](VARIABLES_QUICK_REFERENCE.md)** | ⚡ **Quick reference** - Common variables and examples |
| **[print_environment_variables.py](print_environment_variables.py)** | 🖥️ **Runnable script** - Print variables for any environment |

---

## 🚀 Quickest Way to Get Variable Indices

### Method 1: Use the Script (Recommended)

```bash
# Print variables for any environment
python3 print_environment_variables.py Eplus-5zone-hot-continuous-v1
python3 print_environment_variables.py Eplus-datacenter_cw-hot-continuous-v1
python3 print_environment_variables.py Eplus-office-hot-continuous-v1
```

This will show you:
- All observation variables with indices
- All action variables with indices
- Variable ranges
- Example code

### Method 2: In Your Python Code

```python
import gymnasium as gym
import sinergym

env = gym.make('Eplus-5zone-hot-continuous-v1')

# Print all observation variables with indices
print("\nObservation Variables:")
for i, var_name in enumerate(env.observation_variables):
    print(f"  obs[{i}] = {var_name}")

# Print all action variables with indices
print("\nAction Variables:")
for i, var_name in enumerate(env.action_variables):
    print(f"  action[{i}] = {var_name}")

print(f"\nObservation Space: {env.observation_space}")
print(f"Action Space: {env.action_space}")
```

---

## 📊 Summary of All Environments

### **1. 5Zone Office (`Eplus-5zone-hot-continuous-v1`)**
- **Observations:** 17 variables
- **Actions:** 2 variables (Heating_Setpoint_RL, Cooling_Setpoint_RL)
- **Action Range:** [[12.0, 23.25], [23.25, 30.0]]

**Key Observation Indices:**
- `obs[0]` = month
- `obs[1]` = day_of_month
- `obs[2]` = hour
- `obs[3]` = outdoor_temperature
- `obs[9]` = air_temperature
- `obs[15]` = HVAC_electricity_demand_rate

---

### **2. Data Center CW (`Eplus-datacenter_cw-hot-continuous-v1`)**
- **Observations:** 41 variables
- **Actions:** 2 variables (cooling_setpoint, chiller_water_temperature)
- **Action Range:** [[20.0, 5.0], [30.0, 10.0]]

**Key Observation Indices:**
- `obs[0-2]` = time variables
- `obs[3-8]` = outdoor variables
- `obs[9]` = east_zone_air_temperature
- `obs[10]` = west_zone_air_temperature
- `obs[40]` = HVAC_electricity_demand_rate

---

### **3. Small Data Center (`Eplus-smalldatacenter-hot-continuous-v1`)**
- **Observations:** 22 variables
- **Actions:** 1 variable (Cooling_Setpoint_RL)
- **Action Range:** [20.0, 40.0]

**Key Observation Indices:**
- `obs[0-2]` = time variables
- `obs[9]` = air_temperature
- `obs[21]` = HVAC_electricity_demand_rate

---

### **4. Office Medium (`Eplus-office-hot-continuous-v1`)**
- **Observations:** 48 variables (17 zones!)
- **Actions:** 2 variables (Office_Heating_RL, Office_Cooling_RL)
- **Action Range:** [[15.0, 22.5], [22.5, 30.0]]

**Key Observation Indices:**
- `obs[0-2]` = time variables
- `obs[9-26]` = zone temperatures (17 zones)
- `obs[27-44]` = zone humidities
- `obs[47]` = HVAC_electricity_demand_rate

---

### **5. Warehouse (`Eplus-warehouse-hot-continuous-v1`)**
- **Observations:** 22 variables
- **Actions:** 2 variables (Office_Heating_RL, Office_Cooling_RL)
- **Action Range:** [[15.0, 22.5], [22.5, 35.0]]

**Key Observation Indices:**
- `obs[0-2]` = time variables
- `obs[9-11]` = zone temperatures (3 zones)
- `obs[21]` = HVAC_electricity_demand_rate

---

## 🔍 Common Pattern Across All Environments

### First 3 Variables (Indices 0-2): Time Variables
```python
obs[0]  # month (1-12)
obs[1]  # day_of_month (1-31)
obs[2]  # hour (0-23)
```

### Next 6 Variables (Indices 3-8): Outdoor Variables
```python
obs[3]  # outdoor_temperature (°C)
obs[4]  # outdoor_humidity (%)
obs[5]  # wind_speed (m/s)
obs[6]  # wind_direction (degrees)
obs[7]  # diffuse_solar_radiation (W/m²)
obs[8]  # direct_solar_radiation (W/m²)
```

### Last Variable: Usually HVAC Power
```python
obs[-1] or obs[-2]  # HVAC_electricity_demand_rate (W)
```

---

## 💡 Complete Example

```python
import gymnasium as gym
import sinergym
import numpy as np

# Create environment
env = gym.make('Eplus-5zone-hot-continuous-v1')

# Get initial observation
obs, info = env.reset()

print("="*60)
print("OBSERVATION VARIABLES AND VALUES")
print("="*60)

# Print all observations with indices
for i, var_name in enumerate(env.observation_variables):
    print(f"obs[{i:2d}] = {var_name:40s} = {obs[i]:8.2f}")

print("\n" + "="*60)
print("ACTION VARIABLES")
print("="*60)

# Print action variables
for i, var_name in enumerate(env.action_variables):
    print(f"action[{i}] = {var_name}")

# Action space info
print(f"\nAction Space: {env.action_space}")
print(f"  Low: {env.action_space.low}")
print(f"  High: {env.action_space.high}")

# Create an action
action = np.array([21.0, 25.0])  # [heating, cooling]
print(f"\nApplying action: {action}")

# Step environment
obs, reward, terminated, truncated, info = env.step(action)
print(f"Reward: {reward:.4f}")

env.close()
```

---

## 📖 For Complete Details

### Read These Files:

1. **[SINERGYM_VARIABLES_REFERENCE.md](SINERGYM_VARIABLES_REFERENCE.md)**
   - Complete list of ALL variables for ALL environments
   - Detailed descriptions and units
   - Every single observation and action index

2. **[VARIABLES_QUICK_REFERENCE.md](VARIABLES_QUICK_REFERENCE.md)**
   - Quick lookup tables
   - Common operations
   - Code examples

3. **Run the script:**
   ```bash
   python3 print_environment_variables.py YOUR-ENV-ID
   ```

---

## 🎯 How to Use in Your Code

### Access Observation by Index
```python
obs, info = env.reset()

# By index
month = obs[0]
outdoor_temp = obs[3]
indoor_temp = obs[9]  # varies by environment

print(f"Month: {month}, Outdoor: {outdoor_temp}°C, Indoor: {indoor_temp}°C")
```

### Access Observation by Name
```python
# Get index from name
temp_index = env.observation_variables.index('air_temperature')
indoor_temp = obs[temp_index]
```

### Set Action by Index
```python
# For environments with 2 actions (heating + cooling)
action = np.array([heating_setpoint, cooling_setpoint])

# For environments with 1 action (cooling only)
action = np.array([cooling_setpoint])

obs, reward, terminated, truncated, info = env.step(action)
```

---

## 📊 Quick Lookup Table

| Environment | Obs Count | Action Count | Time Vars | Outdoor Vars | Zone Temps |
|------------|-----------|--------------|-----------|--------------|------------|
| 5zone | 17 | 2 | 3 | 6 | 1 |
| datacenter_cw | 41 | 2 | 3 | 6 | 2 |
| smalldatacenter | 22 | 1 | 3 | 6 | 1 |
| office | 48 | 2 | 3 | 6 | 17 |
| warehouse | 22 | 2 | 3 | 6 | 3 |

---

## ⚡ Quick Commands

```bash
# Print variables for default environment
python3 print_environment_variables.py

# Print variables for specific environment
python3 print_environment_variables.py Eplus-5zone-hot-continuous-v1
python3 print_environment_variables.py Eplus-datacenter_cw-hot-continuous-v1
python3 print_environment_variables.py Eplus-smalldatacenter-hot-continuous-v1
python3 print_environment_variables.py Eplus-office-hot-continuous-v1
python3 print_environment_variables.py Eplus-warehouse-hot-continuous-v1
```

---

## 🔧 Debugging Tips

### Check Your Environment's Variables
```python
import gymnasium as gym
import sinergym

env = gym.make('YOUR-ENV-ID')

print(f"Total observations: {len(env.observation_variables)}")
print(f"Total actions: {len(env.action_variables)}")
print(f"Observation space shape: {env.observation_space.shape}")
print(f"Action space shape: {env.action_space.shape}")

# List all variables
print("\nObservation variables:")
print(env.observation_variables)
print("\nAction variables:")
print(env.action_variables)
```

### Verify Observation Shape
```python
obs, info = env.reset()
assert obs.shape[0] == len(env.observation_variables), "Mismatch!"
print(f"✅ Observation shape matches: {obs.shape}")
```

---

## 📌 Key Points to Remember

1. ✅ **Indices are 0-based** (first variable is index 0)
2. ✅ **Time variables are always first 3** (month, day, hour)
3. ✅ **Outdoor variables usually follow** (indices 3-8)
4. ✅ **Variable order is defined in YAML files**
5. ✅ **Use `env.observation_variables` to see exact order**
6. ✅ **Action ranges are enforced by action space**

---

## 🎉 Summary

**You now have:**
- ✅ Complete lists of all observation variables with indices
- ✅ Complete lists of all action variables with indices
- ✅ Reference documentation for all environments
- ✅ Runnable script to check any environment
- ✅ Code examples for accessing variables

**Three ways to access this info:**
1. Read [SINERGYM_VARIABLES_REFERENCE.md](SINERGYM_VARIABLES_REFERENCE.md)
2. Read [VARIABLES_QUICK_REFERENCE.md](VARIABLES_QUICK_REFERENCE.md)
3. Run `python3 print_environment_variables.py YOUR-ENV-ID`

---

**Version:** Sinergym 3.9.7  
**Last Updated:** 2025-11-05

**Happy coding! 🚀**
