# 📊 Sinergym Variables Reference (v3.9.7)

## Complete Observation and Action Variables with Indices

This document lists **ALL observation variables and their indices**, and **ALL action variables and their indices** for each Sinergym environment.

---

## 🔍 How Observation Indices Work

Observations are returned as a **numpy array**. The order is:
1. **Time variables** (month, day_of_month, hour)
2. **Output:Variables** (in the order defined in YAML)
3. **Output:Meters** (in the order defined in YAML)

---

## 📝 Environments Overview

| Environment | Building Type | Action Dims | Observation Dims |
|------------|---------------|-------------|------------------|
| **5zone** | Office Building | 2 | ~18 |
| **datacenter_cw** | Data Center (Chilled Water) | 2 | ~42 |
| **smalldatacenter** | Small Data Center | 1 | ~21 |
| **office** | Medium Office | 2 | ~45 |
| **warehouse** | Warehouse | 2 | ~18 |

---

## 🏢 1. 5Zone Office Building (`5ZoneAutoDXVAV`)

**Environments:**
- `Eplus-5zone-hot-continuous-v1`
- `Eplus-5zone-mixed-continuous-v1`
- `Eplus-5zone-cool-continuous-v1`

### 📥 Observation Variables (18 total)

| Index | Variable Name | Description | Unit |
|-------|--------------|-------------|------|
| **0** | `month` | Month of year | 1-12 |
| **1** | `day_of_month` | Day of month | 1-31 |
| **2** | `hour` | Hour of day | 0-23 |
| **3** | `outdoor_temperature` | Site outdoor air drybulb temperature | °C |
| **4** | `outdoor_humidity` | Site outdoor air relative humidity | % |
| **5** | `wind_speed` | Site wind speed | m/s |
| **6** | `wind_direction` | Site wind direction | degrees |
| **7** | `diffuse_solar_radiation` | Site diffuse solar radiation rate per area | W/m² |
| **8** | `direct_solar_radiation` | Site direct solar radiation rate per area | W/m² |
| **9** | `air_temperature` | Zone air temperature (SPACE5-1) | °C |
| **10** | `air_humidity` | Zone air relative humidity (SPACE5-1) | % |
| **11** | `people_occupant` | Zone people occupant count (SPACE5-1) | count |
| **12** | `htg_setpoint` | Zone thermostat heating setpoint (SPACE5-1) | °C |
| **13** | `clg_setpoint` | Zone thermostat cooling setpoint (SPACE5-1) | °C |
| **14** | `co2_emission` | Environmental impact total CO2 emissions | kg |
| **15** | `HVAC_electricity_demand_rate` | Facility total HVAC electricity demand rate | W |
| **16** | `total_electricity_HVAC` | Total electricity HVAC (meter) | J |

### 📤 Action Variables (2 total)

| Index | Variable Name | Description | Range | Unit |
|-------|--------------|-------------|-------|------|
| **0** | `Heating_Setpoint_RL` | Heating setpoint control | [12.0, 23.25] | °C |
| **1** | `Cooling_Setpoint_RL` | Cooling setpoint control | [23.25, 30.0] | °C |

**Action Space:** `Box(low=[12.0, 23.25], high=[23.25, 30.0])`

---

## 🖥️ 2. Data Center with Chilled Water (`2ZoneDataCenterHVAC_wEconomizer_CW`)

**Environments:**
- `Eplus-datacenter_cw-chicago-continuous-v1`
- `Eplus-datacenter_cw-hot-continuous-v1`
- `Eplus-datacenter_cw-mixed-continuous-v1`
- `Eplus-datacenter_cw-cool-continuous-v1`

### 📥 Observation Variables (42 total)

