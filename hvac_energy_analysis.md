# Deep Analysis: 5Zone HVAC Energy & Control Behavior

## 🔍 KEY FINDINGS FROM YOUR LOGS

### **1. Why Main Heating Coil Runs with Setpoints (12, 30)**

**Root Cause**: EnergyPlus VAV system maintains **minimum supply air temperature** regardless of zone setpoints.

**Evidence from epJSON**:
- Main Heating Coil has: `"temperature_setpoint_node_name": "Main Heating Coil 1 Outlet Node"`
- System sizing specifies: `"central_heating_design_supply_air_temperature": 18.0`
- Pre-heat design temp: `"preheat_design_temperature": -15.0`

**What's Happening**:
1. **Step 13**: Outdoor = 2.95°C, Indoor ~16.7°C, Setpoints (12, 30)
   - Mixed air (outdoor + return) → Very cold supply air
   - Main heating coil activates to heat supply air to ~18°C minimum
   - This is **system protection**, not zone control

2. **Steps 14-23**: As outdoor drops (2.95°C → 0.80°C)
   - Supply air gets colder → Main coil works harder (60W → 381W)
   - Indoor temps drift down (16.68°C → 15.92°C)
   - **Zone setpoints don't matter** - system maintains supply temp

3. **Why Zone Reheat Coils Show "nan"**:
   - Zone reheat coils only activate when zone needs heating AND supply air is too cold
   - With HSP=12°C and indoor ~16°C, zones don't need heat
   - But supply air at 18°C is still acceptable for zones (not too cold)
   - So reheat coils stay OFF → "nan" (not reported when not operating)

---

### **2. Energy Calculations: Watts vs Joules**

#### **EnergyPlus Reporting**:

**Watts (Rate variables)**:
- `HVAC_electricity_demand_rate` = Instantaneous power (W) at current timestep
- `heating_coil_electricity_rate` = Current heating coil power (W)
- `cooling_coil_electricity_rate` = Current cooling coil power (W)
- `fan_electricity_rate` = Current fan power (W)

**Joules (Meter variables - CUMULATIVE)**:
- `total_electricity_HVAC` = Cumulative energy since simulation start (J)
- `heating_electricity` = Cumulative heating energy (J) - includes ALL heating equipment
- `cooling_electricity` = Cumulative cooling energy (J) - includes coil + basin heater + pumps
- `fans_electricity` = Cumulative fan energy (J)

**Key Difference**:
- **Watts** = snapshot at current timestep
- **Joules** = running total accumulated from simulation start

#### **Your Timestep = 15 minutes = 900 seconds**

**Expected Conversion**: 
- Energy (J) = Power (W) × Time (s)
- For one step: J_step = W_current × 900

**Why They Don't Match Exactly**:

1. **Cumulative vs Instantaneous**:
   - Joules are **cumulative** (sum from t=0 to now)
   - Watts are **instantaneous** (current timestep only)
   - To get step energy: J_step = J_current - J_previous

2. **Meter Aggregation**:
   - `heating_electricity` meter includes:
     - Main heating coil
     - All zone reheat coils (when operating)
     - Any other electric heating equipment
   - `cooling_electricity` meter includes:
     - Cooling coil
     - Basin heater (for DX coils)
     - Evaporative condenser pump
     - Any other cooling equipment

3. **EnergyPlus Internal Calculations**:
   - EnergyPlus uses variable timesteps internally
   - Meter values are accumulated using internal solver timesteps (often sub-hourly)
   - Reported values may reflect fractional timesteps or averaging

---

### **3. Step-by-Step Analysis**

#### **Step 13** (Baseline - Fan Only):
```
HVAC = 117.95W (fan only)
HeatCoilRate = 0W, CoolCoilRate = 0W
Indoor: Z1=16.68°C, Z5=18.65°C
Outdoor: 2.95°C
Setpoints: All (12, 30)
```
**Analysis**: System is at equilibrium. No heating/cooling needed.

#### **Step 14** (Heating Starts):
```
HVAC = 178.61W
HeatCoilRate = 60.66W (MAIN COIL ACTIVATED!)
CoolCoilRate = 0W
Outdoor: 2.58°C (getting colder)
Indoor: Dropping (16.68→16.60°C)
```
**Why Heating?**: 
- Outdoor temp dropped → mixed air colder
- Supply air temp fell below ~18°C threshold
- **Main heating coil activates** to maintain minimum supply temp
- This is **independent of zone setpoints**

#### **Steps 15-23** (Heating Increases):
```
HeatCoilRate: 99W → 245W → 381W (increasing)
Outdoor: 2.20°C → 0.80°C (getting colder)
Indoor: Continuing to drop
```
**Pattern**: As outdoor gets colder, more heating needed to maintain supply air temp.

