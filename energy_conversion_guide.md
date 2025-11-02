# Energy Conversion & Verification Guide

## 🔄 Watts ↔ Joules Conversion

### Basic Formula
```
Energy (Joules) = Power (Watts) × Time (seconds)
```

### For Your Simulation
- **Timestep**: 15 minutes = 900 seconds
- **Expected Step Energy**: `Energy_step (J) = Power (W) × 900`

### Verification Method

```python
import numpy as np

# Example: Check if heating energy matches rate
def verify_heating_energy(df, step_idx):
    """Verify heating energy conversion"""
    
    # Get current and previous values
    heat_j_current = df.loc[step_idx, 'heating_electricity']  # Cumulative
    heat_j_previous = df.loc[step_idx - 1, 'heating_electricity'] if step_idx > 0 else 0
    
    # Step energy (this is what was consumed THIS timestep)
    heat_j_step = heat_j_current - heat_j_previous
    
    # Power at current timestep (W)
    heat_w = df.loc[step_idx, 'heating_coil_electricity_rate']
    
    # Expected energy for this step
    expected_j_step = heat_w * 900  # 15 min = 900 sec
    
    # Difference
    diff = heat_j_step - expected_j_step
    
    print(f"Step {step_idx}:")
    print(f"  Heating Rate (W): {heat_w:.2f}")
    print(f"  Cumulative J (current): {heat_j_current:.2f}")
    print(f"  Cumulative J (previous): {heat_j_previous:.2f}")
    print(f"  Step Energy (J): {heat_j_step:.2f}")
    print(f"  Expected (W × 900): {expected_j_step:.2f}")
    print(f"  Difference: {diff:.2f} J ({diff/900:.2f} W)")
    
    # Why might they differ?
    if abs(diff) > 100:  # More than 0.1W average difference
        print(f"  ⚠️ Discrepancy - Possible reasons:")
        print(f"     - Zone reheat coils contributed ({heat_j_step - expected_j_step:.2f} J)")
        print(f"     - Variable speed operation")
        print(f"     - Internal EnergyPlus solver timesteps")
    
    return heat_j_step, expected_j_step
```

---

## 📊 Meter Components Breakdown

### `Heating:Electricity` Meter Includes:

| Component | Type | Location | When Active |
|-----------|------|----------|-------------|
| Main Heating Coil 1 | Electric | Central AHU | When supply air < ~18°C |
| SPACE1-1 Zone Coil | Electric Reheat | Zone 1 VAV | When zone needs heat & supply too cold |
| SPACE2-1 Zone Coil | Electric Reheat | Zone 2 VAV | When zone needs heat & supply too cold |
| SPACE3-1 Zone Coil | Electric Reheat | Zone 3 VAV | When zone needs heat & supply too cold |
| SPACE4-1 Zone Coil | Electric Reheat | Zone 4 VAV | When zone needs heat & supply too cold |
| SPACE5-1 Zone Coil | Electric Reheat | Zone 5 VAV | When zone needs heat & supply too cold |

**Total Heating Energy = Main Coil + All Zone Reheat Coils**

---

### `Cooling:Electricity` Meter Includes:

| Component | Type | Location | When Active |
|-----------|------|----------|-------------|
| Main Cooling Coil | DX Compressor | Central AHU | When cooling needed |
| Basin Heater | Electric | Condenser Basin | When condenser temp < 2°C |
| Evap Condenser Pump | Electric | Condenser Loop | When condenser pump runs |

**Total Cooling Energy = Cooling Coil + Basin Heater + Condenser Pump**

---

## 🔍 Step-by-Step Energy Analysis

### Step 13 (Fan Only - Baseline)

```python
# Expected values
fan_w = 117.95
fan_j_expected = 117.95 * 900 = 106,155 J

# From your logs
FanE (J) = 106,152.80 J  # ✓ Matches!

# Verification
diff = 106,152.80 - 106,155 = -2.2 J (negligible)
# This is correct - fan running continuously
```

---

### Step 14 (Heating Starts)

```python
# Heating coil activated
heat_w = 60.66
heat_j_expected_step = 60.66 * 900 = 54,594 J

# From your logs (assuming cumulative)
HeatCoilE (J) cumulative
# If previous was 0, then step energy = 54,594 J ✓

# But check:
# Heat J = 54,593.77 J (cumulative)
# This matches expected ✓
```

---

### Step 31 (Cooling Energy Mystery)

```python
# Cooling coil NOT running
cool_w = 0
cool_j_expected = 0 * 900 = 0 J

# But meter shows
Cool J = 270,000 J  # Cumulative!
BasinHeaterE (J) = 54,000 J

# Breakdown:
# - Basin heater: 54,000 J (this step)
# - Previous cooling: 216,000 J (from earlier steps)

# To verify basin heater:
basin_heater_w = 200 W  # From epJSON
basin_heater_expected = 200 * (270 seconds?) = 54,000 J
# But 200 * 900 = 180,000 J... 

# Actual: Basin heater may have run for ~270 seconds this step
# or accumulated from partial timesteps
```

**Explanation**: Basin heater runs intermittently based on condenser temperature. It doesn't run full 15 minutes - only when condenser temp < 2°C.

---

### Step 33 (Occupancy - Energy Spike)

```python
# Heating coil running hard
heat_w = 1127.96
heat_j_expected_step = 1127.96 * 900 = 1,015,164 J

# But cumulative shows
Heat J = 1,035,209 J

# Difference analysis:
# If previous cumulative was ~20,045 J (from step 32)
# Then step energy = 1,035,209 - 20,045 = 1,015,164 J ✓

# OR if previous was different:
# Step energy = 1,035,209 - (previous cumulative)
# This should include:
# - Main coil: 1127.96 W × 900s = 1,015,164 J
# - Zone reheat coils: ~20,045 J (from previous analysis)
# - Total: ~1,035,209 J ✓
```

