# HVAC Power and Energy Verification Guide for 5-Zone Building

## Overview

This guide explains how to cross-check and confirm that the total HVAC power and energy in the 5-zone building is the sum of all individual components, based on the actual EnergyPlus data available in the simulation.

## 🔍 HVAC Components Identified

### Central HVAC System (3 components)
1. **Supply Fan 1** → `Fan Electricity Rate` (SUPPLY FAN 1)
2. **Main Heating Coil 1** → `Heating Coil Electricity Rate` (MAIN HEATING COIL 1)
3. **Main Cooling Coil 1** → `Cooling Coil Electricity Rate` (MAIN COOLING COIL 1)

### Zone HVAC Systems (5 components)
1. **SPACE1-1 Zone Coil** → `Heating Coil Electricity Rate` (SPACE1-1 ZONE COIL)
2. **SPACE2-1 Zone Coil** → `Heating Coil Electricity Rate` (SPACE2-1 ZONE COIL)
3. **SPACE3-1 Zone Coil** → `Heating Coil Electricity Rate` (SPACE3-1 ZONE COIL)
4. **SPACE4-1 Zone Coil** → `Heating Coil Electricity Rate` (SPACE4-1 ZONE COIL)
5. **SPACE5-1 Zone Coil** → `Heating Coil Electricity Rate` (SPACE5-1 ZONE COIL)

## ⚠️ Verification Challenges

### Variable Name Conflicts
- Multiple `Heating Coil Electricity Rate` variables exist (one for each zone)
- Sinergym cannot easily distinguish between them
- This limits direct component-by-component verification

### Solution: Use Categorized Meters
The most reliable verification method uses EnergyPlus meters that automatically aggregate components by category.

## 📊 Verification Methods

### Method 1: Meter-Based Verification (RECOMMENDED)

**Energy Verification:**
```
Total HVAC Energy = Heating:Electricity + Fans:Electricity + Cooling:Electricity
```

**Available Meters:**
- `Electricity:HVAC` - Total HVAC electricity energy
- `Heating:Electricity` - All heating components (main + zone coils)
- `Fans:Electricity` - All fan components
- `Cooling:Electricity` - All cooling components

**Verification Formula:**
```
Electricity:HVAC ≈ Heating:Electricity + Fans:Electricity + Cooling:Electricity
```

### Method 2: Central System Verification

**Power Verification (Central System Only):**
```
Central HVAC Power = Supply Fan + Main Heating + Main Cooling
```

**Components:**
- `Fan Electricity Rate` (SUPPLY FAN 1)
- `Heating Coil Electricity Rate` (MAIN HEATING COIL 1)
- `Cooling Coil Electricity Rate` (MAIN COOLING COIL 1)

**Note:** Zone reheat coils are not included due to variable name conflicts.

### Method 3: Hierarchy Verification

**Energy Hierarchy:**
```
Electricity:Facility ≥ Electricity:Building ≥ Electricity:HVAC
```

**Verification:**
- `Electricity:Facility` - Total facility electricity
- `Electricity:Building` - Total building electricity
- `Electricity:HVAC` - Total HVAC electricity

## 🚀 How to Run Verification

### Quick Start
```bash
python3 /workspace/run_final_verification.py
```

### Manual Verification
```python
from sinergym.envs.eplus_env import EplusEnv
import yaml

# Load configuration
with open('/workspace/final_hvac_verification_config.yaml', 'r') as f:
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
    
    # Check energy verification
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

## 📈 Expected Results

### Energy Verification
- **Expected:** Sum of categorized meters ≈ Total HVAC energy
- **Tolerance:** < 5% difference
- **Status:** Should pass consistently

### Power Verification
- **Expected:** Central system components ≈ Total HVAC power
- **Tolerance:** < 50% difference (due to missing zone components)
- **Status:** May show differences due to variable name conflicts

## 🔧 Troubleshooting

### If Energy Verification Fails
1. Check meter definitions in EnergyPlus building model
2. Verify that all HVAC components are properly categorized
3. Check for missing or misconfigured meters

### If Power Verification Fails
1. This is expected due to variable name conflicts
2. Use energy verification instead (more reliable)
3. Consider modifying the building model to use unique variable names

### If Both Verifications Fail
1. Check EnergyPlus building model configuration
2. Verify that HVAC components are properly defined
3. Check for simulation errors or warnings

## 📋 Verification Checklist

- [ ] Environment created successfully
- [ ] All required variables and meters available
- [ ] Energy verification passes (< 5% error)
- [ ] Power verification shows reasonable results
- [ ] No simulation errors or warnings
- [ ] Data collection working properly

## 🎯 Key Takeaways

1. **Energy verification is more reliable** than power verification
2. **Use categorized meters** for comprehensive verification
3. **Variable name conflicts** limit direct component verification
4. **Total HVAC energy** should equal sum of categorized energy meters
5. **Central system power** can be verified individually
6. **Zone reheat coils** are included in heating energy meter

## 📚 Additional Resources

- EnergyPlus documentation on meters and variables
- Sinergym documentation on environment configuration
- Building model analysis for component identification
- EnergyPlus output variable reference guide

---

**Note:** This verification approach is based on the actual EnergyPlus data available in the 5-zone building simulation. The methods described here provide the most reliable way to cross-check HVAC power and energy calculations given the constraints of the available data structure.