| Index | Variable Name | Description | Unit |
|-------|--------------|-------------|------|
| **0** | `month` | Month of year | 1-12 |
| **1** | `day_of_month` | Day of month | 1-31 |
| **2** | `hour` | Hour of day | 0-23 |
| **3** | `outdoor_temperature` | Site outdoor air drybulb temperature | °C |
| **4** | `outdoor_humidity` | Site outdoor air relative humidity | % |
| **5** | `wind_speed` | Site wind speed | m/s |
| **6** | `wind_direction` | Site wind direction | degrees |
| **7** | `diffuse_solar_radiation` | Site diffuse solar radiation rate per area | W/m² |
| **8** | `direct_solar_radiation` | Site direct solar radiation rate per area | W/m² |
| **9** | `east_zone_air_temperature` | Zone air temperature (East Zone) | °C |
| **10** | `west_zone_air_temperature` | Zone air temperature (West Zone) | °C |
| **11** | `east_zone_mean_radiant_temperature` | Zone mean radiant temperature (East Zone) | °C |
| **12** | `west_zone_mean_radiant_temperature` | Zone mean radiant temperature (West Zone) | °C |
| **13** | `east_zone_air_humidity` | Zone air relative humidity (East Zone) | % |
| **14** | `west_zone_air_humidity` | Zone air relative humidity (West Zone) | % |
| **15** | `east_zone_clg_setpoint` | Zone thermostat cooling setpoint (East Zone) | °C |
| **16** | `east_return_temperature` | System node temperature (East Zone Return) | °C |
| **17** | `east_supply_temperature` | System node temperature (East Air Loop Outlet) | °C |
| **18** | `west_return_temperature` | System node temperature (West Zone Return) | °C |
| **19** | `west_supply_temperature` | System node temperature (West Air Loop Outlet) | °C |
| **20** | `east_mass_flow_rate` | System node mass flow rate (East Zone Inlet) | kg/s |
| **21** | `west_mass_flow_rate` | System node mass flow rate (West Zone Inlet) | kg/s |
| **22** | `chws_return_temperature` | Chiller evaporator inlet temperature | °C |
| **23** | `chws_supply_temperature` | Chiller evaporator outlet temperature | °C |
| **24** | `east_cw_total_cooling_rate` | Cooling coil total cooling rate (East) | W |
| **25** | `west_cw_total_cooling_rate` | Cooling coil total cooling rate (West) | W |
| **26** | `east_cw_sensible_cooling_rate` | Cooling coil sensible cooling rate (East) | W |
| **27** | `west_cw_sensible_cooling_rate` | Cooling coil sensible cooling rate (West) | W |
| **28** | `cpu_loading_fraction` | Performance curve input (CPU loading) | fraction |
| **29** | `east_dec_electricity_rate` | Evaporative cooler electricity rate (East DEC) | W |
| **30** | `east_iec_electricity_rate` | Evaporative cooler electricity rate (East IEC) | W |
| **31** | `west_dec_electricity_rate` | Evaporative cooler electricity rate (West DEC) | W |
| **32** | `west_iec_electricity_rate` | Evaporative cooler electricity rate (West IEC) | W |
| **33** | `chiller_electricity_rate` | Chiller electricity rate | W |
| **34** | `cw_pump_electricity_rate` | Pump electricity rate (CW Circ Pump) | W |
| **35** | `condenser_pump_electricity_rate` | Pump electricity rate (Cond Circ Pump) | W |
| **36** | `east_fan_electricity_rate` | Fan electricity rate (East Zone Supply Fan) | W |
| **37** | `west_fan_electricity_rate` | Fan electricity rate (West Zone Supply Fan) | W |
| **38** | `cooling_tower_fan_electricity_rate` | Cooling tower fan electricity rate | W |
| **39** | `cooling_tower_basin_heater_electricity_rate` | Cooling tower basin heater electricity rate | W |
| **40** | `HVAC_electricity_demand_rate` | Facility total HVAC electricity demand rate | W |

### 📤 Action Variables (2 total)

| Index | Variable Name | Description | Range | Unit |
|-------|--------------|-------------|-------|------|
| **0** | `cooling_setpoint` | Cooling setpoint control | [20.0, 30.0] | °C |
| **1** | `chiller_water_temperature` | Chiller water temperature control | [5.0, 10.0] | °C |

**Action Space:** `Box(low=[20.0, 5.0], high=[30.0, 10.0])`

---