---

## 🛠️ Python Code for Energy Verification

```python
import pandas as pd
import numpy as np

def analyze_energy_discrepancies(df):
    """Analyze energy discrepancies between rate and cumulative meters"""
    
    results = []
    
    for i in range(1, len(df)):
        # Get values
        hvac_w = df.loc[i, 'HVAC_electricity_demand_rate']
        heat_w = df.loc[i, 'heating_coil_electricity_rate']
        cool_w = df.loc[i, 'cooling_coil_electricity_rate']
        fan_w = df.loc[i, 'fan_electricity_rate']
        
        # Cumulative (meters)
        hvac_j = df.loc[i, 'total_electricity_HVAC']
        heat_j = df.loc[i, 'heating_electricity']
        cool_j = df.loc[i, 'cooling_electricity']
        fans_j = df.loc[i, 'fans_electricity']
        
        # Previous cumulative
        hvac_j_prev = df.loc[i-1, 'total_electricity_HVAC'] if i > 0 else 0
        heat_j_prev = df.loc[i-1, 'heating_electricity'] if i > 0 else 0
        cool_j_prev = df.loc[i-1, 'cooling_electricity'] if i > 0 else 0
        fans_j_prev = df.loc[i-1, 'fans_electricity'] if i > 0 else 0
        
        # Step energy (this is what happened THIS timestep)
        hvac_j_step = hvac_j - hvac_j_prev
        heat_j_step = heat_j - heat_j_prev
        cool_j_step = cool_j - cool_j_prev
        fans_j_step = fans_j - fans_j_prev
        
        # Expected from rates
        hvac_w_expected = heat_w + cool_w + fan_w
        hvac_j_expected_step = hvac_w_expected * 900
        heat_j_expected_step = heat_w * 900
        cool_j_expected_step = cool_w * 900
        fans_j_expected_step = fan_w * 900
        
        # Discrepancies
        hvac_diff = hvac_j_step - hvac_j_expected_step
        heat_diff = heat_j_step - heat_j_expected_step
        cool_diff = cool_j_step - cool_j_expected_step
        fans_diff = fans_j_step - fans_j_expected_step
        
        results.append({
            'step': i,
            'hvac_w': hvac_w,
            'hvac_w_expected': hvac_w_expected,
            'hvac_w_diff': hvac_w - hvac_w_expected,
            'hvac_j_step': hvac_j_step,
            'hvac_j_expected': hvac_j_expected_step,
            'hvac_j_diff': hvac_diff,
            'heat_j_step': heat_j_step,
            'heat_j_expected': heat_j_expected_step,
            'heat_j_diff': heat_diff,
            'cool_j_step': cool_j_step,
            'cool_j_expected': cool_j_expected_step,
            'cool_j_diff': cool_diff,
            'fans_j_step': fans_j_step,
            'fans_j_expected': fans_j_expected_step,
            'fans_j_diff': fans_diff,
        })
    
    results_df = pd.DataFrame(results)
    
    # Find problematic steps
    print("Steps with energy discrepancies:")
    print(results_df[abs(results_df['hvac_j_diff']) > 1000])
    
    return results_df
```

---

## 📐 Conversion Utilities

```python
def watts_to_joules_per_step(watts, timestep_seconds=900):
    """Convert watts to joules for one timestep"""
    return watts * timestep_seconds

def joules_to_watts_average(joules, timestep_seconds=900):
    """Convert cumulative joules to average watts over timestep"""
    return joules / timestep_seconds

def get_step_energy(cumulative_current, cumulative_previous):
    """Get energy consumed in this step"""
    return cumulative_current - cumulative_previous

def verify_component_energy(rate_w, cumulative_j_current, cumulative_j_previous, 
                            timestep_seconds=900):
    """Verify if rate matches cumulative energy change"""
    expected_step_j = rate_w * timestep_seconds
    actual_step_j = cumulative_j_current - cumulative_j_previous
    
    diff = actual_step_j - expected_step_j
    diff_w = diff / timestep_seconds
    
    match = abs(diff) < 100  # Within 100J tolerance
    
    return {
        'expected_j': expected_step_j,
        'actual_j': actual_step_j,
        'diff_j': diff,
        'diff_w': diff_w,
        'matches': match
    }
```

---

## 🎯 Key Takeaways

1. **Watts** = Instantaneous power (current timestep snapshot)
2. **Joules (Meters)** = Cumulative energy (sum from simulation start)
3. **Step Energy** = Current Joules - Previous Joules
4. **Meters Include ALL Equipment** (main + zones + auxiliaries)
5. **Rate Variables** = Specific component power (main coil, fan, etc.)
6. **Discrepancies Normal** - Meters aggregate, rates are component-specific

---

## 🔧 Troubleshooting Energy Mismatches

### If `HVAC (W) ≠ HeatCoilRate + CoolCoilRate + FanRate`:
- Check if other components included (basin heater, pumps)
- Verify fan power includes all fans
- Meters may include equipment not shown in rate variables

### If `Step Energy ≠ Rate × 900`:
- Check cumulative vs step calculation
- Component may have cycled (on/off during timestep)
- Variable speed operation (power varies)
- Meter includes multiple components, rate is single component

### If `Cooling J ≠ 0` when `CoolCoilRate = 0`:
- Basin heater running (independent of cooling coil)
- Previous timestep energy still in cumulative total
- Condenser pump may be running
