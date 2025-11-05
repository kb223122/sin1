# 📊 Sinergym Variables Quick Reference (v3.9.7)

## 🚀 Quick Start

```python
import gymnasium as gym
import sinergym

env = gym.make('Eplus-5zone-hot-continuous-v1')
obs, info = env.reset()

# Observation: numpy array with shape (18,)
# obs[0] = month, obs[1] = day, obs[2] = hour
# obs[3] = outdoor_temp, obs[9] = indoor_temp, etc.

# Action: numpy array with shape (2,)
action = np.array([21.0, 25.0])  # [heating_setpoint, cooling_setpoint]
obs, reward, terminated, truncated, info = env.step(action)
```

---

## 📋 Environment Summary

| Environment ID | Obs Dims | Action Dims | Action Range |
|----------------|----------|-------------|--------------|
| `Eplus-5zone-hot-continuous-v1` | 17 | 2 | [[12, 23.25], [23.25, 30]] |
| `Eplus-datacenter_cw-hot-continuous-v1` | 41 | 2 | [[20, 5], [30, 10]] |
| `Eplus-smalldatacenter-hot-continuous-v1` | 22 | 1 | [[20], [40]] |
| `Eplus-office-hot-continuous-v1` | 48 | 2 | [[15, 22.5], [22.5, 30]] |
| `Eplus-warehouse-hot-continuous-v1` | 22 | 2 | [[15, 22.5], [22.5, 35]] |

---

## 🔍 Common Observation Variables (All Environments)

### Time Variables (Indices 0-2)
```python
obs[0]  # month (1-12)
obs[1]  # day_of_month (1-31)
obs[2]  # hour (0-23)
```

### Outdoor Variables (Indices 3-8)
```python
obs[3]  # outdoor_temperature (°C)
obs[4]  # outdoor_humidity (%)
obs[5]  # wind_speed (m/s)
obs[6]  # wind_direction (degrees)
obs[7]  # diffuse_solar_radiation (W/m²)
obs[8]  # direct_solar_radiation (W/m²)
```

---

## 🏢 5Zone Environment (`Eplus-5zone-hot-continuous-v1`)

### Key Observations
```python
obs[0]   # month
obs[1]   # day_of_month
obs[2]   # hour
obs[3]   # outdoor_temperature
obs[9]   # air_temperature (SPACE5-1)
obs[10]  # air_humidity
obs[11]  # people_occupant
obs[12]  # htg_setpoint
obs[13]  # clg_setpoint
obs[15]  # HVAC_electricity_demand_rate
obs[16]  # total_electricity_HVAC (meter)
```

### Actions
```python
action[0]  # Heating_Setpoint_RL (12.0 - 23.25°C)
action[1]  # Cooling_Setpoint_RL (23.25 - 30.0°C)
```

---

## 🖥️ Data Center CW Environment (`Eplus-datacenter_cw-hot-continuous-v1`)

### Key Observations
```python
obs[0]   # month
obs[1]   # day_of_month
obs[2]   # hour
obs[3]   # outdoor_temperature
obs[9]   # east_zone_air_temperature
obs[10]  # west_zone_air_temperature
obs[15]  # east_zone_clg_setpoint
obs[22]  # chws_return_temperature
obs[23]  # chws_supply_temperature
obs[33]  # chiller_electricity_rate
obs[40]  # HVAC_electricity_demand_rate
```

### Actions
```python
action[0]  # cooling_setpoint (20.0 - 30.0°C)
action[1]  # chiller_water_temperature (5.0 - 10.0°C)
```

---

## 💻 Small Data Center Environment (`Eplus-smalldatacenter-hot-continuous-v1`)

### Key Observations
```python
obs[0]   # month
obs[1]   # day_of_month
obs[2]   # hour
obs[3]   # outdoor_temperature
obs[9]   # air_temperature (Main Zone)
obs[12]  # clg_setpoint
obs[16]  # cooling_coil_total_cooling_rate
obs[19]  # cooling_coil_electricity_rate
obs[20]  # fan_electricity_rate
obs[21]  # HVAC_electricity_demand_rate
```

### Actions
```python
action[0]  # Cooling_Setpoint_RL (20.0 - 40.0°C)
```

---

## 🏢 Office Environment (`Eplus-office-hot-continuous-v1`)

