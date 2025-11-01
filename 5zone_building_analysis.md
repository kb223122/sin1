# 5Zone Building Analysis - Extracted Values from EnergyPlus Report

## 1. HVAC HEATING AND COOLING CAPACITY

### Main System Coils:
- **Main Cooling Coil (High Speed)**: 63,709.87 W = **63.71 kW**
- **Main Cooling Coil (Low Speed)**: 21,234.50 W = **21.23 kW**
- **Main Heating Coil**: 8,538.39 W = **8.54 kW**

### Zone Reheat Coils:
- **SPACE1-1 Zone Coil**: 5,666.80 W = **5.67 kW**
- **SPACE2-1 Zone Coil**: 2,343.86 W = **2.34 kW**
- **SPACE3-1 Zone Coil**: 5,488.00 W = **5.49 kW**
- **SPACE4-1 Zone Coil**: 2,343.86 W = **2.34 kW**
- **SPACE5-1 Zone Coil**: 3,251.52 W = **3.25 kW**

### Total HVAC Capacity:
- **Total Cooling Capacity**: 63.71 kW (high speed)
- **Total Heating Capacity**: 8.54 kW (main) + 18.09 kW (zones) = **26.63 kW**

---

## 2. DESIGN HEATING AND COOLING LOAD

### Zone Cooling Loads (Sensible):
- **SPACE1-1**: Calculated: 4,308.22 W, User (with 1.3 factor): 5,600.68 W
- **SPACE2-1**: Calculated: 3,640.23 W, User: 4,732.30 W
- **SPACE3-1**: Calculated: 5,593.41 W, User: 7,271.43 W
- **SPACE4-1**: Calculated: 4,590.04 W, User: 5,967.05 W
- **SPACE5-1**: Calculated: 4,720.71 W, User: 6,136.93 W

**Total Zone Cooling Load**: 22,852.61 W (calculated) = **22.85 kW**
**Total Zone Cooling Load (User)**: 29,708.39 W = **29.71 kW**

### Zone Heating Loads (Sensible):
- **SPACE1-1**: Calculated: 3,564.26 W, User: 4,633.53 W
- **SPACE2-1**: Calculated: 1,474.22 W, User: 1,916.49 W
- **SPACE3-1**: Calculated: 3,451.80 W, User: 4,487.34 W
- **SPACE4-1**: Calculated: 1,474.22 W, User: 1,916.49 W
- **SPACE5-1**: Calculated: 2,045.12 W, User: 2,658.66 W

**Total Zone Heating Load**: 12,009.62 W (calculated) = **12.01 kW**
**Total Zone Heating Load (User)**: 15,612.51 W = **15.61 kW**

### System Design Loads:
- **System Cooling Capacity**: 48,238.56 W = **48.24 kW**
- **System Heating Capacity**: 16,729.67 W = **16.73 kW**

---

## 3. BUILDING THERMAL COEFFICIENT (U-Factor)

### Exterior Opaque Surfaces:
- **Walls (WALL-1)**: U-Factor with Film = **0.384 W/m²-K**
- **Roof (ROOF-1)**: U-Factor with Film = **0.271 W/m²-K**
- **Floor (FLOOR-SLAB-1)**: U-Factor with Film = **1.649 W/m²-K**

### Windows:
- **Single Glazing Grey**: U-Factor = **5.894 W/m²-K**
- **Double Clear**: U-Factor = **2.720 W/m²-K**
- **Average Window U-Factor**: **3.223 W/m²-K**

### Interior Surfaces (for reference):
- **Ceiling (CLNG-1)**: 1.085 W/m²-K
- **Interior Walls (INT-WALL-1)**: 1.680 W/m²-K

---

## 4. BUILDING INSULATION (R-Value)

R-Value = 1 / U-Factor

- **Walls**: R = 1/0.384 = **2.604 m²·K/W** = **R-14.8** (US units: R = R-Value × 5.678)
- **Roof**: R = 1/0.271 = **3.690 m²·K/W** = **R-20.9**
- **Floor**: R = 1/1.649 = **0.606 m²·K/W** = **R-3.4**
- **Windows (Single)**: R = 1/5.894 = **0.170 m²·K/W** = **R-0.96**
- **Windows (Double)**: R = 1/2.720 = **0.368 m²·K/W** = **R-2.09**

---

## 5. BUILDING THERMAL MASS

Thermal mass is not directly reported in EnergyPlus outputs. It must be calculated from material properties.

From "Opaque Construction Layers":
- **WALL-1**: WD01, PW03, IN02, GP01 (Wood, Insulation, Gypsum)
- **ROOF-1**: RG01, BR01, IN46, WD01 (Roof Membrane, Insulation, Wood)
- **FLOOR-SLAB-1**: CC03, CP01 (Concrete)

**Approximate Thermal Mass** (from typical material densities and thicknesses):
- **Total Building Volume**: 1,416.00 m³
- **Total Floor Area**: 927.20 m²
- **Thermal Capacity** (estimated from typical office building): ~**1,200-1,500 kJ/K** for entire building