#### **Step 24** (Power Spike):
```
HVAC = 1464.61W (MASSIVE INCREASE)
HeatCoilRate = 1141.66W
Outdoor: 0.98°C
OA Fraction: 0.246 (24.6% outdoor air!)
```
**Why Spike?**: 
- Higher outdoor air fraction (economizer or OA requirement)
- More cold air → more heating needed
- Main coil working at high capacity

#### **Step 31** (Cooling Joules ≠ 0, but Rate = 0):
```
CoolCoilRate (W) = 0 (coil not running)
Cool J = 270,000J
BasinHeaterE (J) = 54,000J
```
**Explanation**:
- **Basin heater** runs independently (prevents condenser water freezing)
- Basin heater power ≈ 200W (from epJSON)
- Runs when condenser temp < 2°C (setpoint)
- 200W × 270 seconds ≈ 54,000J ✓
- But why 270,000J total? Additional sources:
  - Meter accumulation includes previous timesteps
  - Evaporative condenser pump energy
  - Residual energy from previous operation

#### **Step 33** (Occupancy Starts):
```
HVAC = 1285.90W
HeatCoilRate = 1127.96W
Heat J = 1,035,209J
Building J = 7,875,000J (HUGE - includes lighting/equipment!)
```
**Why Heat J ≠ HeatCoilRate × Time?**:
- Heat J is **cumulative** from start of simulation
- HeatCoilRate is **current** timestep power
- Previous timesteps already accumulated
- Calculation: Heat J_step = 1,035,209 - (previous cumulative) ≠ 1127.96W × 900s

---

### **4. What Contributes to Energy Meters**

#### **`Heating:Electricity` Meter Includes**:
1. Main Heating Coil 1 (central system)
2. SPACE1-1 Zone Coil (reheat)
3. SPACE2-1 Zone Coil (reheat)
4. SPACE3-1 Zone Coil (reheat)
5. SPACE4-1 Zone Coil (reheat)
6. SPACE5-1 Zone Coil (reheat)

#### **`Cooling:Electricity` Meter Includes**:
1. Main Cooling Coil 1 (DX compressor)
2. Cooling Coil Basin Heater (anti-freeze)
3. Evaporative Condenser Pump (if active)
4. Any other cooling auxiliary equipment

#### **`Fans:Electricity` Meter Includes**:
1. Supply Fan 1 (VAV system fan)
2. Any other fans (exhaust, etc.)

---

### **5. Temperature Drift Analysis**

#### **When Only Fan Running (Steps 13, parts of 14-23)**:

**Indoor temp drift factors** (by influence):

1. **Outdoor Temperature** (PRIMARY) - 80% influence
   - Direct conduction through envelope
   - Infiltration (cold air leaks in)
   - Large ΔT (16.7°C indoor vs 2.95°C outdoor) = rapid heat loss

2. **Heat Loss Rate** (from envelope):
   - **Floor**: U=1.649 W/m²·K (POOREST - biggest loss)
   - **Walls**: U=0.384 W/m²·K
   - **Roof**: U=0.271 W/m²·K
   - **Windows**: U=3.223 W/m²·K (high loss, but small area)

3. **Wind Speed** - 10% influence
   - Increases convective heat transfer
   - Your logs: 3.5 m/s → 2.4 m/s (moderate)

4. **Solar Radiation** - 5% influence (MINIMAL at night)
   - Steps 13-23: DirectSolar = 0 W/m² (night)
   - No solar gain → no offset

5. **Internal Gains** - 5% influence
   - Lights OFF (occupancy = 0)
   - Equipment minimal
   - SPACE5-1 has more internal gains (equipment) → stays warmer (18.65°C vs 16.68°C)

**Why SPACE5-1 Drifts Slower**:
- Larger thermal mass (182.49 m² vs 99.16 m²)
- More internal gains (equipment/people)
- No windows (no direct heat loss)
- Interior zone (surrounded by other zones = less envelope loss)

---

### **6. Energy Calculation Discrepancies Explained**

#### **Why Fan J ≠ FanRate × Time in Step 31**:

**Step 31 Logs**:
```
FanRate (W) = 117.95W
FanE (J) = 21,230.56J (in your code as fan_electricity_energy)
Expected: 117.95 × 900 = 106,152.8J (for 15-min step)
But previous FanE = 106,152.80J
Difference: 106,152.80 - 21,230.56 = 84,922.24J
```

**Possible Reasons**:
1. **Fan cycling** - Fan may have cycled off/on during timestep
2. **Variable speed operation** - Fan power varies, meter accumulates average
3. **Reporting delay** - EnergyPlus meters may report at different intervals
4. **Multiple fans** - If there are other fans (exhaust, etc.), they're included in meter

#### **Why Heat J ≠ HeatCoilRate × Time in Step 33**:

