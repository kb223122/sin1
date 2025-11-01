# LLM Pre-Conditioning Control Prompt Template for 5Zone Building

## SYSTEM CONFIGURATION

### Building Overview
- **Building Type**: 5-Zone Office Building
- **Total Floor Area**: 927.20 m²
- **Total Volume**: 1,416.00 m³
- **Zones**: SPACE1-1, SPACE2-1, SPACE3-1, SPACE4-1, SPACE5-1

### Comfort Requirements
- **Winter Comfort Range**: 20.0°C - 23.5°C
- **Summer Comfort Range**: 23.0°C - 26.0°C
- **Summer Period**: June 1 - September 30
- **Winter Period**: October 1 - May 31
- **Target**: Maintain temperature within comfort band at first occupied timestep

---

## ZONE-SPECIFIC INFORMATION

### SPACE1-1
- **Floor Area**: 99.16 m²
- **Volume**: 239.25 m³
- **Ceiling Height**: 2.44 m
- **Reheat Coil Capacity**: 5.67 kW
- **Cooling Design Load**: 5.60 kW
- **Heating Design Load**: 4.63 kW
- **Design Airflow**: 0.635 m³/s (max), 0.0635 m³/s (min)
- **Thermal Response Time**: ~45-60 minutes (estimated)
- **Window Area**: 21.81 m² (south-facing)
- **Wall Area (Exterior)**: 73.20 m²

### SPACE2-1
- **Floor Area**: 42.73 m²
- **Volume**: 103.31 m³
- **Ceiling Height**: 2.44 m
- **Reheat Coil Capacity**: 2.34 kW
- **Cooling Design Load**: 4.73 kW
- **Heating Design Load**: 1.92 kW
- **Design Airflow**: 0.537 m³/s (max), 0.0537 m³/s (min)
- **Thermal Response Time**: ~30-40 minutes (estimated)
- **Window Area**: 9.12 m² (east-facing)
- **Wall Area (Exterior)**: 36.48 m²

### SPACE3-1
- **Floor Area**: 96.48 m²
- **Volume**: 239.25 m³
- **Ceiling Height**: 2.44 m
- **Reheat Coil Capacity**: 5.49 kW
- **Cooling Design Load**: 7.27 kW
- **Heating Design Load**: 4.49 kW
- **Design Airflow**: 0.824 m³/s (max), 0.0824 m³/s (min)
- **Thermal Response Time**: ~45-60 minutes (estimated)
- **Window Area**: 20.85 m² (north-facing)
- **Wall Area (Exterior)**: 73.20 m²

### SPACE4-1
- **Floor Area**: 42.73 m²
- **Volume**: 103.31 m³
- **Ceiling Height**: 2.44 m
- **Reheat Coil Capacity**: 2.34 kW
- **Cooling Design Load**: 5.97 kW
- **Heating Design Load**: 1.92 kW
- **Design Airflow**: 0.677 m³/s (max), 0.0677 m³/s (min)
- **Thermal Response Time**: ~30-40 minutes (estimated)
- **Window Area**: 9.12 m² (west-facing)
- **Wall Area (Exterior)**: 36.48 m²

### SPACE5-1 (Core Zone)
- **Floor Area**: 182.49 m²
- **Volume**: 447.68 m³
- **Ceiling Height**: 2.44 m
- **Reheat Coil Capacity**: 3.25 kW
- **Cooling Design Load**: 6.14 kW
- **Heating Design Load**: 2.66 kW
- **Design Airflow**: 0.696 m³/s (max), 0.0696 m³/s (min)
- **Thermal Response Time**: ~60-75 minutes (estimated) - largest zone
- **Window Area**: 0 m² (NO WINDOWS - interior zone)
- **Wall Area (Exterior)**: 0 m²

---

## BUILDING ENVELOPE PROPERTIES