## 💻 3. Small Data Center (`1ZoneDataCenterCRAC_wApproachTemp`)

**Environments:**
- `Eplus-smalldatacenter-aurora-continuous-v1`
- `Eplus-smalldatacenter-hot-continuous-v1`
- `Eplus-smalldatacenter-mixed-continuous-v1`
- `Eplus-smalldatacenter-cool-continuous-v1`

### 📥 Observation Variables (21 total)

| Index | Variable Name | Description | Unit |
|-------|--------------|-------------|------|
| **0** | `month` | Month of year | 1-12 |
| **1** | `day_of_month` | Day of month | 1-31 |
| **2** | `hour` | Hour of day | 0-23 |
| **3** | `outdoor_temperature` | Site outdoor air drybulb temperature | °C |
| **4** | `outdoor_humidity` | Site outdoor air relative humidity | % |
| **5** | `wind_speed` | Site wind speed | m/s |
| **6** | `wind_direction` | Site wind direction | degrees |
| **7** | `diffuse_solar_radiation` | Site diffuse solar radiation rate per area | W/m² |
| **8** | `direct_solar_radiation` | Site direct solar radiation rate per area | W/m² |
| **9** | `air_temperature` | Zone air temperature (Main Zone) | °C |
| **10** | `mean_radiant_temperature` | Zone mean radiant temperature (Main Zone) | °C |
| **11** | `air_humidity` | Zone air relative humidity (Main Zone) | % |
| **12** | `clg_setpoint` | Zone thermostat cooling setpoint (Main Zone) | °C |
| **13** | `supply_air_temperature` | System node temperature (Supply Outlet) | °C |
| **14** | `return_air_temperature` | System node temperature (Main Zone Outlet) | °C |
| **15** | `supply_mass_flow_rate` | System node mass flow rate (Supply Outlet) | kg/s |
| **16** | `cooling_coil_total_cooling_rate` | Cooling coil total cooling rate | W |
| **17** | `cooling_coil_sensible_cooling_rate` | Cooling coil sensible cooling rate | W |
| **18** | `cpu_loading_fraction` | Performance curve input (CPU loading) | fraction |
| **19** | `cooling_coil_electricity_rate` | Cooling coil electricity rate | W |
| **20** | `fan_electricity_rate` | Fan electricity rate | W |
| **21** | `HVAC_electricity_demand_rate` | Facility total HVAC electricity demand rate | W |

### 📤 Action Variables (1 total)

| Index | Variable Name | Description | Range | Unit |
|-------|--------------|-------------|-------|------|
| **0** | `Cooling_Setpoint_RL` | Cooling setpoint control | [20.0, 40.0] | °C |

**Action Space:** `Box(low=[20.0], high=[40.0])`

---

## 🏢 4. Medium Office Building (`ASHRAE901_OfficeMedium_STD2019_Denver`)

**Environments:**
- `Eplus-office-hot-continuous-v1`
- `Eplus-office-mixed-continuous-v1`
- `Eplus-office-cool-continuous-v1`

### 📥 Observation Variables (45 total)

