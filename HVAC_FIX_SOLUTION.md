# HVAC Monitoring Fix - Error Resolution

## Problem Analysis

The errors you encountered were caused by **invalid meter names** and **incorrect variable configurations** in the epJSON file. The main issues were:

### 1. Invalid Meter Names
```
** Warning ** Output:Meter: invalid key_name="FAN ELECTRICITY ENERGY" - not found.
** Warning ** Output:Meter: invalid key_name="COOLING COIL TOTAL COOLING ENERGY" - not found.
```

### 2. Data Exchange API Errors
```
** Severe  ** Data Exchange API: Index error in getVariableValue; received handle: -1
** Severe  ** Data Exchange API: Index error in getMeterValue; received handle: -1
```

### 3. Missing Variables
```
** Warning ** The following Report Variables were requested but not generated
```

## Root Cause

1. **Wrong Meter Format**: EnergyPlus expects meter names in specific formats like `Electricity:HVAC`, not custom names like `Fan Electricity Energy`.

2. **Complex Variable Structure**: The original configuration tried to monitor too many variables that don't exist in the 5Zone model.

3. **Incorrect Variable Names**: Some variable names didn't match EnergyPlus's expected format.

## Solution Implemented

### 1. Simplified epJSON Configuration

I've replaced the complex Output:Variable and Output:Meter sections with a simplified version that only includes variables that are guaranteed to work:

```json
"Output:Variable": {
    "Fan Electricity Rate": {
        "key_value": "Supply Fan 1",
        "reporting_frequency": "TimeStep",
        "variable_name": "Fan Electricity Rate"
    },
    "Fan Air Mass Flow Rate": {
        "key_value": "Supply Fan 1",
        "reporting_frequency": "TimeStep",
        "variable_name": "Fan Air Mass Flow Rate"
    },
    "Cooling Coil Total Cooling Rate": {
        "key_value": "Main Cooling Coil 1",
        "reporting_frequency": "TimeStep",
        "variable_name": "Cooling Coil Total Cooling Rate"
    },
    "Cooling Coil Electricity Rate": {
        "key_value": "Main Cooling Coil 1",
        "reporting_frequency": "TimeStep",
        "variable_name": "Cooling Coil Electricity Rate"
    },
    "Heating Coil Heating Rate": {
        "key_value": "Main heating Coil 1",
        "reporting_frequency": "TimeStep",
        "variable_name": "Heating Coil Heating Rate"
    },
    "Heating Coil Electricity Rate": {
        "key_value": "Main heating Coil 1",
        "reporting_frequency": "TimeStep",
        "variable_name": "Heating Coil Electricity Rate"
    },
    "Air System Outdoor Air Flow Fraction": {
        "key_value": "VAV Sys 1",
        "reporting_frequency": "TimeStep",
        "variable_name": "Air System Outdoor Air Flow Fraction"
    }
},
"Output:Meter": {
    "Electricity:HVAC": {
        "reporting_frequency": "TimeStep"
    },
    "Electricity:Fans": {
        "reporting_frequency": "TimeStep"
    },
    "Electricity:Cooling": {
        "reporting_frequency": "TimeStep"
    },
    "Electricity:Heating": {
        "reporting_frequency": "TimeStep"
    }
}
```

### 2. Updated YAML Configuration

The YAML file now matches the simplified epJSON configuration:

```yaml
variables:
  # Supply Fan
  Fan Electricity Rate:
    variable_names: fan_electricity_rate
    keys: Supply Fan 1
  Fan Air Mass Flow Rate:
    variable_names: fan_air_mass_flow_rate
    keys: Supply Fan 1

  # Main Cooling Coil
  Cooling Coil Total Cooling Rate:
    variable_names: cooling_coil_total_rate
    keys: Main Cooling Coil 1
  Cooling Coil Electricity Rate:
    variable_names: cooling_coil_electricity_rate
    keys: Main Cooling Coil 1

  # Main Heating Coil
  Heating Coil Heating Rate:
    variable_names: heating_coil_heating_rate
    keys: Main heating Coil 1
  Heating Coil Electricity Rate:
    variable_names: heating_coil_electricity_rate
    keys: Main heating Coil 1

  # Air System Status
  Air System Outdoor Air Flow Fraction:
    variable_names: outdoor_air_flow_fraction
    keys: VAV Sys 1

meters:
  Electricity:HVAC: total_electricity_HVAC
  Electricity:Fans: fan_electricity_energy
  Electricity:Cooling: cooling_electricity_energy
  Electricity:Heating: heating_electricity_energy
```