### Key Observations (17 zones!)
```python
obs[0]   # month
obs[1]   # day_of_month
obs[2]   # hour
obs[3]   # outdoor_temperature
obs[9]   # core_bottom_air_temperature
obs[10]  # core_mid_air_temperature
obs[11]  # core_top_air_temperature
# ... 14 more zone temperatures (indices 12-26)
# ... 17 humidity values (indices 27-43)
obs[44]  # core_bottom_htg_setpoint
obs[45]  # core_bottom_clg_setpoint
obs[46]  # HVAC_electricity_demand_rate
```

### Actions
```python
action[0]  # Office_Heating_RL (15.0 - 22.5°C)
action[1]  # Office_Cooling_RL (22.5 - 30.0°C)
```

---

## 🏭 Warehouse Environment (`Eplus-warehouse-hot-continuous-v1`)

### Key Observations
```python
obs[0]   # month
obs[1]   # day_of_month
obs[2]   # hour
obs[3]   # outdoor_temperature
obs[9]   # zone1_office_air_temperature
obs[10]  # zone2_fine_storage_air_temperature
obs[11]  # zone3_bulk_storage_air_temperature
obs[15]  # zone1_office_people_occupant
obs[21]  # HVAC_electricity_demand_rate
```

### Actions
```python
action[0]  # Office_Heating_RL (15.0 - 22.5°C)
action[1]  # Office_Cooling_RL (22.5 - 35.0°C)
```

---

## 🎯 How to Find Variable Indices

### Method 1: Print Observation Variables
```python
import gymnasium as gym
import sinergym

env = gym.make('Eplus-5zone-hot-continuous-v1')
print("Observation variables:", env.observation_variables)
print("Total observations:", len(env.observation_variables))

# Output:
# ['month', 'day_of_month', 'hour', 'outdoor_temperature', ...]
```

### Method 2: Check Observation Space
```python
print("Observation space:", env.observation_space)
print("Observation shape:", env.observation_space.shape)

# Output:
# Box(shape=(17,), ...)
```

### Method 3: Inspect During Execution
```python
obs, info = env.reset()
print("Observation shape:", obs.shape)
print("First 5 values:", obs[:5])

for i, var_name in enumerate(env.observation_variables):
    print(f"  obs[{i}] = {var_name} = {obs[i]:.2f}")
```

---

## 🔧 Common Operations

### Access Observation by Index
```python
obs, info = env.reset()

month = obs[0]
outdoor_temp = obs[3]
indoor_temp = obs[9]  # varies by environment
hvac_power = obs[-1]  # usually last or second to last
```

### Set Action by Index
```python
# 2-action environment (heating + cooling)
action = np.array([heating_setpoint, cooling_setpoint])

# 1-action environment (cooling only)
action = np.array([cooling_setpoint])

obs, reward, terminated, truncated, info = env.step(action)
```

### Get Variable Name from Index
```python
index = 9
var_name = env.observation_variables[index]
print(f"Variable at index {index}: {var_name}")
```

### Get Index from Variable Name
```python
var_name = 'air_temperature'
index = env.observation_variables.index(var_name)
print(f"Index of '{var_name}': {index}")
```

---

## ⚠️ Important Notes

1. **Indices are 0-based**: First variable is index 0
2. **Time variables always first**: month, day_of_month, hour (indices 0-2)
3. **Order matters**: Observations are numpy arrays, not dictionaries
4. **Variable names are normalized**: Lowercase, underscores replace spaces
5. **Action ranges are enforced**: Stay within bounds defined in action space

---

## 📖 For Complete Details

See **[SINERGYM_VARIABLES_REFERENCE.md](SINERGYM_VARIABLES_REFERENCE.md)** for:
- Complete variable lists for all environments
- Detailed descriptions and units
- All observation and action indices
- Additional environment variants

---

## 🔍 Check Your Environment

```python
import gymnasium as gym
import sinergym

# Replace with your environment
env_id = 'Eplus-5zone-hot-continuous-v1'
env = gym.make(env_id)

print(f"\n{'='*60}")
print(f"Environment: {env_id}")
print(f"{'='*60}")
print(f"Observation Space: {env.observation_space}")
print(f"Action Space: {env.action_space}")
print(f"\nObservation Variables ({len(env.observation_variables)}):")
for i, var in enumerate(env.observation_variables):
    print(f"  [{i:2d}] {var}")
print(f"\nAction Variables ({len(env.action_variables)}):")
for i, var in enumerate(env.action_variables):
    print(f"  [{i:2d}] {var}")
print(f"{'='*60}\n")

env.close()
```

---

**Version:** Sinergym 3.9.7  
**Last Updated:** 2025-11-05