| Index | Variable Name | Description | Unit |
|-------|--------------|-------------|------|
| **0** | `month` | Month of year | 1-12 |
| **1** | `day_of_month` | Day of month | 1-31 |
| **2** | `hour` | Hour of day | 0-23 |
| **3** | `outdoor_temperature` | Site outdoor air drybulb temperature | °C |
| **4** | `outdoor_humidity` | Site outdoor air relative humidity | % |
| **5** | `wind_speed` | Site wind speed | m/s |
| **6** | `wind_direction` | Site wind direction | degrees |
| **7** | `diffuse_solar_radiation` | Site diffuse solar radiation rate per area | W/m² |
| **8** | `direct_solar_radiation` | Site direct solar radiation rate per area | W/m² |
| **9** | `core_bottom_air_temperature` | Zone air temperature (Core_bottom) | °C |
| **10** | `core_mid_air_temperature` | Zone air temperature (Core_mid) | °C |
| **11** | `core_top_air_temperature` | Zone air temperature (Core_top) | °C |
| **12** | `firstfloor_plenum_air_temperature` | Zone air temperature (FirstFloor_Plenum) | °C |
| **13** | `midfloor_plenum_air_temperature` | Zone air temperature (MidFloor_Plenum) | °C |
| **14** | `topfloor_plenum_air_temperature` | Zone air temperature (TopFloor_Plenum) | °C |
| **15** | `perimeter_bot_zn_1_air_temperature` | Zone air temperature (Perimeter_bot_ZN_1) | °C |
| **16** | `perimeter_bot_zn_2_air_temperature` | Zone air temperature (Perimeter_bot_ZN_2) | °C |
| **17** | `perimeter_bot_zn_3_air_temperature` | Zone air temperature (Perimeter_bot_ZN_3) | °C |
| **18** | `perimeter_bot_zn_4_air_temperature` | Zone air temperature (Perimeter_bot_ZN_4) | °C |
| **19** | `perimeter_mid_zn_1_air_temperature` | Zone air temperature (Perimeter_mid_ZN_1) | °C |
| **20** | `perimeter_mid_zn_2_air_temperature` | Zone air temperature (Perimeter_mid_ZN_2) | °C |
| **21** | `perimeter_mid_zn_3_air_temperature` | Zone air temperature (Perimeter_mid_ZN_3) | °C |
| **22** | `perimeter_mid_zn_4_air_temperature` | Zone air temperature (Perimeter_mid_ZN_4) | °C |
| **23** | `perimeter_top_zn_1_air_temperature` | Zone air temperature (Perimeter_top_ZN_1) | °C |
| **24** | `perimeter_top_zn_2_air_temperature` | Zone air temperature (Perimeter_top_ZN_2) | °C |
| **25** | `perimeter_top_zn_3_air_temperature` | Zone air temperature (Perimeter_top_ZN_3) | °C |
| **26** | `perimeter_top_zn_4_air_temperature` | Zone air temperature (Perimeter_top_ZN_4) | °C |
| **27** | `core_bottom_air_humidity` | Zone air relative humidity (Core_bottom) | % |
| **28** | `core_mid_air_humidity` | Zone air relative humidity (Core_mid) | % |
| **29** | `core_top_air_humidity` | Zone air relative humidity (Core_top) | % |
| **30** | `firstfloor_plenum_air_humidity` | Zone air relative humidity (FirstFloor_Plenum) | % |
| **31** | `midfloor_plenum_air_humidity` | Zone air relative humidity (MidFloor_Plenum) | % |
| **32** | `topfloor_plenum_air_humidity` | Zone air relative humidity (TopFloor_Plenum) | % |
| **33** | `perimeter_bot_zn_1_air_humidity` | Zone air relative humidity (Perimeter_bot_ZN_1) | % |
| **34** | `perimeter_bot_zn_2_air_humidity` | Zone air relative humidity (Perimeter_bot_ZN_2) | % |
| **35** | `perimeter_bot_zn_3_air_humidity` | Zone air relative humidity (Perimeter_bot_ZN_3) | % |
| **36** | `perimeter_bot_zn_4_air_humidity` | Zone air relative humidity (Perimeter_bot_ZN_4) | % |
| **37** | `perimeter_mid_zn_1_air_humidity` | Zone air relative humidity (Perimeter_mid_ZN_1) | % |
| **38** | `perimeter_mid_zn_2_air_humidity` | Zone air relative humidity (Perimeter_mid_ZN_2) | % |
| **39** | `perimeter_mid_zn_3_air_humidity` | Zone air relative humidity (Perimeter_mid_ZN_3) | % |
| **40** | `perimeter_mid_zn_4_air_humidity` | Zone air relative humidity (Perimeter_mid_ZN_4) | % |
| **41** | `perimeter_top_zn_1_air_humidity` | Zone air relative humidity (Perimeter_top_ZN_1) | % |
| **42** | `perimeter_top_zn_2_air_humidity` | Zone air relative humidity (Perimeter_top_ZN_2) | % |
| **43** | `perimeter_top_zn_3_air_humidity` | Zone air relative humidity (Perimeter_top_ZN_3) | % |
| **44** | `perimeter_top_zn_4_air_humidity` | Zone air relative humidity (Perimeter_top_ZN_4) | % |
| **45** | `core_bottom_htg_setpoint` | Zone thermostat heating setpoint (Core_bottom) | °C |
| **46** | `core_bottom_clg_setpoint` | Zone thermostat cooling setpoint (Core_bottom) | °C |
| **47** | `HVAC_electricity_demand_rate` | Facility total HVAC electricity demand rate | W |