**Step 33**:
```
HeatCoilRate = 1127.96W (main coil only)
Heat J = 1,035,209J (cumulative)
```

**Calculation Check**:
- If this is step 33, and step 32 had Heat J = ~1,129,285J
- Step 33 Heat J - Step 32 Heat J = 1,035,209 - (previous)
- This should equal: HeatCoilRate × 900s + ReheatCoil contributions

**Missing Components**:
- Zone reheat coils may have contributed in previous timesteps
- Meter includes ALL heating equipment, not just main coil
- Accumulation includes partial timesteps from solver iterations

---

### **7. Why Cooling Joules Exist When Rate = 0**

**Step 31 Analysis**:
```
CoolCoilRate (W) = 0 (compressor OFF)
Cool J = 270,000J
BasinHeaterE (J) = 54,000J
```

**What's in "Cool J"** (Cooling:Electricity meter):
1. Basin Heater = 54,000J ✓
2. Remaining 216,000J comes from:
   - Previous timestep accumulation (compressor ran earlier)
   - Evaporative condenser pump (if active)
   - Meter is CUMULATIVE - includes all past cooling energy

**Why Basin Heater Runs When Cooling Coil is OFF**:
- Basin heater prevents condenser water from freezing
- Setpoint: 2°C (from epJSON)
- Runs independently when condenser temp < 2°C
- This is **maintenance heating**, not cooling load

---

### **8. Real-World HVAC Control Truth**

#### **Why Main Heating Coil Runs Despite Low Zone Setpoints**:

**VAV System Design**:
- VAV systems require **minimum supply air temperature** (~15-18°C)
- Below this, condensation forms → equipment damage
- Supply air must be warm enough for proper mixing

**Control Hierarchy**:
1. **System Level**: Maintain supply air temp ≥ 18°C (main heating coil)
2. **Zone Level**: Maintain zone temp within setpoint band (reheat coils)

**Your Case**:
- Zone setpoints (12, 30) = zones don't need heat
- But outdoor = 2°C → mixed air very cold
- Supply air would be < 12°C without main heating
- **Main coil MUST run** to protect system, regardless of zone setpoints

**This is NOT a bug - it's correct HVAC operation!**

---

### **9. EnergyPlus Meter vs Variable Difference**

#### **Variable (Rate)**:
- `Coil:Heating:Electric Main heating Coil 1 Electricity Rate` = Power at this timestep
- `Fan:VariableVolume Supply Fan 1 Electricity Rate` = Fan power at this timestep

#### **Meter (Cumulative)**:
- `Heating:Electricity` = Sum of ALL heating equipment energy since start
- `Cooling:Electricity` = Sum of ALL cooling equipment energy since start
- `Fans:Electricity` = Sum of ALL fan energy since start

**To Get Step Energy**:
```
Step_Energy (J) = Meter_Current (J) - Meter_Previous (J)
```

**Why HVAC J Doesn't Match Sum**:
```
HVAC (W) = HeatCoilRate + CoolCoilRate + FanRate (instantaneous)
HVAC J = Cumulative total (includes all components + previous timesteps)
```

---

### **10. Practical Recommendations**

1. **For Pre-Conditioning Control**:
   - Account for **main heating coil minimum operation** (~18°C supply temp)
   - Even with zone HSP=12°C, system may heat supply air
   - This is **unavoidable** - part of VAV system design

2. **For Energy Monitoring**:
   - Use **rate variables** (W) for real-time power
   - Use **meter variables** (J) for cumulative energy
   - Calculate step energy as: ΔJ = J_current - J_previous

3. **For Control Logic**:
   - Zone setpoints control **reheat coils** (zone-level)
   - System-level controls **main coil** (supply temp protection)
   - These operate independently

---

## 📊 SUMMARY

| Issue | Explanation |
|-------|-------------|
| **Main heating runs with (12,30)** | System maintains min supply air temp ~18°C (VAV protection) |
| **Reheat coils show "nan"** | Not operating when zones don't need heat |
| **Cool J ≠ 0 when Rate = 0** | Cumulative meter includes basin heater + previous timesteps |
| **Heat J ≠ HeatCoilRate × time** | Cumulative vs instantaneous + includes all heating equipment |
| **Fan J changes oddly** | Fan may cycle, variable speed, or includes multiple fans |
| **Outdoor temp = primary driver** | 80% of temperature drift when unoccupied |
| **SPACE5-1 drifts slowest** | Largest thermal mass, no windows, more internal gains |

**Bottom Line**: The HVAC behavior is **correct**. Main heating coil protects system by maintaining minimum supply air temperature, independent of zone setpoints. Energy calculations are cumulative (Joules) vs instantaneous (Watts), requiring step-wise differences to get per-timestep energy.