### Thermal Coefficients (U-Factors)
- **Exterior Walls**: 0.384 W/m²·K
- **Roof**: 0.271 W/m²·K
- **Floor**: 1.649 W/m²·K (HIGHEST HEAT LOSS)
- **Windows**: 3.223 W/m²·K (average) - single: 5.894, double: 2.720
- **Windows SHGC**: 0.756 (solar heat gain coefficient)

### Insulation (R-Values)
- **Walls**: 2.604 m²·K/W (R-14.8)
- **Roof**: 3.690 m²·K/W (R-20.9)
- **Floor**: 0.606 m²·K/W (R-3.4) - POOREST INSULATION
- **Windows**: 0.310 m²·K/W (R-1.76)

### Thermal Mass
- **Building Thermal Capacity**: ~1,350 kJ/K
- **Zone Response Rates**: 
  - Small zones (SPACE2-1, SPACE4-1): ~30-40 min
  - Medium zones (SPACE1-1, SPACE3-1): ~45-60 min
  - Large zone (SPACE5-1): ~60-75 min

---

## HVAC SYSTEM CAPABILITIES

### Central System
- **Main Cooling Coil (High Speed)**: 63.71 kW
- **Main Cooling Coil (Low Speed)**: 21.23 kW
- **Main Heating Coil**: 8.54 kW
- **Total System Airflow**: 3.37 m³/s (max)
- **Supply Air Temperature (Cooling)**: 12.0°C design
- **Supply Air Temperature (Heating)**: 18.0°C design

### Zone Controls
- **Action Space**: [Heating Setpoint, Cooling Setpoint]
- **Heating Setpoint Range**: 12.0°C - 23.25°C
- **Cooling Setpoint Range**: 23.25°C - 30.0°C
- **Setpoint Constraints**: Heating < Cooling (23.25°C boundary)

---

## THERMODYNAMIC UNDERSTANDING

### Heat Loss Characteristics
- **Total Building Heat Loss (Design)**: 54 kW at -17.3°C outdoor
- **Primary Contributors**:
  - Floor conduction: 29.4 kW (54%)
  - Windows: 7.5 kW (14%)
  - Walls: 4.0 kW (7%)
  - Roof: 4.8 kW (9%)
  - Infiltration: ~8-10 kW (16%)

### Heat Gain Characteristics
- **Total Building Heat Gain (Design)**: 30.5 kW at 30.86°C outdoor
- **Primary Contributors**:
  - Solar through windows: 15-25 kW (50-80%)
  - Conduction: 8.3 kW (27%)
  - Infiltration/Ventilation: 2-3 kW (7-10%)
  - Internal gains: ~7.5 kW lighting + equipment (not from outdoor)

### Zone-Specific Heat Loss Rates
**Per degree difference (ΔT = 1°C):**
- SPACE1-1: ~0.42 kW/°C
- SPACE2-1: ~0.18 kW/°C
- SPACE3-1: ~0.42 kW/°C
- SPACE4-1: ~0.18 kW/°C
- SPACE5-1: ~0.35 kW/°C (no windows = lower heat gain/loss)

---

## PRE-CONDITIONING STRATEGY PARAMETERS

### Thermal Response Times (Estimated)
**Time to heat/cool zone by 2°C (typical comfort band adjustment):**

**Small zones (SPACE2-1, SPACE4-1):**
- Heating: ~15-20 minutes
- Cooling: ~10-15 minutes

**Medium zones (SPACE1-1, SPACE3-1):**
- Heating: ~20-30 minutes
- Cooling: ~15-20 minutes

**Large zone (SPACE5-1):**
- Heating: ~30-40 minutes
- Cooling: ~25-30 minutes

### Energy Efficiency Guidelines
1. **Pre-condition early** when outdoor temp is closer to comfort band (less energy needed)
2. **Avoid overshooting** comfort band edges (wastes energy)
3. **Utilize outdoor conditions**: Start earlier if outdoor temp is favorable
4. **Zone prioritization**: Core zone (SPACE5-1) takes longest, start first
5. **Solar consideration**: Zones with windows gain more heat in morning
6. **Floor insulation weak**: Extra heating needed, especially in winter

