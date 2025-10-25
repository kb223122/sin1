# YAML Fixes and HVAC Verification Guide

## 🔍 **Issues Found in Your Original YAML**

### **Critical Issues:**
1. **❌ Duplicate Variable Names**: `Heating Coil Electricity Energy` appears twice
2. **❌ Missing Categorized Meters**: No `Heating:Electricity`, `Fans:Electricity`, `Cooling:Electricity` meters
3. **❌ Incorrect Variable Mapping**: Zone reheat coils mapped to energy instead of power

## 🔧 **Required Changes to Your YAML**

### **1. Fix Duplicate Variable Names**
**BEFORE (INCORRECT):**
```yaml
Heating Coil Electricity Energy:
  variable_names: heating_coil_electricity_energy
  keys: MAIN HEATING COIL 1

Heating Coil Electricity Energy:  # ❌ DUPLICATE!
  variable_names:
    - reheat_energy_space1
    - reheat_energy_space2
    # ...
  keys:
    - SPACE1-1 ZONE COIL
    - SPACE2-1 ZONE COIL
    # ...
```

**AFTER (CORRECT):**
```yaml
Heating Coil Electricity Energy:
  variable_names: heating_coil_electricity_energy
  keys: MAIN HEATING COIL 1

Heating Coil Electricity Rate:  # ✅ FIXED - Changed to Rate
  variable_names:
    - reheat_power_space1
    - reheat_power_space2
    # ...
  keys:
    - SPACE1-1 ZONE COIL
    - SPACE2-1 ZONE COIL
    # ...
```

### **2. Add Categorized Meters for Verification**
**ADD TO YOUR METERS SECTION:**
```yaml
meters:
  # EXISTING METERS
  Electricity:HVAC: total_electricity_HVAC
  Electricity:Building: total_electricity_building
  Electricity:Zone:SPACE1-1: zone_electricity_space1
  # ... other existing meters

  # ADD THESE FOR VERIFICATION
  Heating:Electricity: heating_electricity
  Fans:Electricity: fans_electricity
  Cooling:Electricity: cooling_electricity
  Electricity:Facility: total_electricity_facility
```

### **3. Reorganize Variables for Clarity**
**ADD CLEAR COMMENTS:**
```yaml
variables:
  # ---------------------------------- ENERGY ---------------------------------- #
  Environmental Impact Total CO2 Emissions Carbon Equivalent Mass:
    variable_names: co2_emission
    keys: site

  # TOTAL HVAC POWER AND ENERGY
  Facility Total HVAC Electricity Demand Rate:
    variable_names: HVAC_electricity_demand_rate
    keys: Whole Building

  # CENTRAL HVAC SYSTEM COMPONENTS
  Cooling Coil Electricity Energy:
    variable_names: cooling_coil_electricity_energy
    keys: MAIN COOLING COIL 1

  # ZONE REHEAT COIL COMPONENTS (FIXED - was duplicate variable name)
  Heating Coil Electricity Rate:
    variable_names:
      - reheat_power_space1
      - reheat_power_space2
      # ...
```

## 📊 **Verification Methods**

### **Method 1: Meter-Based Energy Verification (RECOMMENDED)**
```python
# Formula: Total HVAC Energy = Heating:Electricity + Fans:Electricity + Cooling:Electricity
total_hvac_energy = obs.get('total_electricity_HVAC', 0.0)
heating_energy = obs.get('heating_electricity', 0.0)
fans_energy = obs.get('fans_electricity', 0.0)
cooling_energy = obs.get('cooling_electricity', 0.0)

calculated_total = heating_energy + fans_energy + cooling_energy
difference = abs(total_hvac_energy - calculated_total)
percentage_error = (difference / total_hvac_energy) * 100
```