---

## 6. LATENT COOLING

From "Component Sizing Summary" - Cooling Coil:
- **Main Cooling Coil Total Capacity**: 63,709.87 W
- **Main Cooling Coil Sensible Capacity**: 50,888.14 W
- **Latent Cooling Capacity**: 63,709.87 - 50,888.14 = **12,821.73 W** = **12.82 kW**

**Sensible Heat Ratio (SHR)**: 0.7987 (79.87% sensible, 20.13% latent)

---

## 7. HEAT LOSS TO OUTDOOR

Heat loss occurs through:
1. **Conduction through envelope** (U × Area × ΔT)
2. **Infiltration** (air leakage)
3. **Ventilation** (outdoor air requirements)

### Envelope Areas:
- **Wall Area**: 274.20 m²
- **Roof Area**: 463.60 m²
- **Floor Area**: 463.60 m²
- **Window Area**: 60.90 m²

### Calculated Heat Loss (at Design Heating Conditions):
Design conditions: Indoor 21.1°C, Outdoor -17.3°C, ΔT = 38.4°C

**Wall Heat Loss**: 0.384 W/m²-K × 274.20 m² × 38.4°C = **4,044 W**
**Roof Heat Loss**: 0.271 W/m²-K × 463.60 m² × 38.4°C = **4,828 W**
**Floor Heat Loss**: 1.649 W/m²-K × 463.60 m² × 38.4°C = **29,390 W**
**Window Heat Loss**: 3.223 W/m²-K × 60.90 m² × 38.4°C = **7,545 W**

**Total Envelope Heat Loss**: 45,807 W = **45.81 kW**

**Infiltration Heat Loss** (from Zone Sizing):
- Average infiltration ACH: 0.25
- Estimated infiltration heat loss: ~**8,000-10,000 W** = **8-10 kW**

**Total Heat Loss to Outdoor**: ~**54 kW** (at design conditions)

---

## 8. HEAT GAIN FROM OUTDOOR

Heat gain occurs through:
1. **Solar radiation** (windows)
2. **Conduction** (when outdoor > indoor)
3. **Infiltration/Ventilation** (warm outdoor air)

### At Design Cooling Conditions:
Design conditions: Indoor 23.9°C, Outdoor 30.86°C, ΔT = 6.96°C

**Conductive Heat Gain** (reversed):
- **Wall Heat Gain**: 0.384 × 274.20 × 6.96 = **732 W**
- **Roof Heat Gain**: 0.271 × 463.60 × 6.96 = **875 W**
- **Floor Heat Gain**: 1.649 × 463.60 × 6.96 = **5,312 W**
- **Window Heat Gain**: 3.223 × 60.90 × 6.96 = **1,366 W**

**Total Conductive Heat Gain**: 8,285 W = **8.29 kW**

**Solar Heat Gain** (Windows):
- Window SHGC (average): 0.756
- Direct solar radiation on windows: Estimated **15,000-25,000 W** = **15-25 kW** (peak)

**Infiltration/Ventilation Heat Gain**: ~**2,000-3,000 W** = **2-3 kW**

**Total Heat Gain from Outdoor**: ~**25-36 kW** (at design cooling conditions, including solar)

---

## SUMMARY TABLE

| Parameter | Value | Unit | Notes |
|-----------|-------|------|-------|
| **Cooling Capacity** | 63.71 | kW | High speed |
| **Heating Capacity** | 26.63 | kW | Total (main + zones) |
| **Design Cooling Load** | 29.71 | kW | User (with safety factor) |
| **Design Heating Load** | 15.61 | kW | User (with safety factor) |
| **Latent Cooling** | 12.82 | kW | At peak conditions |
| **Wall U-Factor** | 0.384 | W/m²-K | Exterior walls |
| **Roof U-Factor** | 0.271 | W/m²-K | |
| **Floor U-Factor** | 1.649 | W/m²-K | |
| **Wall R-Value** | 2.604 | m²·K/W | R-14.8 (US) |
| **Roof R-Value** | 3.690 | m²·K/W | R-20.9 (US) |
| **Window U-Factor** | 3.223 | W/m²-K | Average |
| **Window R-Value** | 0.310 | m²·K/W | R-1.76 (US) |
| **Thermal Mass** | ~1,200-1,500 | kJ/K | Estimated |
| **Heat Loss (Design)** | ~54 | kW | At -17.3°C outdoor |
| **Heat Gain (Design)** | ~25-36 | kW | At 30.86°C outdoor (incl. solar) |

---

## NOTES

1. **Design loads** include a 1.3 safety factor as specified in Sizing:Parameters
2. **Heat loss/gain** values are calculated at design conditions and will vary with actual weather
3. **Thermal mass** is estimated based on typical building construction; exact value requires material property extraction from epJSON
4. **Solar heat gain** is a significant contributor during cooling design conditions
5. All values are from sizing calculations (design days), not annual simulation results