### 📤 Action Variables (2 total)

| Index | Variable Name | Description | Range | Unit |
|-------|--------------|-------------|-------|------|
| **0** | `Office_Heating_RL` | Office heating setpoint control | [15.0, 22.5] | °C |
| **1** | `Office_Cooling_RL` | Office cooling setpoint control | [22.5, 30.0] | °C |

**Action Space:** `Box(low=[15.0, 22.5], high=[22.5, 30.0])`

---

## 🏭 5. Warehouse (`ASHRAE901_Warehouse_STD2019_Denver`)

**Environments:**
- `Eplus-warehouse-hot-continuous-v1`
- `Eplus-warehouse-mixed-continuous-v1`
- `Eplus-warehouse-cool-continuous-v1`

### 📥 Observation Variables (18 total)

| Index | Variable Name | Description | Unit |
|-------|--------------|-------------|------|
| **0** | `month` | Month of year | 1-12 |
| **1** | `day_of_month` | Day of month | 1-31 |
| **2** | `hour` | Hour of day | 0-23 |
| **3** | `outdoor_temperature` | Site outdoor air drybulb temperature | °C |
| **4** | `outdoor_humidity` | Site outdoor air relative humidity | % |
| **5** | `wind_speed` | Site wind speed | m/s |
| **6** | `wind_direction` | Site wind direction | degrees |
| **7** | `diffuse_solar_radiation` | Site diffuse solar radiation rate per area | W/m² |
| **8** | `direct_solar_radiation` | Site direct solar radiation rate per area | W/m² |
| **9** | `zone1_office_air_temperature` | Zone air temperature (Zone1 Office) | °C |
| **10** | `zone2_fine_storage_air_temperature` | Zone air temperature (Zone2 Fine Storage) | °C |
| **11** | `zone3_bulk_storage_air_temperature` | Zone air temperature (Zone3 Bulk Storage) | °C |
| **12** | `zone1_office_air_humidity` | Zone air relative humidity (Zone1 Office) | % |
| **13** | `zone2_fine_storage_air_humidity` | Zone air relative humidity (Zone2 Fine Storage) | % |
| **14** | `zone3_bulk_storage_air_humidity` | Zone air relative humidity (Zone3 Bulk Storage) | % |
| **15** | `zone1_office_people_occupant` | Zone people occupant count (Zone1 Office) | count |
| **16** | `zone1_office_htg_setpoint` | Zone thermostat heating setpoint (Zone1 Office) | °C |
| **17** | `zone2_fine_storage_htg_setpoint` | Zone thermostat heating setpoint (Zone2 Fine Storage) | °C |
| **18** | `zone3_bulk_storage_htg_setpoint` | Zone thermostat heating setpoint (Zone3 Bulk Storage) | °C |
| **19** | `zone1_office_clg_setpoint` | Zone thermostat cooling setpoint (Zone1 Office) | °C |
| **20** | `zone2_fine_storage_clg_setpoint` | Zone thermostat cooling setpoint (Zone2 Fine Storage) | °C |
| **21** | `HVAC_electricity_demand_rate` | Facility total HVAC electricity demand rate | W |

### 📤 Action Variables (2 total)

| Index | Variable Name | Description | Range | Unit |
|-------|--------------|-------------|-------|------|
| **0** | `Office_Heating_RL` | Office heating setpoint control | [15.0, 22.5] | °C |
| **1** | `Office_Cooling_RL` | Office cooling setpoint control | [22.5, 35.0] | °C |