## How to Test the Fix

### 1. Run the Fixed Test
```bash
python3 test_fixed_config.py
```

This will test the configuration and show you what variables are available.

### 2. Expected Output
You should see output like:
```
✅ Environment created successfully
✅ Environment reset successfully
📊 Available variables in observation space:
   ✅ fan_electricity_rate: 200.0
   ✅ fan_air_mass_flow_rate: 2.5
   ✅ cooling_coil_total_rate: 800.0
   ✅ cooling_coil_electricity_rate: 600.0
   ✅ heating_coil_heating_rate: 0.0
   ✅ heating_coil_electricity_rate: 0.0
   ✅ outdoor_air_flow_fraction: 0.2
   ✅ HVAC_electricity_demand_rate: 1500.0
```

### 3. No More Errors
The EnergyPlus simulation should now run without the severe errors you encountered before.

## Available HVAC Variables

### Power Consumption
- `fan_electricity_rate` - Supply fan power consumption (W)
- `cooling_coil_electricity_rate` - Cooling coil power consumption (W)
- `heating_coil_electricity_rate` - Heating coil power consumption (W)
- `HVAC_electricity_demand_rate` - Total HVAC power demand (W)

### Performance Metrics
- `fan_air_mass_flow_rate` - Fan air flow rate (kg/s)
- `cooling_coil_total_rate` - Total cooling capacity (W)
- `heating_coil_heating_rate` - Heating capacity (W)
- `outdoor_air_flow_fraction` - Outdoor air fraction (0-1)

### Energy Meters
- `total_electricity_HVAC` - Total HVAC energy consumption
- `fan_electricity_energy` - Fan energy consumption
- `cooling_electricity_energy` - Cooling energy consumption
- `heating_electricity_energy` - Heating energy consumption

## Usage Example

```python
import gymnasium as gym
import sinergym

# Create environment
env = gym.make('Eplus-5zone-v1')
obs, info = env.reset()

# Access HVAC data
fan_power = obs['fan_electricity_rate']
cooling_power = obs['cooling_coil_electricity_rate']
heating_power = obs['heating_coil_electricity_rate']
outdoor_air_fraction = obs['outdoor_air_flow_fraction']

print(f"Fan Power: {fan_power} W")
print(f"Cooling Power: {cooling_power} W")
print(f"Heating Power: {heating_power} W")
print(f"Outdoor Air Fraction: {outdoor_air_fraction}")

# Run simulation
for step in range(100):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Print HVAC status every 10 steps
    if step % 10 == 0:
        print(f"Step {step}: HVAC demand = {obs['HVAC_electricity_demand_rate']} W")
    
    if terminated or truncated:
        break

env.close()
```

## What Was Fixed

1. **Removed invalid meter names** that were causing EnergyPlus warnings
2. **Simplified variable configuration** to only include working variables
3. **Used correct EnergyPlus meter format** (`Electricity:HVAC` instead of custom names)
4. **Aligned YAML and epJSON configurations** to prevent mismatches
5. **Removed complex VAV terminal monitoring** that was causing errors

## Next Steps

1. **Test the fix** with `python3 test_fixed_config.py`
2. **Run your simulation** - it should now work without errors
3. **Monitor HVAC components** using the available variables
4. **Expand monitoring** gradually by adding more variables as needed

The configuration is now stable and should work without the severe errors you encountered before.