### **Method 2: Component-Based Power Verification**
```python
# Formula: Total HVAC Power = Central Components + Zone Components
total_hvac_power = obs.get('HVAC_electricity_demand_rate', 0.0)

# Central system components
central_power = (obs.get('fan_electricity_rate', 0.0) + 
                 obs.get('heating_coil_electricity_rate', 0.0) + 
                 obs.get('cooling_coil_electricity_rate', 0.0))

# Zone reheat components
zone_power = (obs.get('reheat_power_space1', 0.0) + 
              obs.get('reheat_power_space2', 0.0) + 
              obs.get('reheat_power_space3', 0.0) + 
              obs.get('reheat_power_space4', 0.0) + 
              obs.get('reheat_power_space5', 0.0))

calculated_total = central_power + zone_power
```

### **Method 3: Hierarchy Verification**
```python
# Formula: Electricity:Facility ≥ Electricity:Building ≥ Electricity:HVAC
facility_energy = obs.get('total_electricity_facility', 0.0)
building_energy = obs.get('total_electricity_building', 0.0)
hvac_energy = obs.get('total_electricity_HVAC', 0.0)

# Should satisfy: facility_energy >= building_energy >= hvac_energy
```

## 🎯 **Components Contributing to Total HVAC**

### **Central HVAC System (3 components):**
1. **Supply Fan 1** → `fan_electricity_rate` / `fan_electricity_energy`
2. **Main Heating Coil 1** → `heating_coil_electricity_rate` / `heating_coil_electricity_energy`
3. **Main Cooling Coil 1** → `cooling_coil_electricity_rate` / `cooling_coil_electricity_energy`

### **Zone HVAC Systems (5 components):**
1. **SPACE1-1 Zone Coil** → `reheat_power_space1` / `reheat_energy_space1`
2. **SPACE2-1 Zone Coil** → `reheat_power_space2` / `reheat_energy_space2`
3. **SPACE3-1 Zone Coil** → `reheat_power_space3` / `reheat_energy_space3`
4. **SPACE4-1 Zone Coil** → `reheat_power_space4` / `reheat_energy_space4`
5. **SPACE5-1 Zone Coil** → `reheat_power_space5` / `reheat_energy_space5`

### **Additional Components:**
- **Cooling Coil Evaporative Condenser Pump** → `cooling_coil_evaporative_condenser_pump_electricity_energy`
- **Cooling Coil Basin Heater** → `cooling_coil_basin_heater_electricity_energy`

## 🚀 **How to Run Verification**

### **Quick Start:**
```bash
# Use the fixed YAML file
python3 /workspace/run_fixed_verification.py
```

### **Manual Verification:**
```python
from sinergym.envs.eplus_env import EplusEnv
import yaml

# Load the fixed configuration
with open('/workspace/fixed_5zone_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create environment
env = EplusEnv(
    building_file=config['building_file'],
    weather_files=config['weather_specification']['weather_files'][0],
    variables=config['variables'],
    meters=config['meters'],
    actuators=config['actuators']
)

# Run verification
obs, info = env.reset()
for step in range(10):
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Meter-based verification
    total_hvac = obs.get('total_electricity_HVAC', 0.0)
    heating = obs.get('heating_electricity', 0.0)
    fans = obs.get('fans_electricity', 0.0)
    cooling = obs.get('cooling_electricity', 0.0)
    
    calculated_total = heating + fans + cooling
    difference = abs(total_hvac - calculated_total)
    percentage_error = (difference / total_hvac) * 100 if total_hvac > 0 else 0
    
    print(f"Step {step + 1}:")
    print(f"  Total HVAC: {total_hvac:.2f} J")
    print(f"  Calculated: {calculated_total:.2f} J")
    print(f"  Error: {percentage_error:.2f}%")
    
    if terminated or truncated:
        break

env.close()
```

## 📋 **Expected Results**

- ✅ **Energy verification should pass** (< 5% error)
- ✅ **Power verification should pass** (< 5% error)
- ✅ **All 8 HVAC components properly tracked**
- ✅ **Meter-based verification most reliable**

## 🔧 **Summary of Required Changes**

1. **Fix duplicate variable names** in your YAML
2. **Add categorized meters** for verification
3. **Reorganize variables** for clarity
4. **Use the fixed YAML file** provided
5. **Run verification script** to confirm everything works

The fixed YAML file (`/workspace/fixed_5zone_config.yaml`) contains all the necessary changes and is ready to use for proper HVAC verification.