**Action Space:** `Box(low=[15.0, 22.5], high=[22.5, 35.0])`

---

## 🎮 How to Access Variables in Code

### Getting Observation Variable Names
```python
import gymnasium as gym
import sinergym

env = gym.make('Eplus-5zone-hot-continuous-v1')
print("Observation variables:", env.observation_variables)
print("Observation space shape:", env.observation_space.shape)
```

### Getting Action Variable Names
```python
print("Action variables:", env.action_variables)
print("Action space:", env.action_space)
```

### Accessing Specific Observation by Index
```python
obs, info = env.reset()

# Access specific observations by index
month = obs[0]
day = obs[1]
hour = obs[2]
outdoor_temp = obs[3]
air_temp = obs[9]  # For 5zone environment

print(f"Month: {month}, Day: {day}, Hour: {hour}")
print(f"Outdoor Temperature: {outdoor_temp}°C")
print(f"Indoor Air Temperature: {air_temp}°C")
```

### Accessing Specific Observation by Name
```python
# Use info dictionary for named access
obs_dict = info  # Or from the observation wrapper

# Better: Use observation wrapper
from sinergym.utils.wrappers import NormalizeObservation

env = gym.make('Eplus-5zone-hot-continuous-v1')
# The environment internally uses obs_dict with variable names as keys
```

### Setting Actions by Index
```python
# For 5zone environment (2 actions)
action = np.array([21.0, 25.0])  # [heating_setpoint, cooling_setpoint]
obs, reward, terminated, truncated, info = env.step(action)

# For smalldatacenter environment (1 action)
action = np.array([22.0])  # [cooling_setpoint]
obs, reward, terminated, truncated, info = env.step(action)
```

---

## 📋 Quick Reference Table

| Environment | Time Vars | Outdoor Vars | Zone Temp Vars | Total Obs | Actions |
|------------|-----------|--------------|----------------|-----------|---------|
| **5zone** | 3 | 6 | 1 | 18 | 2 (htg, clg) |
| **datacenter_cw** | 3 | 6 | 2 | 42 | 2 (clg, chw) |
| **smalldatacenter** | 3 | 6 | 1 | 21 | 1 (clg) |
| **office** | 3 | 6 | 17 | 45 | 2 (htg, clg) |
| **warehouse** | 3 | 6 | 3 | 18 | 2 (htg, clg) |

---

## 🔧 Common Time Variables (All Environments)

These are **always** the first 3 observation variables:

| Index | Variable | Range |
|-------|----------|-------|
| 0 | `month` | 1-12 |
| 1 | `day_of_month` | 1-31 |
| 2 | `hour` | 0-23 |

---

## 🌡️ Common Outdoor Variables (All Environments)

These typically follow time variables (indices 3-8):

| Variable | Description | Unit |
|----------|-------------|------|
| `outdoor_temperature` | Site outdoor air drybulb temperature | °C |
| `outdoor_humidity` | Site outdoor air relative humidity | % |
| `wind_speed` | Site wind speed | m/s |
| `wind_direction` | Site wind direction | degrees |
| `diffuse_solar_radiation` | Diffuse solar radiation | W/m² |
| `direct_solar_radiation` | Direct solar radiation | W/m² |

---

## ⚡ Common Energy Variable (All Environments)

All environments include this observation variable:

| Variable | Description | Unit |
|----------|-------------|------|
| `HVAC_electricity_demand_rate` | Facility total HVAC electricity demand rate | W (Watts) |

---

## 💡 Tips

1. **Observation order matters!** Always use indices consistently.
2. **Action ranges are enforced** by the action space bounds.
3. **Variable names are normalized**: spaces and special characters are replaced with underscores and converted to lowercase.
4. **Check `env.observation_variables`** to see the exact order for your environment.
5. **Use the observation wrapper** for named access to observations.

---

## 📖 Related Files

- YAML Configuration Files: `/workspace/sinergym/data/default_configuration/`
- Check which YAML your environment uses: See `START_HERE.md`

---

**Version:** Sinergym 3.9.7  
**Last Updated:** 2025-11-05