---

## PROMPT STRUCTURE FOR LLM

```
You are an intelligent HVAC controller for a 5-zone office building managing pre-conditioning strategies.

BUILDING KNOWLEDGE:
[Include all zone-specific data above]
[Include envelope properties]
[Include HVAC capabilities]

CURRENT STATE:
- Current Timestep: {current_timestep}
- Month: {month}
- Day of Month: {day}
- Hour: {hour}
- Weather Forecast: {outdoor_temp_forecast} (next N hours)
- Current Outdoor Temp: {current_outdoor_temp}
- Current Outdoor Humidity: {current_outdoor_humidity}
- Solar Radiation: {solar_radiation}

ZONE STATES:
For each zone (SPACE1-1 through SPACE5-1):
- Current Air Temperature: {zone_temp}
- Current Relative Humidity: {zone_humidity}
- Occupancy Schedule: {next_occupied_timestep}
- Current Setpoints: [Heating: {htg_sp}, Cooling: {clg_sp}]

OBJECTIVE:
1. Calculate optimal pre-conditioning start time for each zone
2. Determine setpoint trajectories to reach comfort band edge at first occupied timestep
3. Minimize energy consumption while ensuring comfort
4. Consider thermal mass and response times for each zone

CONSTRAINTS:
- Comfort Range: Winter [20.0-23.5°C], Summer [23.0-26.0°C]
- Setpoint Range: Heating [12.0-23.25°C], Cooling [23.25-30.0°C]
- Heating Setpoint < Cooling Setpoint must always hold
- Pre-conditioning must complete before first occupied timestep

ENERGY CONSIDERATIONS:
- Each zone has different thermal mass (SPACE5-1 largest, takes longest)
- Floor insulation is poor (U=1.649) - expect higher heating needs
- Solar gains significant for perimeter zones (SPACE1-1, SPACE2-1, SPACE3-1, SPACE4-1)
- SPACE5-1 has no windows - primarily internal loads
- Zone heating capacities vary (2.34-5.67 kW)

DECISION OUTPUT FORMAT:
For each zone, provide:
1. Pre-conditioning start timestep: {start_ts}
2. Setpoint trajectory: [{timestep: sp1, htg_sp: X, clg_sp: Y}, ...]
3. Estimated energy impact: {energy_kWh}
4. Reasoning: {why this strategy}

Calculate optimal strategy now.
```

---

## KEY INFORMATION FOR LLM DECISION-MAKING

### Critical Factors
1. **Zone Size** → Thermal response time (larger = slower)
2. **Current Temperature** → Distance to comfort band
3. **Outdoor Temperature Trend** → Natural help/hindrance
4. **Time Until Occupancy** → How much time available
5. **Zone Orientation** → Solar gain patterns (south/north windows)
6. **HVAC Capacity** → Max heating/cooling rate per zone
7. **Thermal Mass** → Inertia (slower to change)

### Decision Logic Framework
```
IF (zone_temp < comfort_min AND time_to_occupy > response_time):
    START pre-heating early with gradual setpoint increase
    Consider: outdoor_temp (if cold, start earlier)
    
ELIF (zone_temp > comfort_max AND time_to_occupy > response_time):
    START pre-cooling early with gradual setpoint decrease
    Consider: solar_gain (if high, start earlier)
    
ELSE:
    Monitor and adjust minimally
```

---

## OPTIMIZATION PRIORITIES

1. **Comfort Priority**: Ensure comfort at occupancy start (MANDATORY)
2. **Energy Priority**: Minimize overshoot and early operation
3. **Zone Priority**: SPACE5-1 (core, largest) → start first
4. **Weather Priority**: Leverage favorable outdoor conditions
5. **Solar Priority**: Account for morning solar gains on perimeter zones
